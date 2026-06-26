# GeoGebra Diagram Generator Skill

A Codex skill for generating accurate static or interactive geometry diagrams in GeoGebra using a single `Execute({...})` script.

The skill is designed for geometry problems where free points, reflected points, perpendiculars, tangencies, ratios, angle measurements, and auxiliary construction lines must stay geometrically correct while the diagram is moved or parameterized.

## What It Does

- Builds a coordinate model for a geometry problem.
- Produces a single-line GeoGebra `Execute({...})` command.
- Uses GeoGebra-native constraints such as `Intersect`, `Reflect`, `PerpendicularLine`, `ParallelLine`, `Rotate`, and `Circle`.
- Adds `SetAxesRatio[1, 1]` so circles, squares, rotations, and perpendicular relationships are not visually distorted.
- Supports dynamic diagrams with sliders and constrained moving points.
- Guides browser execution and verification on GeoGebra.

## When To Use

Use this skill when Codex should:

- Draw a geometry problem in GeoGebra.
- Create a copy-pasteable GeoGebra script.
- Preserve geometric relationships dynamically instead of drawing static approximations.
- Open GeoGebra in a browser, paste the script, and verify the result with visible objects, measured values, or a screenshot.

## Recommended GeoGebra Workflow

The most reliable browser workflow is:

1. Open <https://www.geogebra.org/geometry>.
2. Dismiss any restore-unsaved-work dialog if it appears.
3. Select the left-side Algebra panel.
4. Click the input row, such as `Input...` or the localized input textbox.
5. Paste the entire `Execute({...})` command through the browser clipboard.
6. Press Enter.
7. Verify the expected objects, ratios, or angles in the Algebra panel.
8. Capture or show a screenshot when reporting success.

Avoid programmatic `fill()` on GeoGebra's math input. It can update the visible textbox without synchronizing GeoGebra's internal editor state. Clipboard paste plus Enter behaves like real user input and is much more reliable.

## Example

```geogebra
Execute({"SetAxesRatio[1, 1]", "A=(0,0)", "B=(6,0)", "D=Point[Segment[A,B]]", "s=Segment[A,B]", "p=PerpendicularLine[D, s]", "C=Intersect[p, Circle[D, 2], 1]", "Segment[D,C]", "SetColor[p, 0.85, 0.85, 0.85]", "SetLineStyle[p, 2]"})
```

## Skill Files

- `SKILL.md` contains the main Codex instructions.
- `references/examples.md` contains reusable GeoGebra `Execute` patterns and browser paste checks.
- `agents/openai.yaml` contains UI metadata for Codex skill discovery.

## Installation

Clone or copy this folder into your Codex skills directory:

```powershell
git clone https://github.com/gallexy-liu/geogebra-diagram-generator.git $env:USERPROFILE\.codex\skills\geogebra-diagram-generator
```

Then invoke it in Codex with:

```text
$geogebra-diagram-generator
```

