# Creative Micro Assets

This layer integrates the useful idea from external creative-tool skills: select a compact visual medium that improves communication. It is an internal method router, not a dependency on the external skill.

## When To Use

Enable `Creative Micro Assets Routing` when the content asks for or benefits from:

- ASCII / monospace art for developer, command-line, retro, terminal, or playful technical contexts.
- Hand-drawn micro diagrams for informal explainers, knowledge maps, article inline images, workshop notes, or lightweight concept maps.
- Excalidraw-style editable sketch assets when the user wants a shareable diagram source in addition to rendered cards.
- p5.js / generative canvas textures or motion studies for HTML-rendered covers/cards, when the final text remains separate and readable.
- PixiJS canvas layers for particles, lighting, sprites, procedural texture, data-flow atmosphere, or static motion-study frames when pure HTML/CSS rendering looks low quality.
- DESIGN.md-style token notes when a visual system needs to be handed to another agent or engineering renderer.

Do not use this layer to bypass Source Lock, platform specs, content compression, exact Chinese text requirements, or asset-source policy.

## Placement

```text
Source Lock
↓
Output Mode Router
↓
Execution Mode Router
↓
Content Analysis / Compression
↓
Style Atlas / Visual Direction / Illustration Grammar / Design Enhancement
↓
Creative Micro Assets Routing（optional）
↓
Prompt / Render Package
↓
Batch Generation / Rendering
↓
Quality Gate
```

## Medium Router

| Need | Route | Production Boundary |
|---|---|---|
| Retro, terminal, code culture | `ascii_art` / `monospace_mark` | Use native text or HTML/CSS text; keep Chinese exact text outside image models |
| Soft explanatory sketch | `hand_drawn_diagram` | Good for inline images and social cards; avoid tiny text |
| Editable sketch source | `excalidraw_source` | Deliver `.excalidraw` or JSON as source asset plus rendered preview |
| Browser generative texture | `p5js_canvas` | HTML/render-engine only; screenshot/export output is static |
| Rich browser canvas visual | `pixijs_canvas` | HTML/render-engine or static screenshot export only; use `pixijs_generated_visual_layer` for AI background + canvas overlay routes |
| Agent-readable design handoff | `design_token_note` | Output tokens and rationale; do not replace the visual card schema |

## Output Fields

When enabled, output:

- `creative_micro_assets.enabled`
- `creative_micro_assets.trigger`
- `creative_micro_assets.asset_plan[]`
- `creative_micro_assets.medium`
- `creative_micro_assets.target_output_family`
- `creative_micro_assets.rendering_route`
- `creative_micro_assets.text_policy`
- `creative_micro_assets.asset_source_policy`
- `creative_micro_assets.anti_copy_boundary`
- `creative_micro_assets.quality_checks`

Each `asset_plan[]` item should include:

- `id`
- `medium`
- `page_or_card`
- `purpose`
- `source_anchor`
- `rendering_route`
- `text_policy`
- `export_boundary`

## Boundaries

- ASCII art is content when it carries theme, mood, or label meaning; it is noise when it fills space.
- Hand-drawn style is not a universal default. Serious product, business, legal, finance, or investor material usually needs `product-evidence`, `swiss-grid`, or `editorial-magazine` unless the user explicitly asks for a sketch tone.
- p5.js and generative canvas outputs can support HTML render previews, but they must not make mobile text unreadable.
- PixiJS canvas can improve generated visual depth, particles, lighting, and sprite composition, but final card/cover/image delivery is static unless the requested output is an HTML preview.
- Excalidraw or sketch JSON can be source material, but final social cards and WeChat images still need platform-sized previews.
- External creative repositories are method references only. Do not copy templates, sample diagrams, CSS, source code, palettes, assets, or visual signatures.

## Quality Checks

- The micro asset has a declared purpose tied to a source claim or reading-rhythm job.
- The medium choice is smaller and clearer than a full illustration or large decorative background.
- Exact Chinese text remains in engineering rendering or post-layout when precision matters.
- Mobile thumbnails remain readable.
- Asset source records exist for any external image, font, texture, logo, screenshot, or imported diagram source.
- Anti-copy boundaries are explicit when the route was inspired by an external skill or public example.
