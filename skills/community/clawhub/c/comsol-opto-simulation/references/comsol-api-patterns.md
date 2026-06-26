# COMSOL API Patterns via MPh

This document records common MPh/COMSOL Java API patterns used in the optoelectronic simulation skill.

## 1. Starting a Client

```python
import mph
client = mph.start()           # Start local COMSOL client
# client = mph.start(cores=4)  # Multi-core
```

## 2. Model Lifecycle

```python
# Create new model
model = client.create('my_model')

# Load existing
model = client.load('path/to/model.mph')

# Save
model.save()                   # Overwrite original
model.save('new_path.mph')     # Save as new file
```

## 3. Accessing the Java Model Object

```python
jm = model.java  # NOT model.java()
```

All COMSOL API calls go through `jm` (the Java ModelUtil object).

## 4. Geometry Creation (2D)

```python
comp = jm.component().create('comp1', True)
geom = comp.geom().create('geom1', 2)

# Rectangle
rect = geom.feature().create('r1', 'Rectangle')
rect.set('size', ['1000[nm]', '100[nm]'])
rect.set('pos', ['0[nm]', '0[nm]'])

# Circle
circ = geom.feature().create('c1', 'Circle')
circ.set('r', '50[nm]')
circ.set('pos', ['500[nm]', '50[nm]'])

# Boolean difference
bool_diff = geom.feature().create('bd1', 'Difference')
bool_diff.selection('input').set(['r1'])
bool_diff.selection('input2').set(['c1'])

# Build
geom.run()
```

## 5. Physics: Electromagnetic Waves

```python
emw = comp.physics().create('emw', 'ElectromagneticWavesFrequencyDomain', 'geom1')

# Wave Equation (default)
# No need to explicitly create; it's added automatically

# Boundary conditions
# Perfect Electric Conductor (PEC) - for metals
pec = emw.create('pec1', 'PEC')
pec.selection().set([1, 2])  # boundary numbers

# Port (for incident wave)
port = emw.create('port1', 'Port')
port.selection().set([6])    # top boundary
port.set('PortExcitation', 'on')
port.set('Pin', '1[W]')    # or use field amplitude

# Scattering boundary condition (SBC) - for open boundaries
sbc = emw.create('sbc1', 'SBC')
sbc.selection().set([1, 2, 3, 4])
```

## 6. Physics: Semiconductor

```python
semi = comp.physics().create('semi', 'Semiconductor', 'geom1')

# Semiconductor Material Model per domain
mat1 = semi.create('mat1', 'SemiconductorMaterialModel')
mat1.selection().set([1])
# Properties set in the physics node, not the material node

# Doping
# Doping is set via domain properties or separate Doping feature
doping = semi.create('dop1', 'Doping')
doping.selection().set([1])  # domain
doping.set('DopantType', 'Donor')
doping.set('ND', '1e20[1/cm^3]')

# Metal Contact (ohmic)
contact = semi.create('cont1', 'MetalContact')
contact.selection().set([6])  # boundary
contact.set('V0', '0[V]')     # Ground

contact2 = semi.create('cont2', 'MetalContact')
contact2.selection().set([1])  # other boundary
contact2.set('V0', 'V_bias')   # Bias voltage (parameter)

# Recombination: Shockley-Read-Hall
srh = semi.create('srh1', 'SRHRecombination')
srh.selection().set([1, 2, 3])
```

## 7. Materials

```python
mat = comp.material().create('mat1', 'Common')
mat.selection().set([1])
pg = mat.propertyGroup('def')

# Optical: refractive index (n, k)
pg.set('refractiveindex', ['2.3', '0.1'])  # n=2.3, k=0.1

# Semiconductor: permittivity
pg.set('relpermittivity', ['<CONFIGURE_RELATIVE_PERMITTIVITY>'])
```

## 8. Study Setup

```python
study = jm.study().create('std1')

# Stationary (for I-V)
stat = study.feature().create('stat1', 'Stationary')

# Frequency Domain (for optical)
freq = study.feature().create('freq1', 'FrequencyDomain')
freq.set('plist', ['5e14[Hz]', '5.5e14[Hz]', '6e14[Hz]'])  # λ = 600, 545, 500 nm

# Parametric sweep
sweep = stat.create('sweep', 'AuxiliarySweep')
sweep.set('pname', 'V_bias')
sweep.set('plist', ['-1[V]', '-0.5[V]', '0[V]', '0.5[V]', '1[V]'])
```

## 9. Mesh

```python
mesh = comp.mesh().create('mesh1')

# Automatic mesh size
mesh.feature().create('size1', 'Size')
mesh.feature('size1').set('hauto', '4')  # 1=extremely fine, 9=extremely coarse
mesh.run()

# Custom size for semiconductor region
mesh.feature().create('size2', 'Size')
mesh.feature('size2').set('custom', 'on')
mesh.feature('size2').set('hmax', '5[nm]')
mesh.feature('size2').selection().geom('geom1', 2)
mesh.feature('size2').selection().set([2, 3])  # semiconductor layers
```

## 10. Solving

```python
# Synchronous (blocking)
study.run()

# Check solver log
print(model.java.sol('sol1').feature().tags())
```

## 11. Results Evaluation

```python
# Global evaluation (e.g., terminal current)
results = jm.result()
global_eval = results.create('gev1', 'GlobalEval')
global_eval.set('expr', ['semi.I_1'])  # Current at contact 1

# Line graph (band diagram)
line = results.create('pg1', 'PlotGroup1D')
line_graph = line.create('lg1', 'LineGraph')
line_graph.set('expr', 'semi.E_c')  # Conduction band edge

# Export plot
model.export('plot', 'band_diagram.png')

# Export data
data = results.create('data1', 'Data')
data.set('expr', ['semi.E_c', 'semi.E_v', 'semi.E_f'])
# Save to file via Java API or manual extraction
```

## 12. Parameters

```python
# Set global parameters
jm.param().set('V_bias', '0[V]')
jm.param().set('T_ambient', '300[K]')

# List parameters
for p in jm.param().tags():
    print(p, jm.param().get(p))
```

## 13. Important Gotchas

1. **`jm` vs `model`**: `model.java` returns the Java Model object. Use it for all low-level API calls. MPh's `model.parameter()` and `model.solve()` are convenience wrappers.
2. **Selection indices**: COMSOL uses 1-based indexing for domains/boundaries in Java API. Domain 1 is the first created geometry feature.
3. **Units**: Always include units in string values: `'100[nm]'`, `'1e17[1/cm^3]'`. COMSOL handles unit conversion.
4. **Material assignments**: Material selection uses domain numbers. If you boolean-union layers, domain numbering changes. Be careful.
5. **Physics tags**: Physics features are referenced by tag strings (e.g., `'semi'`, `'mat1'`). Keep track of them.
6. **Study order**: If multiple studies exist, `model.solve()` solves the last created unless specified.
7. **Do not guess property keys**: Build a small model in COMSOL Desktop, use `File > Compact History`, then save as `Model file for Java (*.java)` to inspect exact API calls.
8. **Prefer local docs for version-specific behavior**: Run `scripts/discover_comsol_environment.py --pretty`, then open the detected Programming Reference Manual and module manuals.

## 14. MPh Helper Methods

```python
# List model features
print(model.java.component().tags())
print(model.java.physics().tags())
print(model.java.study().tags())

# Clear solution
model.java.sol().clear()

# Reset model history (compact file)
model.clear()
model.reset()
```

## 15. Java Shell and Batch Route

When an API call is uncertain, use the COMSOL Desktop Java Shell on Windows:

```java
model.geom().create("geom1", 2);
model.param().set("V_bias", "1[V]");
```

For repeatable automation:

1. Build a representative model in COMSOL Desktop.
2. Compact history.
3. Save as `Model file for Java (*.java)`.
4. Compile with `<COMSOLROOT>\bin\win64\comsolcompile.exe model.java`.
5. Run through `comsolbatch.exe` or port the stable calls to Python via `model.java`.

Batch runs are preferred for long parameter sweeps because logs preserve solver
progress and memory usage. Use graphics only when exports need plot/image nodes.


