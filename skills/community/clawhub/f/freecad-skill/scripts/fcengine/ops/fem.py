"""Linear static FEM (Gmsh + CalculiX) with built-in verification.

Probed on FreeCAD 1.1 (cantilever 100x10x10 mm steel, 1000 N):
- 1st-order tetrahedra are ~39 % too stiff in bending; 2nd order match the
  analytic deflection within 0.3 %, so 2nd order is always used.
- A force given as a bare number is interpreted in mN; loads must carry units.
- CalculiX writes the reaction at the fixed faces to the .dat file, which
  gives an equilibrium check.
Every run checks equilibrium and, unless 'convergence' is false, mesh
convergence (a second solve on a finer mesh), so wrong models or meshes are
visible instead of plausible-looking. A check that cannot run (convergence
turned off, no reaction in the solver output) is reported as a warning, never
skipped silently.
"""

from __future__ import annotations

import glob
import math
import os
import shutil
import tempfile
from typing import Any, Dict, List, Optional, Tuple

import FreeCAD as App

from .. import errors, geometry, matdata, workspace
from ..document import Context
from ..errors import SkillError

DISCLAIMER = (
    "Linear static estimate (small deformations, linear elastic material, no contact). "
    "Not a substitute for engineering review; stresses at sharp inner corners are mesh-dependent."
)


MESH_TIMEOUT = 120.0  # s


def _safe_gmsh_class() -> Any:
    """GmshTools that meshes single-threaded, with a timeout, and reads the mesh back deterministically.

    FreeCAD writes 'General.NumThreads = <cpu count>' and waits on Gmsh with no
    timeout; the multithreaded 3D mesher occasionally deadlocks (seen in testing:
    a Gmsh process spinning for >10 min on a 100 mm beam). In FreeCAD 1.1,
    create_mesh() runs Gmsh through a QProcess (ObjectTools.run: waitForFinished(-1))
    and reads the mesh in a 'finished' signal handler, bypassing run_gmsh_with_geo;
    headless, that handler does not always run, which showed as occasional empty
    meshes. create_mesh is therefore replaced as well.
    """
    import re
    import subprocess

    from femmesh.gmshtools import GmshTools

    class SafeGmsh(GmshTools):  # type: ignore[misc]
        def run_gmsh_with_geo(self) -> str:
            with open(self.temp_file_geo, encoding="utf-8") as fh:
                geo = fh.read()
            with open(self.temp_file_geo, "w", encoding="utf-8") as fh:
                fh.write(re.sub(r"General\.NumThreads\s*=\s*\d+;", "General.NumThreads = 1;", geo))
            kwargs: Dict[str, Any] = {}
            try:
                import femtools.femutils as femutils

                kwargs["startupinfo"] = femutils.startProgramInfo("hide")
            except Exception:
                pass
            p = subprocess.Popen(
                [self.gmsh_bin, "-", self.temp_file_geo], stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs
            )
            try:
                _out, err = p.communicate(timeout=MESH_TIMEOUT)
            except subprocess.TimeoutExpired:
                p.kill()
                p.communicate()
                raise SkillError(
                    errors.TIMEOUT,
                    f"Meshing did not finish within {MESH_TIMEOUT:.0f} s",
                    hint="Use a larger 'mesh_size', or remove tiny features (small fillets, text) from the analysed part.",
                ) from None
            text = err.decode("utf-8", "replace")
            text = text.replace(
                "Warning : Unknown element type for UNV export (MSH type 15) - output file might be invalid", ""
            )
            self.exit_code = p.returncode
            return "".join(s for s in text.splitlines(True) if s.strip("\r\n"))

        def create_mesh(self) -> Optional[str]:
            """prepare -> our Gmsh run -> read the mesh. Returns an error text, or None on success."""
            import os

            self.prepare()
            log = self.run_gmsh_with_geo()
            if (
                getattr(self, "exit_code", 1) != 0
                or not os.path.isfile(self.temp_file_mesh)
                or os.path.getsize(self.temp_file_mesh) == 0
            ):
                return log or f"Gmsh exited with code {getattr(self, 'exit_code', '?')} and wrote no mesh"
            self.update_properties()
            return None

    return SafeGmsh


SOLVE_TIMEOUT = 300.0  # s


def _safe_ccx_class() -> Any:
    """FemToolsCcx that runs CalculiX single-threaded and with a timeout.

    With its default preference FreeCAD sets OMP_NUM_THREADS to *all* CPU cores. In
    testing, multithreaded CalculiX returned wrong results on identical input about one
    run in 15 (deflection 5-60 % off, stress spikes of 10^4-10^5 MPa) while equilibrium
    still held, so no output check could catch it. Single-threaded runs were always correct.
    """
    import subprocess

    from femtools import ccxtools

    class SafeCcx(ccxtools.FemToolsCcx):  # type: ignore[misc]
        def start_ccx(self) -> int:
            self.ccx_stdout = ""
            self.ccx_stderr = ""
            # Single-threaded, set by name on this (one-request) FreeCAD process, which the solver inherits.
            for name in ("OMP_NUM_THREADS", "CCX_NPROC_EQUATION_SOLVER", "CCX_NPROC_STIFFNESS", "CCX_NPROC_RESULTS"):
                os.environ[name] = "1"
            folder, base = os.path.split(self.inp_file_name)
            base = os.path.splitext(base)[0]
            p = subprocess.Popen(
                [self.ccx_binary, "-i", base],
                cwd=folder or None,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            try:
                out, err = p.communicate(timeout=SOLVE_TIMEOUT)
            except subprocess.TimeoutExpired:
                p.kill()
                p.communicate()
                raise SkillError(
                    errors.TIMEOUT,
                    f"CalculiX did not finish within {SOLVE_TIMEOUT:.0f} s",
                    hint="Use a larger 'mesh_size' (fewer elements).",
                ) from None
            self.ccx_stdout, self.ccx_stderr = out.decode("utf-8", "replace"), err.decode("utf-8", "replace")
            return p.returncode

    return SafeCcx


def _quantity(text: Any, kind: str, where: str) -> float:
    """'500 N' -> 500.0 (N); '2 MPa' -> 2.0 (MPa). Bare numbers are rejected (FreeCAD would read mN)."""
    unit = {"force": "N", "pressure": "MPa"}[kind]
    if not isinstance(text, str):
        raise SkillError(
            errors.INVALID_PARAM,
            f"{where}: give a {kind} with units, e.g. '500 {unit}'",
            hint="Bare numbers are ambiguous (FreeCAD reads them in mN for forces).",
        )
    try:
        q = App.Units.Quantity(text)
        return float(q.getValueAs(unit))
    except Exception:
        raise SkillError(
            errors.INVALID_PARAM, f"{where}: {text!r} is not a valid {kind} (e.g. '500 {unit}', '2 kN', '0.5 MPa')"
        ) from None


def _faces(shape: Any, selector: Any, where: str) -> List[int]:
    idx = geometry.select_faces(shape, selector)
    if not idx:
        raise SkillError(
            errors.INVALID_SELECTOR,
            f"{where}: selector {selector!r} matches no face",
            hint="Use inspect with topology=true on the target to see its faces.",
        )
    return idx


def _solve(
    ctx: Context,
    target: Any,
    mat: Tuple[float, float, float, float],
    fixed: List[int],
    loads: List[Dict[str, Any]],
    h: float,
    workdir: str,
    keep: bool,
    tag: str,
) -> Dict[str, Any]:
    import ObjectsFem

    GmshTools = _safe_gmsh_class()

    doc = ctx.doc
    created: List[Any] = []

    def add(obj: Any) -> Any:
        created.append(obj)
        return obj

    try:
        an = add(ObjectsFem.makeAnalysis(doc, f"FEM_{target.Name}{tag}"))
        sol = add(ObjectsFem.makeSolverCalculiXCcxTools(doc, f"{an.Name}_Solver"))
        an.addObject(sol)
        m = add(ObjectsFem.makeMaterialSolid(doc, f"{an.Name}_Material"))
        props = m.Material
        props.update(
            {
                "Name": "material",
                "YoungsModulus": f"{mat[0]} MPa",
                "PoissonRatio": str(mat[1]),
                "Density": f"{mat[2]} kg/m^3",
            }
        )
        m.Material = props
        an.addObject(m)
        fx = add(ObjectsFem.makeConstraintFixed(doc, f"{an.Name}_Fixed"))
        fx.References = [(target, [f"Face{i}" for i in fixed])]
        an.addObject(fx)
        for k, ld in enumerate(loads):
            refs = [(target, [f"Face{i}" for i in ld["faces"]])]
            if "force" in ld:
                d = App.Vector(*ld["direction"]).normalize()
                line = add(doc.addObject("Part::Line", f"{an.Name}_Dir{k + 1}"))
                line.X1 = line.Y1 = line.Z1 = 0
                line.X2, line.Y2, line.Z2 = d.x, d.y, d.z
                # The line must exist before the constraint reads it: assigning Direction to a
                # not-yet-recomputed line gave random load directions (~1 run in 8).
                line.recompute()
                c = add(ObjectsFem.makeConstraintForce(doc, f"{an.Name}_Force{k + 1}"))
                c.References = refs
                c.Force = App.Units.Quantity(f"{ld['force']} N")
                c.Direction = (line, ["Edge1"])
                c.Reversed = False
                c.recompute()
                got = App.Vector(c.DirectionVector)
                if got.Length < 1e-9 or abs(abs(got.normalize().dot(d)) - 1) > 1e-6:
                    raise SkillError(errors.INTERNAL, f"Force direction was not applied (got {geometry.vec(got)})")
                if got.normalize().dot(d) < 0:
                    c.Reversed = True
                    c.recompute()
                ctx.own_helper(c, line)
            else:
                c = add(ObjectsFem.makeConstraintPressure(doc, f"{an.Name}_Pressure{k + 1}"))
                c.References = refs
                c.Pressure = App.Units.Quantity(f"{ld['pressure']} MPa")
                c.Reversed = False  # pushes into the faces
            an.addObject(c)
        mesh = add(ObjectsFem.makeMeshGmsh(doc, f"{an.Name}_Mesh"))
        mesh.Shape = target
        mesh.ElementOrder = "2nd"
        mesh.CharacteristicLengthMax = h
        mesh.CharacteristicLengthMin = 0
        an.addObject(mesh)
        doc.recompute()
        err = None
        retried = False
        for _attempt in range(3):
            # Gmsh occasionally returns an empty mesh without an error (seen ~1 in 15 runs),
            # so check the result, and that elements really are quadratic (10-node tetrahedra):
            # linear ones are ~20-40 % too stiff in bending.
            err = GmshTools(mesh).create_mesh()
            vols = list(mesh.FemMesh.Volumes)
            if not err and vols and len(mesh.FemMesh.getElementNodes(vols[0])) == 10:
                break
            retried = True
            mesh.ElementOrder = "2nd"
        vols = list(mesh.FemMesh.Volumes)
        if err or not vols:
            raise SkillError(
                errors.RECOMPUTE_FAILED,
                f"Meshing failed: {str(err)[:300] or 'empty mesh'}",
                hint="Gmsh must be installed (conda: 'gmsh'); try a larger mesh size, or simplify tiny features.",
            )
        if len(mesh.FemMesh.getElementNodes(vols[0])) != 10:
            raise SkillError(
                errors.RECOMPUTE_FAILED,
                "Gmsh did not produce 2nd-order elements; results would be too stiff",
                hint="Retry; if it persists, check the Gmsh installation.",
            )
        fea = _safe_ccx_class()(an, sol)
        fea.purge_results()
        fea.update_objects()
        fea.setup_working_dir(workdir)
        msg = fea.check_prerequisites()
        if msg:
            raise SkillError(
                errors.UNSUPPORTED,
                f"CalculiX cannot run: {msg.strip()[:300]}",
                hint="Install CalculiX (conda: 'calculix'; it ships with the FreeCAD snap and installers).",
            )
        fea.write_inp_file()
        fea.ccx_run()
        fea.load_results()
        res = [o for o in an.Group if o.isDerivedFrom("Fem::FemResultObject")]
        if not res:
            raise SkillError(
                errors.RECOMPUTE_FAILED,
                "CalculiX produced no results",
                hint="The part may be insufficiently fixed (free to move or rotate); fix more faces.",
            )
        r = res[0]
        created.append(r)
        nodes = mesh.FemMesh.Nodes
        coords = [nodes[n] for n in r.NodeNumbers]
        i_d = max(range(len(r.DisplacementLengths)), key=lambda i: r.DisplacementLengths[i])
        i_s = max(range(len(r.vonMises)), key=lambda i: r.vonMises[i])
        reaction = None
        dat = glob.glob(os.path.join(workdir, "*.dat"))
        if dat:
            toks = open(dat[0]).read().split()
            name = fx.Name.upper()
            for j, t in enumerate(toks):
                if t == name and j + 6 < len(toks):
                    try:
                        reaction = [float(toks[j + 4]), float(toks[j + 5]), float(toks[j + 6])]
                    except ValueError:
                        pass
        out = {
            "mesh_retried": retried,
            "nodes": mesh.FemMesh.NodeCount,
            "max_displacement": max(r.DisplacementLengths),
            "max_displacement_at": geometry.vec(coords[i_d], 3),
            "max_von_mises": max(r.vonMises),
            "max_stress_at": geometry.vec(coords[i_s], 3),
            "reaction": reaction,
            "_field": _surface_field(mesh, target, r),
        }
        return out
    finally:
        if not keep:
            for o in reversed(created):
                try:
                    if doc.getObject(o.Name) is not None:
                        doc.removeObject(o.Name)
                except Exception:
                    pass


def _surface_field(mesh: Any, target: Any, r: Any) -> Any:
    """Surface triangles of the FEM mesh (corner nodes) and von Mises stress per node."""
    fm = mesh.FemMesh
    stress = dict(zip(r.NodeNumbers, r.vonMises))
    ids: Dict[int, int] = {}
    pts: List[Tuple[float, float, float]] = []
    vals: List[float] = []
    tris: List[Tuple[int, int, int]] = []
    for face in target.Shape.Faces:
        for fid in fm.getFacesByFace(face):
            corner = fm.getElementNodes(fid)[:3]
            tri = []
            for n in corner:
                if n not in ids:
                    ids[n] = len(pts)
                    p = fm.Nodes[n]
                    pts.append((p.x, p.y, p.z))
                    vals.append(stress.get(n, 0.0))
                tri.append(ids[n])
            tris.append(tuple(tri))
    return pts, tris, vals


def _check_equilibrium(
    res: Dict[str, Any], applied: List[float], shape: Any, loads: List[Dict[str, Any]], fixed: List[int], which: str
) -> None:
    """Reject a solve whose reactions do not balance the applied loads."""
    r = res.get("reaction")
    if r is None:
        return
    mag = math.sqrt(sum(x * x for x in applied)) or 1.0
    eq = math.sqrt(sum((a + b) ** 2 for a, b in zip(applied, r))) / mag
    limit = 0.08 if any(_faces_touch(shape, ld["faces"], fixed) for ld in loads) else 0.02
    if eq > limit:
        raise SkillError(
            errors.RECOMPUTE_FAILED,
            f"The {which} FEM solve failed its equilibrium check ({eq:.1%} off); no results are reported",
            hint="Re-run; if it persists, check the loads and fixed faces.",
            details={
                "reaction_n": [geometry.num(x, 3) for x in r],
                "applied_load_n": [geometry.num(x, 3) for x in applied],
            },
        )


def _faces_touch(shape: Any, a: List[int], b: List[int]) -> bool:
    edges_a = [e for i in a for e in shape.Faces[i - 1].Edges]
    return any(e.isSame(x) for i in b for x in shape.Faces[i - 1].Edges for e in edges_a)


def _applied(target: Any, loads: List[Dict[str, Any]]) -> List[float]:
    total = App.Vector(0, 0, 0)
    for ld in loads:
        if "force" in ld:
            total += App.Vector(*ld["direction"]).normalize() * ld["force"]
        else:
            for i in ld["faces"]:
                f = target.Shape.Faces[i - 1]
                u0, u1, v0, v1 = f.ParameterRange
                if type(f.Surface).__name__ != "Plane":
                    raise SkillError(
                        errors.UNSUPPORTED,
                        "Pressure on curved faces is not supported for the equilibrium check",
                        hint="Apply pressure to planar faces, or use a force.",
                    )
                total += f.normalAt((u0 + u1) / 2, (v0 + v1) / 2) * (-ld["pressure"] * f.Area)  # pushes into the face
    return [total.x, total.y, total.z]


def _report_png(ctx: Context, target: Any, field: Any, dest: Any, vmax: float) -> Dict[str, Any]:
    import numpy as np

    from . import render

    pts = np.array(field[0], float)
    tris = np.array(field[1], int).reshape(-1, 3)
    vals = np.array(field[2], float)
    a, b, c = pts[tris[:, 0]], pts[tris[:, 1]], pts[tris[:, 2]]
    nrm = np.cross(b - a, c - a)
    nrm /= np.maximum(np.linalg.norm(nrm, axis=1, keepdims=True), 1e-12)
    _p, _t, _n, edges, deflection, _vn, _rgb = render._mesh(np, [target])  # model edges drawn on top
    t = np.clip(vals / (vmax or 1.0), 0, 1)
    stops = np.array([[0.1, 0.2, 0.9], [0.0, 0.8, 0.9], [0.1, 0.8, 0.2], [0.95, 0.85, 0.1], [0.9, 0.1, 0.1]])
    pos = t * (len(stops) - 1)
    lo = np.floor(pos).astype(int).clip(0, len(stops) - 2)
    frac = (pos - lo)[:, None]
    vrgb = stops[lo] * (1 - frac) + stops[lo + 1] * frac  # blue -> cyan -> green -> yellow -> red
    size = 400
    bases = [render._basis(np, v) for v in ("iso", "front", "top", "right")]
    extent = max(float(np.ptp(pts @ R[:2].T, axis=0).max()) for R in bases) or 1.0
    scale = 0.86 * size / extent
    tiles = []
    for R in bases:
        light = R[2] * 0.8 + R[1] * 0.45 + R[0] * -0.3
        light /= np.linalg.norm(light)
        tiles.append(render._raster(np, pts, tris, nrm, edges, R, scale, size, light, deflection, vertex_rgb=vrgb))
    sheet = np.full((2 * size + 2, 2 * size + 2, 3), 180, np.uint8)
    for k, tile in enumerate(tiles):
        r, cc = divmod(k, 2)
        sheet[r * (size + 2) : r * (size + 2) + size, cc * (size + 2) : cc * (size + 2) + size] = tile
    tmp = dest.with_name(f".{dest.stem}.fcskill-tmp.png")
    dest.parent.mkdir(parents=True, exist_ok=True)
    render._png(str(tmp), sheet)
    rec = {
        "file": workspace.relative(ctx.root, dest),
        "format": "png",
        "legend": f"von Mises stress, blue 0 MPa -> red {geometry.num(vmax, 1)} MPa; views iso, front, top, right",
    }
    ctx.pending_exports.append({"tmp": tmp, "dest": dest, "record": rec})
    return rec


def _material(target: Any, name: Optional[str]) -> Tuple[str, Tuple[float, float, float, float]]:
    """(preset name, (E MPa, Poisson, density kg/m3, yield MPa)) from 'material', else the part's own material."""
    import json

    from ..document import APPEARANCE_PROP

    source = "'material'"
    if name is None:
        raw = getattr(target, APPEARANCE_PROP, "") if APPEARANCE_PROP in target.PropertiesList else ""
        name = (json.loads(raw).get("material") if raw else None) or None
        source = f"the material assigned to '{target.Name}'"
        if name is None:
            raise SkillError(
                errors.INVALID_PARAM,
                f"'{target.Name}' has no material: give 'material', or assign one with the 'material' op",
                hint=f"Materials with strength data: {matdata.structural_names()}.",
            )
    key = matdata.canonical(name)
    preset = matdata.PRESETS.get(key) if key else None
    if preset is None or not preset.structural:
        why = "is a generic material without a defined yield strength" if preset is not None else "is not known"
        raise SkillError(
            errors.INVALID_PARAM,
            f"{source} ('{name}') {why}; a stress analysis needs a specific grade",
            hint=f"Use one of {matdata.structural_names()}.",
        )
    return key, (preset.youngs_mpa, preset.poisson, preset.density * 1000.0, preset.yield_mpa)


def fem_static(ctx: Context, p: Dict[str, Any]) -> Dict[str, Any]:
    target = ctx.get(p["target"])
    shape = target.Shape
    if shape.isNull() or len(shape.Solids) != 1:
        raise SkillError(
            errors.INVALID_PARAM,
            f"'{target.Name}' must be exactly one solid for FEM (it has {len(shape.Solids)})",
            hint="Fuse touching parts into one solid, or analyse each part separately.",
        )
    mat_name, mat = _material(target, p.get("material"))
    fixed = _faces(shape, p["fixed"], "fixed")
    loads = []
    for k, ld in enumerate(p["loads"]):
        faces = _faces(shape, ld["faces"], f"loads[{k}]")
        if set(faces) & set(fixed):
            raise SkillError(
                errors.INVALID_PARAM, f"loads[{k}] is applied to a fixed face", hint="Load and fixed faces must differ."
            )
        if "force" in ld:
            loads.append(
                {
                    "faces": faces,
                    "force": _quantity(ld["force"], "force", f"loads[{k}].force"),
                    "direction": ld["direction"],
                }
            )
        else:
            loads.append({"faces": faces, "pressure": _quantity(ld["pressure"], "pressure", f"loads[{k}].pressure")})
    bb = geometry.tight_bbox(shape)
    # Typical wall thickness ~ 2 V / A (exact for thin plates); bbox extents overestimate it for L- or U-shapes.
    wall = 2.0 * shape.Volume / shape.Area if shape.Area > 0 else min(bb.XLength, bb.YLength, bb.ZLength)
    h = float(p["mesh_size"]) if p.get("mesh_size") else max(wall / 1.2, bb.DiagonalLength / 50.0)
    h_fine = h
    work = tempfile.mkdtemp(prefix="fcskill-fem-")
    try:
        for sub_dir in ("a", "b", "c"):
            os.makedirs(os.path.join(work, sub_dir), exist_ok=True)
        first = _solve(ctx, target, mat, fixed, loads, h, os.path.join(work, "a"), keep=False, tag="_coarse")
        _check_equilibrium(first, _applied(target, loads), shape, loads, fixed, "coarse")
        final = first
        conv: Optional[Dict[str, Any]] = None
        if p["convergence"]:
            # The refined mesh must really be finer: Gmsh may ignore a size limit the geometry already satisfies.
            h_fine = h * 0.7
            refined = False
            for attempt in range(3):
                d = os.path.join(work, f"b{attempt}")
                os.makedirs(d, exist_ok=True)
                final = _solve(ctx, target, mat, fixed, loads, h_fine, d, keep=False, tag=f"_fine{attempt}")
                refined = final["nodes"] > first["nodes"] * 1.3
                if refined:
                    break
                h_fine *= 0.7
            if p["keep"]:
                final = _solve(ctx, target, mat, fixed, loads, h_fine, os.path.join(work, "c"), keep=True, tag="")
            dd = abs(final["max_displacement"] - first["max_displacement"]) / max(final["max_displacement"], 1e-12)
            ds = abs(final["max_von_mises"] - first["max_von_mises"]) / max(final["max_von_mises"], 1e-12)
            conv = {
                "mesh_sizes": [geometry.num(h, 3), geometry.num(h_fine, 3)],
                "nodes": [first["nodes"], final["nodes"]],
                "displacement_change": geometry.num(dd, 4),
                "stress_change": geometry.num(ds, 4),
                "refined": refined,
            }
            if not refined:
                # Two nearly identical meshes always agree, so their comparison proves nothing.
                ctx.warn(
                    "NO_CONVERGENCE_CHECK",
                    f"the mesh could not be refined enough to check convergence ({first['nodes']} -> "
                    f"{final['nodes']} nodes): the result is unverified; give a smaller 'mesh_size'",
                )
            elif dd > 0.05:
                ctx.warn(
                    "NOT_CONVERGED",
                    f"max displacement changed {dd:.1%} when refining the mesh; give a smaller 'mesh_size'",
                )
            if refined and ds > 0.15:
                ctx.warn(
                    "STRESS_CONCENTRATION",
                    f"max stress changed {ds:.1%} when refining the mesh: it is probably at a sharp "
                    "inner corner, where linear FEM stress grows without limit. Add a fillet there, or judge stress away from it.",
                )
        elif p["keep"]:
            final = _solve(ctx, target, mat, fixed, loads, h, os.path.join(work, "c"), keep=True, tag="")
    finally:
        shutil.rmtree(work, ignore_errors=True)

    applied = _applied(target, loads)
    data: Dict[str, Any] = {
        "material": mat_name,
        "youngs_modulus_mpa": mat[0],
        "yield_mpa": mat[3],
        "mesh": {
            "size": geometry.num(h_fine if p["convergence"] else h, 3),
            "nodes": final["nodes"],
            "element_order": 2,
        },
        "max_displacement_mm": geometry.num(final["max_displacement"], 5),
        "max_displacement_at": final["max_displacement_at"],
        "max_von_mises_mpa": geometry.num(final["max_von_mises"], 3),
        "max_stress_at": final["max_stress_at"],
        "safety_factor": geometry.num(mat[3] / final["max_von_mises"], 3) if final["max_von_mises"] > 0 else None,
        "applied_load_n": [geometry.num(x, 3) for x in applied],
        "disclaimer": DISCLAIMER,
    }
    # Each check is "passed", "failed" or "unavailable"/"skipped", so nothing passes unverified. A failed
    # equilibrium check is an error; a failed convergence check comes with NOT_CONVERGED or STRESS_CONCENTRATION.
    if conv is None:
        conv_status = "skipped"
    elif not conv["refined"]:
        conv_status = "unavailable"
    elif conv["displacement_change"] > 0.05 or conv["stress_change"] > 0.15:
        conv_status = "failed"
    else:
        conv_status = "passed"
    data["checks"] = {
        "equilibrium": "passed" if final["reaction"] is not None else "unavailable",
        "convergence": conv_status,
    }
    if final["reaction"] is not None:
        r = final["reaction"]
        data["reaction_n"] = [geometry.num(x, 3) for x in r]
        mag = math.sqrt(sum(x * x for x in applied)) or 1.0
        eq = math.sqrt(sum((a + b) ** 2 for a, b in zip(applied, r))) / mag
        data["equilibrium_error"] = geometry.num(eq, 5)
        # Load applied on nodes shared with fixed faces is counted as reaction by CalculiX, so
        # loads on faces adjoining the fixed faces legitimately show a few percent.
        adjoining = any(_faces_touch(shape, ld["faces"], fixed) for ld in loads)
        limit = 0.08 if adjoining else 0.02
        if adjoining:
            data["equilibrium_note"] = "loaded faces touch fixed faces: part of the load acts directly on the supports"
        if eq > limit:
            raise SkillError(
                errors.RECOMPUTE_FAILED,
                f"The FEM result failed its equilibrium check: reactions {data['reaction_n']} N do not balance "
                f"the applied loads {data['applied_load_n']} N ({eq:.1%} off); no results are reported",
                hint="Check that loads and fixed faces are what you intend; if they are, re-run (meshing can fail silently).",
                details={"equilibrium_error": geometry.num(eq, 5)},
            )
    else:
        ctx.warn(
            "NO_EQUILIBRIUM_CHECK",
            "CalculiX reported no reaction forces, so the result could not be checked for equilibrium: "
            "treat it as unverified",
        )
    if conv:
        data["convergence"] = conv
    else:
        ctx.warn(
            "NO_CONVERGENCE_CHECK",
            "'convergence' is off, so mesh convergence was not checked: the stresses may depend on the mesh size",
        )
    if final["max_displacement"] > 0.05 * bb.DiagonalLength:
        ctx.warn(
            "LARGE_DEFORMATION",
            "displacement exceeds 5% of the part size: the linear small-deformation result is not reliable",
        )
    if p.get("report"):
        dest = workspace.resolve(ctx.root, p["report"])
        if dest.suffix.lower() != ".png":
            raise SkillError(errors.INVALID_PARAM, "'report' must be a .png filename")
        data["report"] = _report_png(ctx, target, final["_field"], dest, final["max_von_mises"])["file"]
    req = p.get("require") or {}
    failures = []
    if "min_safety_factor" in req and (data["safety_factor"] or 0) < req["min_safety_factor"]:
        failures.append(
            {"check": "min_safety_factor", "expected": req["min_safety_factor"], "actual": data["safety_factor"]}
        )
    if "max_displacement" in req and data["max_displacement_mm"] > req["max_displacement"]:
        failures.append(
            {"check": "max_displacement", "expected": req["max_displacement"], "actual": data["max_displacement_mm"]}
        )
    if failures:
        raise SkillError(
            errors.EXPECTATION_FAILED,
            f"{len(failures)} requirement(s) not met",
            hint="Make the part stiffer or stronger: thicker sections, ribs, fillets at stressed corners, or another material.",
            details={"failures": failures, "result": {k: v for k, v in data.items() if k != "disclaimer"}},
        )
    if first.get("mesh_retried") or final.get("mesh_retried"):
        data["mesh_retried"] = True
    if p["keep"]:
        ctx.mutated = True
    return {"data": data}


HANDLERS = {"fem_static": fem_static}
