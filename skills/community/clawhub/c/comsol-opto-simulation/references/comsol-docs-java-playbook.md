# COMSOL Documentation and Java API Playbook

Use this reference when a task needs COMSOL Help, manuals, Java API usage,
Java Shell exploration, model export to Java, or robust `mph`/JPype automation.

## Official documentation map

Prefer COMSOL 6.4 documentation when the installed model version is 6.4. If the
installed COMSOL version differs, switch every `/6.4/` URL below to the matching
version and re-check API names before editing automation code.

| Need | Primary source |
| --- | --- |
| API overview and supported execution routes | https://doc.comsol.com/6.4/doc/com.comsol.help.comsol/comsol_api_intro.46.01.html |
| Running API code from Application Builder, Desktop, batch, or shell | https://doc.comsol.com/6.4/doc/com.comsol.help.comsol/comsol_api_intro.46.02.html |
| Java Shell interactive interpreter | https://doc.comsol.com/6.4/doc/com.comsol.help.comsol/comsol_ref_modeling.19.028.html |
| Full Programming Reference PDF | https://doc.comsol.com/6.4/doc/com.comsol.help.comsol/COMSOL_ProgrammingReferenceManual.pdf |
| Application Programming Guide PDF | https://doc.comsol.com/6.4/doc/com.comsol.help.comsol/ApplicationProgrammingGuide.pdf |
| Java API package docs | https://doc.comsol.com/6.4/doc/com.comsol.help.comsol/api/com/comsol/model/package-summary.html |
| Model object Javadoc | https://doc.comsol.com/6.4/doc/com.comsol.help.comsol/api/com/comsol/model/Model.html |
| ModelUtil API | https://doc.comsol.com/6.4/doc/com.comsol.help.comsol/comsol_api_general.47.15.html |
| Numerical global evaluation API | https://doc.comsol.com/6.4/doc/com.comsol.help.comsol/comsol_api_results.52.066.html |
| Semiconductor Module manual | https://doc.comsol.com/6.4/doc/com.comsol.help.semicond/SemiconductorModuleUsersGuide.pdf |
| Semiconductor heterojunction theory | https://doc.comsol.com/6.4/doc/com.comsol.help.semicond/semicond_ug_semiconductor.6.66.html |
| Semiconductor recombination/generation | https://doc.comsol.com/6.4/doc/com.comsol.help.semicond/semicond_ug_semiconductor.6.59.html |
| Wave Optics EMW frequency-domain interface | https://doc.comsol.com/6.4/doc/com.comsol.help.woptics/woptics_ug_optics.6.02.html |
| Wave Optics Port boundary | https://doc.comsol.com/6.4/doc/com.comsol.help.woptics/woptics_ug_optics.6.20.html |
| Scattering Boundary Condition | https://doc.comsol.com/6.4/doc/com.comsol.help.rf/rf_ug_radio_frequency.07.036.html |

## Local COMSOL and Help discovery

Before assuming COMSOL is unavailable, check all four routes below.

```powershell
# 1) Executables on PATH.
Get-Command comsol, comsolbatch, comsolcompile, java -ErrorAction SilentlyContinue

# 2) Environment variables and common Windows install locations.
$roots = @(
  $env:COMSOL_HOME,
  $env:COMSOL_ROOT,
  "C:\Program Files\COMSOL",
  "C:\Program Files (x86)\COMSOL"
) | Where-Object { $_ -and (Test-Path -LiteralPath $_) }
$roots | ForEach-Object {
  Get-ChildItem -LiteralPath $_ -Recurse -Filter comsol.exe -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -match "\\bin\\win64\\comsol.exe$" }
}

# 3) Windows registry, when accessible.
Get-ChildItem "HKLM:\SOFTWARE\Comsol" -ErrorAction SilentlyContinue |
  ForEach-Object { Get-ItemProperty $_.PSPath } |
  Select-Object PSChildName, COMSOLROOT

# 4) Manuals inside an install tree.
$root = "C:\Program Files\COMSOL\COMSOL64\Multiphysics"
Get-ChildItem -LiteralPath $root -Recurse -Include `
  "*ProgrammingReferenceManual*.pdf", `
  "ApplicationProgrammingGuide.pdf", `
  "SemiconductorModuleUsersGuide.pdf", `
  "WaveOpticsModuleUsersGuide.pdf" `
  -ErrorAction SilentlyContinue
```

The `mph` package included with this skill performs similar discovery. On
Windows it searches the registry and PATH, and on Linux/macOS it checks the
default application folders. If `mph.start()` fails, inspect
`vendor/site-packages/mph/discovery.py` before changing automation code.

For a repeatable JSON report, run:

```powershell
python scripts/discover_comsol_environment.py --pretty
```

That script reports candidate COMSOL roots, command launchers, bundled Java
tools, and whether the key local manuals exist.

### Local manuals worth opening first

| Need | Local manual under `doc/help/wtpwebapps/ROOT/doc` |
| --- | --- |
| Overall modeling, geometry, mesh, solvers, results | `com.comsol.help.comsol/COMSOL_ReferenceManual.pdf` |
| Java API, model files for Java, compile/run workflow | `com.comsol.help.comsol/COMSOL_ProgrammingReferenceManual.pdf` |
| Semiconductor drift-diffusion, contacts, traps, heterojunctions | `com.comsol.help.semicond/SemiconductorModuleUsersGuide.pdf` |
| Optical absorption and wave optics setup | `com.comsol.help.woptics/WaveOpticsModuleUsersGuide.pdf` |
| RF frequency-domain EM wave backup reference | `com.comsol.help.rf/RFModuleUsersGuide.pdf` |
| Thermal coupling and heat sources | `com.comsol.help.heat/HeatTransferModuleUsersGuide.pdf` |
| MATLAB bridge and server access model | `com.comsol.help.llmatlab/LiveLinkForMATLABUsersGuide.pdf` |

### Command-line and Java launchers

COMSOL installs command wrappers under `<COMSOLROOT>/bin/win64` on Windows:

| Command | Use |
| --- | --- |
| `comsoldoc.exe` | Open local COMSOL documentation. |
| `comsolmphserver.exe` | Start a COMSOL server for `mph` or Java API clients. |
| `comsolmphclient.exe` | Connect a Desktop client to a server. |
| `comsolbatch.exe` | Run `.mph` files or compiled Java class files headlessly. |
| `comsolcompile.exe` | Compile model files for Java. |

Prefer COMSOL's bundled Java runtime for COMSOL API work:

```powershell
$COMSOLROOT = "C:\Program Files\COMSOL\COMSOL64\Multiphysics"
& "$COMSOLROOT\java\win64\jre\bin\java.exe" -version
& "$COMSOLROOT\java\win64\jre\bin\javac.exe" -version
& "$COMSOLROOT\java\win64\jre\bin\jshell.exe" --version
```

Always quote COMSOL paths because installation folders commonly contain spaces.

### Useful ModelUtil probes

Use these before expensive jobs or when triaging environment issues:

```python
from com.comsol.model.util import ModelUtil

print(ModelUtil.getComsolVersion())
print(ModelUtil.hasProduct("COMSOL"))
print(ModelUtil.hasProductForFile(r"path\to\device.mph"))
ModelUtil.checkoutLicenseForFile(r"path\to\device.mph")
ModelUtil.showProgress(True)          # or ModelUtil.showProgress("solver.log")
ModelUtil.showPlots(False)
ModelUtil.closeWindows()
ModelUtil.clear()
```

Use `hasProduct(...)` for known module names and `hasProductForFile(...)` or
`checkoutLicenseForFile(...)` when an existing `.mph` file declares the required
products. For headless sweeps, disable plots unless image export is required.

## Java/API execution routes

### 1. Java Shell as the fastest interpreter

Use the Java Shell when COMSOL Desktop is available and the goal is to learn or
debug the exact API call for a GUI action. It is Windows Desktop only.

Workflow:

1. Open COMSOL Desktop, then open the Java Shell from the Windows menu or the
   Developer ribbon.
2. Type commands beginning with `model.` to change the active model tree.
3. Use code completion with `Ctrl+Space`.
4. Use multiline mode for loops or blocks; run multiline input with
   `Ctrl+Enter`.
5. Use Record Code before making a GUI change. Stop recording, then copy the
   generated API calls into the Python/Java automation script.
6. Use Data Viewer to inspect shell variables, model parameters, and values.
7. Save the model if the changes should persist. Java Shell session variables
   are not saved between sessions.

High-value probes:

```java
model.component().tags();
model.component("comp1").geom().tags();
model.component("comp1").physics().tags();
model.study().tags();
model.result().dataset().tags();
model.result().numerical().tags();
model.getUsedProducts();
```

### 2. Model file for Java

Use this route when a GUI-built model should become reproducible source code.
In Desktop, run `File > Compact History` before exporting so the generated Java
is smaller and closer to the final model tree.

```python
import mph
client = mph.start(cores=1)
model = client.load("input.mph")
model.save("input_export.java", format="Java")
```

For native COMSOL commands, compile and run with the matching installation:

```powershell
$bin = "C:\Program Files\COMSOL\COMSOL64\Multiphysics\bin\win64"
& "$bin\comsolcompile.exe" "C:\work\input_export.java"
& "$bin\comsolbatch.exe" -inputfile "C:\work\input_export.class" -outputfile "C:\work\out.mph"
```

Keep Java exports as diagnostic snapshots, not as the only source of truth.
They are verbose, version-specific, and often include GUI/history details.

### 3. Python `mph` plus direct Java object

Use `mph` for batch workflows and use `model.java` when the Python wrapper lacks
a feature. The wrapper is backed by COMSOL `ModelUtil` through JPype.

```python
import mph
client = mph.start(cores=1)
pymodel = client.load("device.mph")
jm = pymodel.java

jm.param().set("V_bias", "0.5[V]")
jm.study("std1").run()

gev = jm.result().numerical().create("gev_auto", "Global")
gev.set("expr", ["semi.I0_1", "maxop1(semi.n)", "maxop1(semi.p)"])
data = gev.getData()  # shape: expression, solution, value
```

JPype can host only one JVM per Python process. For parallel sweeps, use
separate Python processes or COMSOL batch jobs rather than multiple clients in
one interpreter.

## Optoelectronic model guidance from manuals

### Semiconductor heterojunctions

COMSOL handles interior semiconductor boundaries through
`Continuity/Heterojunction`. For configured multi-material interfaces, do not assume a simple
continuity boundary is physically neutral. Choose and document one of:

- `Continuous quasi-Fermi levels`: suitable as a first pass when interface
  resistance is negligible.
- `Thermionic emission`: more appropriate when band offsets create an injection
  barrier or interface transport is rate-limiting.
- WKB tunneling factor: consider only when a thin barrier or strong field makes
  tunneling physically plausible.

For configured heterointerfaces, always report which interface model was
used when interpreting rectification, photocurrent, dark current, or built-in
field trends.

### Generation and recombination

The Semiconductor interface supports additive generation/recombination
features. For any configured device or material stack, map mechanisms explicitly:

| Mechanism | Use in configured simulations |
| --- | --- |
| Optical generation | Couple from EM absorption or use user-defined generation from measured/calculated absorption. |
| Direct recombination | Relevant for direct-gap-like radiative channels; verify coefficient units. |
| Trap-assisted/SRH | Default suspect for dark current, hysteresis, slow response, and interface loss. |
| Trap-assisted heterointerface recombination | Use when TEM or electrical data imply interface defect states. |
| Auger | Reserve for high carrier density/high illumination regimes. |
| Impact ionization | Only for high-field breakdown or gain analysis. |

When debugging performance, connect every COMSOL change to the user's configured
analysis axes, such as band alignment, carrier dynamics, trap states, built-in
field, heat flow, or another project-relevant mechanism.

### EM waves, ports, and boundaries

For optical absorption, prefer the Wave Optics `Electromagnetic Waves,
Frequency Domain` interface (`ewfd`) for time-harmonic fields. Mesh size must
resolve the shortest wavelength in the highest-index region. A conservative
starting point is:

```text
hmax <= lambda0 / (8*n_max)    for 2D quadratic elements
hmax <= lambda0 / (5*n_max)    for 3D quadratic elements
```

Use a Port when the incident optical power must be well defined. Use Scattering
Boundary Condition or PML for open boundaries; prefer PML when oblique or
non-planar outgoing waves cause reflections.

Track optical power consistently:

```text
absorbed_power_layer = intop_layer(emw.Qh)
generation_rate = absorbed_power_layer / (h_const*c_const/lambda)
```

Check the actual interface tag (`ewfd` or `emw`) before using variables such as
`ewfd.Pin`, `ewfd.normE`, or `emw.Qh`.

## Result extraction patterns

Prefer numerical result features for machine-readable data instead of scraping
tables or plots.

```python
def ensure_global(jm, tag, exprs, dataset=None, units=None):
    num = jm.result().numerical()
    if tag in list(num.tags()):
        num.remove(tag)
    gev = num.create(tag, "Global")
    gev.set("expr", exprs)
    if dataset:
        gev.set("data", dataset)
    if units:
        gev.set("unit", units)
    gev.run()
    return gev.getData()
```

For sweeps, remember `getData()` is ordered as
`result[expression][solution][value]`. For outer parametric sweeps, set or loop
over `outersolnum` explicitly when ambiguity appears.

## Validation checklist

Before declaring a COMSOL automation result valid:

- Record COMSOL version, required modules, and model file version.
- Confirm geometry was built after edits: `geom.run()`.
- Confirm selections still point to the intended domains/boundaries after any
  Boolean operation or stack thickness change.
- Check that every dimensional parameter includes units.
- Verify material properties and semiconductor variables use the active physics
  tag (`semi`, `ewfd`, `emw`, `ht`, etc.).
- Run at least one small mesh/bias/wavelength case before full sweeps.
- Export machine-readable CSV/JSON plus the `.mph` or Java snapshot needed to
  reproduce the case.
- Physically review the result through band alignment, carrier dynamics, trap
  states, and built-in field.


