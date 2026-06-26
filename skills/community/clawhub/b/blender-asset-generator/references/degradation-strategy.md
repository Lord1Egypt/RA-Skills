## Degradation Strategy (When Vision Is Not Available)

Problem: user provides reference images, but the local agent/runtime cannot do multimodal vision.

Design goal: never block the pipeline. Always continue with a deterministic text-driven build, while collecting the minimum extra info needed to make the asset usable.

### Rule 1: Acknowledge image, do not interpret it

If vision is unavailable:
- Do not guess shapes, colors, or dimensions from the image.
- Use the image only as a file attachment to be carried into the project package for later reference.

### Rule 2: Ask a "Minimal Clarification Form"

Ask the user to answer 6 items max (prefer 3):

```text
Minimal Clarification Form (No-Vision Mode)

1) What is it? (one sentence)
2) Choose the closest base shape:
   - A) box-ish (rounded rectangle)
   - B) cylinder-ish
   - C) bottle-ish (cylinder + neck)
   - D) flat plate/sheet
3) Provide ONE anchor dimension in mm:
   - height OR width OR diameter = ?
4) Do you need a lid/cap/handle/button? (yes/no; if yes, which)
5) Target style: matte plastic / metal / glass / other
6) Output: GLB (required); FBX (optional yes/no)
```

If the user refuses dimensions:
- Use a category default size from presets, and mark `open_questions` prominently.

### Rule 3: Continue with "Text-only Mode"

Proceed to generate:
- `spec.json` using defaults and user answers
- scripts + run commands
- preview renders

Mark all unconfirmed dimensions as:
- `confidence: low`
- or put into `open_questions`

### Rule 4: Provide a "Upgrade Path"

Offer two ways to improve accuracy later:
- User supplies one more anchor dimension or a simple dimension table
- User runs the same project in a vision-capable agent (cloud) to refine the spec

