---
name: geogebra-diagram-generator
description: Generate precise static or interactive geometry diagrams for geometry problems using GeoGebra's Execute text script. Use when Codex needs to create a construction for geogebra.org/geometry or geogebra.org/classic, produce a single-line Execute({...}) command, preserve geometric constraints dynamically with GeoGebra commands, paste and verify a diagram through GeoGebra's Algebra panel, or autonomously draw and screenshot a geometry figure in a browser when browser automation is available.
metadata:
  openclaw:
    emoji: "📐"
    homepage: https://github.com/gallexy-liu/geogebra-diagram-generator
    requires:
      env: []
      bins: []
---

# GeoGebra Diagram Generator

Create GeoGebra geometry diagrams by computing a clean coordinate model, then emitting one `Execute({...})` command made of GeoGebra strings. Prefer native GeoGebra constraints over browser clicks or static coordinates when relationships must stay true while points move.

## Workflow

1. Analyze the geometry.
   - Choose a virtual Cartesian coordinate system, often with a natural origin such as `O=(0,0)`.
   - Compute coordinates, equations, circle radii, ratios, and angles needed to make the figure accurate.
   - Identify free elements, movable constrained elements, and derived elements.
   - Preserve dynamic relationships with GeoGebra constructions whenever possible, not with one-time coordinate approximations.

2. Formulate GeoGebra command strings.
   - Use variables and sliders for user-controlled values, for example `"r=5"` or `"ang=Slider[0°, 360°, 1°]"`.
   - Use constrained moving points such as `"D=Point[Segment[A,B]]"` or `"P=Rotate[A, ang, O]"`.
   - Enforce relationships with native commands: `PerpendicularLine[A, line]`, `ParallelLine[A, line]`, `Intersect[obj1, obj2]`, `Circle[O, r]`, `Rotate[A, ang, O]`, etc.
   - Include `"SetAxesRatio[1, 1]"` in every diagram to prevent visual distortion of circles, squares, rotations, and perpendiculars.

3. Apply syntax and compatibility rules.
   - Use square brackets `[]` for GeoGebra math commands, not parentheses.
   - Avoid escaped color-name strings such as `\"Black\"`; use RGB numeric color commands, for example `SetColor[obj, 0, 0, 0]`.
   - Avoid `ShowObject`, `SetVisibleInView`, and similar visibility commands because localized GeoGebra builds may crash. Make auxiliary objects faint instead: `SetColor[line, 0.85, 0.85, 0.85]` and `SetLineStyle[line, 2]`.
   - Keep object names stable and meaningful so later commands can reference them.

4. Provide the result.
   - Return a single-line fenced `geogebra` code block containing `Execute({...})`.
   - Briefly explain which objects are movable, which sliders control the construction, and which relationships are guaranteed.
   - If a browser automation skill or tool is available, prefer `https://www.geogebra.org/geometry` for geometry problems. Open the Algebra panel first, click the `Input...` / `输入...` row, paste the command through the clipboard, press Enter, and verify that the figure appears.
   - If no browser automation tool is available, tell the user to open GeoGebra Geometry or Classic, switch to the Algebra panel, paste the single line into the input row, and press Enter.

## Browser Execution

Prefer the real paste workflow on `https://www.geogebra.org/geometry`; it has proven more reliable than directly filling GeoGebra's math input or using `https://www.geogebra.org/classic`.

1. Open `https://www.geogebra.org/geometry`.
2. If GeoGebra shows a restore-unsaved-work dialog, dismiss it before testing a fresh script.
3. Select the left-side Algebra panel (`Algebra` / `代数区`).
4. Click the input row (`Input...`, `输入...`, or a localized textbox such as `在此处输入方程或代数式.`).
5. Write the whole `Execute({...})` command to the browser clipboard, paste it, then press Enter.
6. Verify by checking the expected objects or measured values in the Algebra panel and by capturing a screenshot. Save or display the screenshot when the user needs evidence.

Do not rely on Playwright-style `fill()` for GeoGebra math input. It can change the visible DOM value without synchronizing GeoGebra's internal editor state; even simple entries like `A=(0,0)` may then fail. Clipboard paste plus Enter matches real user input and is much more dependable.

If the browser exposes a JavaScript evaluation surface and clipboard paste is not available, injecting through GeoGebra's applet API can still work:

```javascript
ggbApplet.evalCommand('Execute({"SetAxesRatio[1, 1]", "O=(0,0)", "A=(2,0)", "B=(0,2)", "Segment[A,B]"})')
```

After any execution path, verify that expected objects exist or that the canvas is nonblank. If execution fails, inspect the failing command string first for bracket syntax, quotes, unsupported localized commands, malformed Unicode degree symbols, or a hidden restore dialog blocking the page.

## Examples

Read `references/examples.md` when you need a compact template for common constructions or when debugging GeoGebra syntax.
