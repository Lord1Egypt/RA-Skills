# Ready-made parts and imported files

Read this before using `import` or the `library` command.

## Ready-made parts (FreeCAD library)

Don't model standard parts that already exist: bearings, stepper motors, fasteners, aluminium profiles,
electronics boards and more come from the official FreeCAD library (github.com/FreeCAD/FreeCAD-library).

```bash
python3 {baseDir}/scripts/fcskill.py library 608 bearing
```

The command returns `matches` with a `part` path and its formats. Import one:

```json
{"op": "import", "library": "Mechanical Parts/Bearings/608ZZ_Ball_Bearing", "name": "Bearing",
 "anchor": "center", "position": [20, 20, 7.5]}
```

- **Placement:** library parts keep their author's orientation. Check the reported `bbox`, use `anchor`
  (`center`, `bottom_center`, `min_corner`) and `rotation`, then cut seats or holes to fit.
- **Shape:** the result is a fixed solid. It can be placed, cut, fused, measured, given a material and added
  to an assembly, but its dimensions can't be edited.
- **Licence:** parts are CC-BY 3.0. Tell the user the `attribution` from the response when you hand over the
  model.
- **Network:** search and first use need network access to GitHub (parts are then cached in the workspace).
  Only anonymous downloads from the FreeCAD library repository are made; nothing about the user or the model
  is sent. With `FCSKILL_OFFLINE=1`, or without network, the command returns `LIBRARY_UNAVAILABLE`.
- **Files:** `{"op": "import", "file": "vendor/motor.step"}` imports any STEP/IGES/BREP/FCStd file in the
  workspace, e.g. a manufacturer's model.
- **Meshes (STL, OBJ, 3MF, PLY, OFF):** `{"op": "import", "file": "scan.stl"}` turns a closed mesh into a solid
  you can cut, fuse, measure and export (e.g. "add a hole to this STL").
  - The solid is made of the mesh's flat triangles. Coplanar ones are merged (`refine`), but curved surfaces
    stay faceted, so fillets on its edges and FEM are unreliable.
  - Open, non-manifold or self-intersecting meshes are refused with `GEOMETRY_INVALID`: ask the user to repair
    the mesh (or for a STEP file). The limit is 20,000 triangles, and booleans on meshes are slow (about
    a minute at the limit): prefer a STEP file when the user has one.
  - Mesh files carry no units. Check the reported `bbox`; `CHECK_UNITS` warns when the size looks like inches
    or metres, which you fix with `scale` (25.4 or 1000).
