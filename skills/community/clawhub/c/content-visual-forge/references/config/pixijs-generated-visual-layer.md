# PixiJS Generated Visual Layer

This optional layer improves generated visual quality when pure HTML/CSS
engineering rendering looks flat, template-like, or too limited for the visual
job. It combines AI-generated no-text imagery with a PixiJS-rendered canvas
layer, then exports a static image through the render engine.

PixiJS is a browser rendering runtime, not a design template library. Use its
official agent-facing docs or installed skills as implementation context when
available, but treat them as method/runtime guidance only. Do not copy demo
code, assets, shaders, palettes, layouts, or visual signatures from external
examples.

## When To Use

Enable `pixijs_generated_visual_layer` when all of these are true:

- The output needs stronger visual richness than HTML/CSS templates can provide.
- The main visual job is mood, texture, particles, light fields, depth, motion
  study, data-flow atmosphere, sprite composition, or high-quality abstract
  graphics.
- Exact Chinese titles, data, labels, screenshots, and body copy can stay in the
  engineering text layer or post-layout layer.
- The final deliverable can be a static PNG/JPG/PDF frame, not an editable
  vector/design source.

Do not enable it just because a project mentions canvas. For simple cards,
tables, vocabulary cards, screenshots, or text-heavy layouts, plain
`engineering_rendering` remains the better route.

## Recommended Pipeline

```text
Source Lock
↓
Output Mode Router
↓
Execution Mode Router
↓
AI no-text image or subject background
↓
PixiJS canvas layer for particles / lighting / texture / procedural graphics
↓
HTML/CSS or post-layout text overlay
↓
Playwright screenshot export
↓
Quality Gate
```

## Route Choices

| Need | Route | Boundary |
|---|---|---|
| Editorial cover with richer atmosphere | `ai_background_plus_pixi_overlay` | AI generates no-text subject/background; PixiJS adds light, particles, depth, or motion-frame texture; text stays outside image model |
| Abstract data / tech / signal visual | `pixi_procedural_visual` | PixiJS renders self-generated geometry, sprites, or particles; no copied shader/demo signature |
| Social card cover page needs a premium visual anchor | `pixi_cover_frame_export` | Export one static frame for the cover/page image; subsequent cards can use simpler engineering layouts |
| Motion study for later static asset | `pixi_motion_study_frames` | Export selected still frames only; do not imply animated final delivery unless the output is HTML |

## Required Output Block

When enabled, output:

- `pixijs_generated_visual_layer.enabled`
- `pixijs_generated_visual_layer.trigger`
- `pixijs_generated_visual_layer.route`
- `pixijs_generated_visual_layer.target_output_family`
- `pixijs_generated_visual_layer.canvas_role`
- `pixijs_generated_visual_layer.ai_image_role`
- `pixijs_generated_visual_layer.text_policy`
- `pixijs_generated_visual_layer.asset_source_policy`
- `pixijs_generated_visual_layer.export_plan`
- `pixijs_generated_visual_layer.quality_checks`
- `pixijs_generated_visual_layer.anti_copy_boundary`

Each `export_plan.frames[]` item should include:

- `id`
- `page_or_card`
- `size`
- `source_layers`
- `static_export_path`
- `text_overlay_policy`
- `qa_focus`

## Boundaries

- PixiJS output is a browser canvas/runtime layer. Static image export is the
  default delivery for covers, cards, inline visuals, and PDF assets.
- Do not describe PixiJS canvas output as editable design source, editable PPT,
  or native vector graphics.
- Keep exact Chinese text, numbers, labels, UI screenshots, and source quotes in
  HTML/CSS, PPT, design-tool, or post-layout text layers.
- AI image generation should produce no-text or low-text visual subjects. It
  should not generate final Chinese copy.
- If external assets, textures, fonts, logos, or screenshots are used, they must
  be declared in `asset_source_record[]`.
- Generated procedural graphics may be recorded as `generated_graphics`, but the
  prompt/render package must still document how they were produced.
- If the PixiJS layer makes the image noisy, unreadable, or less faithful to the
  source, remove it and fall back to `background_then_layout` or plain
  `engineering_rendering`.

## Quality Checks

- The PixiJS layer solves a named visual problem, such as flatness, poor depth,
  weak atmosphere, or low-quality procedural texture.
- The generated image subject and PixiJS layer have separate roles.
- The output passes mobile thumbnail readability after the text overlay is added.
- The static export is checked at the target platform size.
- No external PixiJS demo, shader, texture, asset, code, or visual signature is
  copied into the production artifact.
- The render package states whether the final artifact is static image, HTML
  preview, or both.
