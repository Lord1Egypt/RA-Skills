# COMSOL Java API Cheat Sheet for MPh / Python Bridge

Quick reference for common COMSOL Multiphysics Java API patterns used in this skill. All examples assume:

```python
jm = model.java  # Java Model object via mph
comp = jm.component("comp1")
geom = comp.geom("geom1")
```

## Geometry

| Task | Java API | Notes |
|------|----------|-------|
| Create component | `jm.component().create("comp1", True)` | `True` = 3D, `False` = 2D/1D |
| Create geometry | `comp.geom().create("geom1", 2)` | Dimension: 1, 2, or 3 |
| Rectangle | `geom.feature().create("r1", "Rectangle")` | |
| Set size | `rect.set("size", ["1000[nm]", "100[nm]"])` | List of strings with units |
| Set position | `rect.set("pos", ["0[nm]", "0[nm]"])` | |
| Build | `geom.run()` | Required before physics |
| Form Union | `geom.feature().create("fu1", "Union")` | Merges all objects; changes domain indices |
| Selection from feature | `geom.feature("r1").selection()` | Output selection of a geometry feature |
| Selection entities | `sel.entities()` or `sel.globalEntities()` | Returns array of indices |

## Physics

### Electromagnetic Waves

```python
emw = comp.physics().create("emw", "ElectromagneticWavesFrequencyDomain", "geom1")
```

| Feature | Tag | Key Properties |
|---------|-----|----------------|
| Wave Equation | auto-created | |
| PEC | `emw.create("pec1", "PEC")` | `selection().set([boundary_indices])` |
| Port | `emw.create("port1", "Port")` | `"PortExcitation"`, `"Pin"` |
| SBC | `emw.create("sbc1", "Scattering")` | `"ScatteringType"` |

### Semiconductor

```python
semi = comp.physics().create("semi", "Semiconductor", "geom1")
```

| Feature | Tag | Key Properties |
|---------|-----|----------------|
| Material Model | `semi.create("mat1", "SemiconductorMaterialModel")` | `selection().set([domain])` |
| Set bandgap | `mm.set("Eg0", "0.41[eV]")` | Varshhi: use expression with `T` |
| Set affinity | `mm.set("Chi0", "4.7[eV]")` | |
| Electron mobility | `mm.set("mun0", "500[cm^2/(V*s)]")` | COMSOL uses SI internally |
| Hole mobility | `mm.set("mup0", "200[cm^2/(V*s)]")` | |
| Effective DOS | `mm.set("Nc0", "1e19[1/cm^3]")` | |
| Permittivity | `mm.set("epsilonr", "17")` | Relative, dimensionless |
| Doping (Donor) | `semi.create("dop1", "Doping")` | `"DopantType"`, `"ND"` |
| Doping (Acceptor) | `semi.create("dop2", "Doping")` | `"DopantType"`, `"NA"` |
| SRH Recombination | `semi.create("srh1", "SRHRecombination")` | `"taun"`, `"taup"` |
| Metal Contact | `semi.create("c1", "MetalContact")` | `"V0"`, `"ContactType"` |
| Heterojunction | `semi.create("hj1", "HeterojunctionBoundaryCondition")` | Only needed for explicit band offset |

### Heat Transfer

```python
ht = comp.physics().create("ht", "HeatTransfer", "geom1")
```

| Feature | Tag | Key Properties |
|---------|-----|----------------|
| Solid | `ht.create("solid1", "SolidHeatTransferModel")` | `"k"`, `"rho"`, `"Cp"` |
| Convection | `ht.create("conv1", "ConvectiveHeatFlux")` | `"h"`, `"T_inf"` |
| Temperature BC | `ht.create("temp1", "Temperature")` | `"T0"` |
| Heat Source | `ht.create("q1", "HeatSource")` | `"Qh"` |
| Symmetry | `ht.create("sym1", "SymmetryHeatFlux")` | |

## Materials

```python
mat = comp.material().create("mat1", "Common")
mat.selection().set([domain_index])
pg = mat.propertyGroup("def")
```

| Property | Set Call | Unit Hint |
|----------|----------|-----------|
| Refractive index (n,k) | `pg.set("refractiveindex", ["2.3", "0.1"])` | Complex as [real, imag] |
| Relative permittivity | `pg.set("relpermittivity", ["22"])` | Array even for scalar |
| Thermal conductivity | `pg.set("thermalconductivity", ["2.0"])` | W/m/K |
| Density | `pg.set("density", ["7600"])` | kg/m³ |
| Heat capacity | `pg.set("heatcapacity", ["210"])` | J/kg/K |

## Studies

```python
study = jm.study().create("std1")
```

| Step | Creation | Key Properties |
|------|----------|----------------|
| Stationary | `study.feature().create("stat1", "Stationary")` | |
| Frequency Domain | `study.feature().create("freq1", "FrequencyDomain")` | `"plist"` |
| Auxiliary Sweep | `stat.create("sweep", "AuxiliarySweep")` | `"pname"`, `"plist"` |
| Time Dependent | `study.feature().create("time1", "TimeDependent")` | `"tlist"` |

### Parameter Strings

```python
jm.param().set("V_bias", "0[V]")
# Sweep list (comma-separated, each with unit)
sweep.set("plist", "-1[V],0[V],0.5[V],1[V]")
# Or with expression
jm.param().set("T_ambient", "300[K]")
```

## Mesh

```python
mesh = comp.mesh().create("mesh1")
```

| Control | Creation | Key Properties |
|---------|----------|----------------|
| Auto size | `mesh.feature().create("size1", "Size")` | `"hauto"`: 1=extremely fine, 9=extremely coarse |
| Custom max size | `mesh.feature().create("size2", "Size")` | `"custom"`: "on", `"hmax"`: "5[nm]" |
| Domain-specific | size selection via `.selection().geom("geom1", 2)` then `.set(domains)` | |
| Build | `mesh.run()` | |

## Solvers

Access solver node (advanced):

```python
sol = jm.sol("sol1")  # or create via study
solver_seq = sol.feature()
# Switch linear solver
solver_seq.create("d1", "Direct")
solver_seq.create("i1", "Iterative")
```

| Solver | Tag | Notes |
|--------|-----|-------|
| Direct (MUMPS) | `"Direct"` + `feature.set("linsolver", "mumps")` | Default for small/medium |
| Direct (PARDISO) | `"Direct"` + `feature.set("linsolver", "pardiso")` | Faster, more memory |
| Iterative (GMRES) | `"Iterative"` + `feature.set("linsolver", "gmres")` | Good for large DOF |
| Preconditioner ILU | `"ILU"` | Default |
| Preconditioner Multigrid | `"Multigrid"` | Best for 3D/thermal |

## Results / Evaluation

```python
results = jm.result()
```

| Task | Creation / Access | Expression |
|------|------------------|------------|
| Global evaluation | `results.create("gev1", "GlobalEval")` | `"semi.I_1"` (terminal current) |
| 1D Plot group | `results.create("pg1", "PlotGroup1D")` | |
| Line graph | `pg.create("lg1", "LineGraph")` | `"semi.E_c"`, `"semi.E_v"`, `"semi.E_f"` |
| 2D Plot group | `results.create("pg2", "PlotGroup2D")` | |
| Surface plot | `pg2.create("surf1", "Surface")` | `"T"` (temperature) |
| Export plot | `model.export("image1", "path.png")` | |

### Common COMSOL Variables

| Variable | Meaning | Module |
|----------|---------|--------|
| `semi.I_1` | Terminal current at contact 1 | Semiconductor |
| `semi.E_c` | Conduction band edge energy | Semiconductor |
| `semi.E_v` | Valence band edge energy | Semiconductor |
| `semi.E_f` | Fermi level / quasi-Fermi level | Semiconductor |
| `semi.n` | Electron concentration | Semiconductor |
| `semi.p` | Hole concentration | Semiconductor |
| `semi.Qj` | Joule heating density | Semiconductor |
| `emw.Qh` | Electromagnetic loss density | EM Waves |
| `emw.normE` | Electric field norm | EM Waves |
| `ht.T` | Temperature | Heat Transfer |
| `ht.Qh` | Total heat source | Heat Transfer |

## Selection Indexing

**Critical: COMSOL Java API uses 1-based indexing for domains, boundaries, edges, and points.**

| Object | Index Base | Example |
|--------|-----------|---------|
| Domain | 1-based | `mm.selection().set([2])` selects domain #2 |
| Boundary | 1-based | `contact.selection().set([6])` selects boundary #6 |
| Edge (1D/2D) | 1-based | |
| Point | 1-based | |

**After `FormUnion` / `FormAssembly`:**
- Domain count may be less than feature count (merged overlapping regions)
- Boundary count changes (shared interfaces become internal, not external)
- **Always verify with mapping.json or GUI before trusting hard-coded indices**

## Common Pitfalls

1. **Units in strings**: Always include units: `"100[nm]"`, `"1e17[1/cm^3]"`, `"300[K]"`. COMSOL parses and converts.
2. **Missing `geom.run()`**: Physics features created before `geom.run()` may throw "geometry not built".
3. **Selection before domain exists**: Cannot assign `mat.selection().set([2])` if domain 2 does not exist yet.
4. **Study mismatch**: `study.run()` solves the *last* created study unless specified. Use `model.solve("std1")` for explicit control.
5. **Solution clearing**: Re-running a study without `model.java.sol().clear()` may append solutions rather than overwrite.
6. **MPh vs. Java API**: `model.parameter("V_bias")` is MPh convenience; `jm.param().set("V_bias", "1[V]")` is Java API. Both work, but Java API is more complete.
7. **Feature tag uniqueness**: Cannot create two features with the same tag (e.g., two `"mat1"`). Use incremental tags.

## Debugging Tips

```python
# List all physics features
for tag in comp.physics("semi").feature().tags():
    print(tag)

# List all studies
for tag in jm.study().tags():
    print(tag)

# Check if selection is valid
try:
    mm.selection().set([99])
except Exception as e:
    print(f"Invalid selection: {e}")

# Print current parameter values
for p in jm.param().tags():
    print(p, "=", jm.param().get(p))
```

## Environment and License Checks

Run `python scripts/discover_comsol_environment.py --pretty` before automation
to locate the COMSOL installation, command launchers, local manuals, and bundled
Java runtime.

```python
from com.comsol.model.util import ModelUtil

print(ModelUtil.getComsolVersion())
print(ModelUtil.hasProduct("COMSOL"))
print(ModelUtil.hasProductForFile(r"path\to\device.mph"))
ModelUtil.showProgress(True)
ModelUtil.showPlots(False)
```

Useful Windows launchers live under `<COMSOLROOT>\bin\win64`:

| Command | Use |
|---------|-----|
| `comsoldoc.exe` | Open local COMSOL documentation |
| `comsolmphserver.exe` | Start server for `mph` / Java API clients |
| `comsolbatch.exe` | Run `.mph` or compiled Java class files headlessly |
| `comsolcompile.exe` | Compile model files for Java |
| `comsolmphclient.exe` | Connect a Desktop client to a server |

COMSOL also ships Java tools under
`<COMSOLROOT>\java\win64\jre\bin`: `java.exe`, `javac.exe`, and `jshell.exe`.

## References

- COMSOL Multiphysics Reference Manual, "Java API" chapter
- MPh documentation: https://mph.readthedocs.io
- `references/comsol-docs-java-playbook.md` for local manual paths, official doc links, and Java/batch workflows
- This skill: `references/comsol-api-patterns.md` for detailed walkthroughs
