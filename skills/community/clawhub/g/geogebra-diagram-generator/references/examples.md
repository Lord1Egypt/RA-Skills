# GeoGebra Execute Examples

Use these examples as compact patterns. Always adapt object names and geometry to the problem.

## Rotating Dynamic Triangle

```geogebra
Execute({"SetAxesRatio[1, 1]", "ang=Slider[0°, 360°, 1°]", "O=(0,0)", "A=Rotate[(2,0), ang, O]", "B=Rotate[(0,2), ang, O]", "Segment[A,B]", "Segment[O,A]", "Segment[O,B]"})
```

## Point Constrained To Segment With Perpendicular

```geogebra
Execute({"SetAxesRatio[1, 1]", "A=(0,0)", "B=(6,0)", "D=Point[Segment[A,B]]", "s=Segment[A,B]", "p=PerpendicularLine[D, s]", "C=Intersect[p, Circle[D, 2], 1]", "Segment[D,C]", "SetColor[p, 0.85, 0.85, 0.85]", "SetLineStyle[p, 2]"})
```

## Circle Tangency By Construction

```geogebra
Execute({"SetAxesRatio[1, 1]", "O=(0,0)", "r=3", "c=Circle[O, r]", "A=Point[c]", "t=PerpendicularLine[A, Segment[O,A]]", "SetColor[t, 0.85, 0.85, 0.85]", "SetLineStyle[t, 2]"})
```

## Output Checklist

- Include `SetAxesRatio[1, 1]`.
- Emit exactly one top-level `Execute({...})` block for the user to paste.
- Use GeoGebra square-bracket command syntax.
- Prefer `Point`, `Intersect`, `PerpendicularLine`, `ParallelLine`, `Rotate`, and `Circle` to preserve constraints.
- Style auxiliary objects faintly instead of hiding them.
- Explain draggable points and sliders after the code block.

## Browser Paste Checklist

- Prefer `https://www.geogebra.org/geometry` for geometry diagrams; use Classic only as a fallback.
- Dismiss any restore-unsaved-work dialog before testing a fresh construction.
- Click the left-side Algebra panel (`Algebra` / `代数区`) before trying to paste.
- Click `Input...`, `输入...`, or the localized algebra textbox before pasting.
- Paste with the browser clipboard and press Enter; avoid programmatic `fill()` on GeoGebra's math editor.
- Verify by reading expected objects or values in the Algebra panel, then save or display a screenshot when reporting success.
