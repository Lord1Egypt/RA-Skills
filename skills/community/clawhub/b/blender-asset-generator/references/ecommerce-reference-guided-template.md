## Ecommerce "Reference-Image Guided" Template

Goal: given one or more reference images, produce a *confirmable* structure + dimensions spec for ecommerce assets, with low user effort.

### Inputs

- Images: ideally `front`, `side`, `top/back` (any subset works)
- Optional: scale reference in image (ruler, A4 paper, coin, hand, known standard)
- Text: product name + category + short description

### Output: "Structure Card" (agent-generated)

Always output this card before generating the final `spec.json`:

```text
Structure Card (Draft)

1) View & assumptions
- Views available: front/side/top/other
- Symmetry: none | left-right | radial
- Hidden parts: unknown | inferred (must be marked as inferred)
- Scale: known anchor | unknown (needs 1 anchor)

2) Components (decomposed)
- Component A: (e.g., main body) -> primitive: box/cylinder/profile
- Component B: (e.g., lid/cap) -> primitive: cylinder
- Component C: (e.g., handle/spout/button) -> primitive: box/cylinder/curve-extrude

3) Key dimensions (best-effort, mark confidence)
- Overall: height H=?, width W=?, depth D=? (confidence: high/med/low)
- Diameters: D1=?, D2=? (confidence)
- Thicknesses: wall T=?, lid T=? (confidence)
- Radii/chamfers: R=? (confidence)

4) Material hints (visual)
- Main: matte plastic / brushed metal / glass / rubber
- Color palette: #... (optional)
- Surface details: label area / logo recess / grip texture (optional)

5) What MUST be confirmed by user (minimal)
- One anchor dimension (e.g. height in mm)
- Any critical functional dimension (e.g. opening diameter)
```

### How the agent extracts dimensions from images (Vision-assisted mode)

Rules (keep it honest and low-friction):
- Never claim exact dimensions from a single photo without a scale anchor.
- Use relative ratios when scale is unknown (e.g. `W/H = 0.62`).
- If multiple views exist, cross-check ratios (front vs side).
- Mark each inferred dimension with confidence.

Recommended extraction steps:
1. Identify silhouette bounding box in each view.
2. Estimate aspect ratios (H:W, H:D).
3. Detect key features and their relative placement:
   - Lid height as % of total height
   - Handle thickness vs body width
   - Spout position from top edge
4. If a scale reference exists:
   - Derive pixel-to-mm scale (approx)
   - Convert key dimensions to mm
5. Ask for ONE anchor if missing:
   - "Please confirm one value: overall height (mm) or overall width (mm)."

### A universal "Ecommerce Spec" mapping

For ecommerce, focus on what reduces returns:
- Overall dimensions (H/W/D)
- Opening size / usable volume (if applicable, only if user provides)
- Fit-critical sizes (case, holder, accessory compatibility)
- Material + finish (matte/gloss, metal vs plastic)
- Included parts (caps, seals, accessories)

### Output: Final `spec.json`

After user confirms the minimal anchor(s), generate `spec.json`:
- Use mm
- Put unknowns into `open_questions`
- Preserve a `reference_images` array with notes and assumptions

