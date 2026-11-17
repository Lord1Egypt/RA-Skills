# Component Raster Fallback

Use localized raster, SVG/HTML render, or generated visual components when a bounded slide component expresses relationship complexity, visual metaphor, spatial structure, or rich material treatment that native PPT objects would make confusing, ugly, brittle, or visually unfinished.

## Default Principle

Do not rasterize an entire deck unless the user explicitly asks for image-only delivery. The default final deck remains hybrid editable: titles, explanatory text, labels, sources, cards, tables, simple charts, and ordinary diagrams should be editable PPT objects.

For `relationship_visual`, `conceptual_scene`, and visual-heavy `hybrid_panel` slides, a rendered/generated bounded component is a planned delivery route, not merely late-stage rescue.

## Good Candidates

- complex relationship maps with many cross-links
- ecosystem maps or stakeholder networks
- capability landscapes with nested regions and soft boundaries
- conceptual metaphors or abstract spatial structures
- dense architecture murals where visual comprehension matters more than direct editing
- illustrated process scenes, IP illustrations, or editorial visual metaphors
- complex textures, material backgrounds, photos, or atmospheric layers

## Poor Candidates

Do not image-generate components that can be made clear and editable as native PPT objects:

- 2x2, 2x3, or 3x3 card grids
- ordinary comparison matrices
- tables and scorecards
- metric cards
- simple process lanes
- clean issue trees or dependency trees
- simple architecture diagrams with modest connector counts
- already-stabilized layouts after reducing connectors, grouping, or switching to cards

## Decision Test

Before choosing raster/generated delivery, answer:

1. Is the component's value mainly spatial relationship, visual metaphor, complex visual texture, or soft-boundary structure?
2. Would native PPT reconstruction require fragile connectors, nested shapes, masks, or effects?
3. Would the user reasonably accept reduced editability if title, interpretation, labels, source notes, and surrounding content remain editable?
4. Have simpler editable alternatives been tried or rejected for a clear reason?

Use localized image fallback only when 1-3 are yes, and 4 is documented.

## Required Resolver Flow

Raster fallback is an engineered route, not a visual shortcut. Before any bounded SVG/image/generated component is built, follow this flow:

1. Query `references/component-registry.json` for the object's `component_type`.
2. Check `native_capability`, `allowed_delivery_routes`, and `raster_policy`.
3. Check the current Builder capability (`full`, `partial`, `visual_only`, `unsupported`, or `unknown`).
4. Check object complexity against `complexity_limits.native`.
5. Select the smallest local SVG/image region that preserves comprehension.
6. Preserve the declared `editable_core` as native PPT overlay where the route requires it.
7. Record the bounded component area ratio; never silently rasterize the whole slide.
8. Write the selected route, fallback reason codes, editable core, raster/SVG parts, and QA checks to `delivery-plan.json`.
9. Write actual route and any deviation to `build-manifest.json`.
10. In QA, compare intended route against actual build output and disclose non-editable parts.

普通组件不进入 Raster Fallback。`metric_card`、普通表格、矩阵、简单图表、标题、正文、来源说明、普通卡片必须优先保持原生可编辑；如果 Builder 做不到，Resolver 应返回 `unsupported` 或切换 Builder，而不是截图糊过去。

## Implementation Contract

- crop the image to the component region, not the full slide
- keep title, interpretation line, key labels, source note, and footer editable
- overlay key labels as editable PPT text when later editing is likely
- store prompt and image path in the project directory
- disclose the rasterized component in `delivery-plan.json`, `build-manifest.json`, and `verification-report.md`
- count media objects and confirm only intended components are rasterized
- ensure the user can tell which parts are editable and which parts are not

## Native PPT Stop Conditions

Stop adding native PPT connectors when more than 8 nodes, more than 9 connectors, more than 2 relationship types, 3 connector crossings, labels below 10 pt, nested soft boundaries, or fragile micro-positioning are required.
