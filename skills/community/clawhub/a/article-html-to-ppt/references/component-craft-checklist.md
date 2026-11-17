# Component Craft Checklist

Use before scoring and final handoff.

## Text

- Component type is registered in `references/component-registry.json`.
- Selected delivery route exists in `delivery-plan.json`.
- Judgment title fits without clipping.
- Body text is transformed, not copied as paragraphs.
- Labels use consistent case, length, and alignment.
- Source and assumption notes are visible but quiet.

## Cards And Frameworks

- Route is `native_ppt`; cards are not SVG/raster/generated unless the user explicitly approved an exception.
- Cards are equal only when ideas are equal.
- Each card has a clear role: claim, proof, risk, action, example, or status.
- Card count and text length fit the slide density.
- Icons add recognition, not repetition.
- Fill, border, radius, padding, text color, and shadow come from `card_tokens`.

## Tables And Matrices

- Route is `native_table`; cells, headers, highlights, and source notes remain editable.
- Table is the primary anchor or clearly secondary.
- Row/column count does not force unreadable text.
- Highlights guide the intended comparison.
- Empty or low-value cells are removed or summarized.
- Header fill, text color, row alternation, border width, and cell padding come from `table_tokens`.

## Charts

- Route is `native_chart` for simple charts; data remains editable.
- Chart type matches the comparison task.
- Labels and units are clear.
- Color highlights the message, not every series equally.
- The title interprets the chart.
- Series colors, axes, labels, gridlines, markers, and legend defaults come from `chart_tokens`.

## Relationship Diagrams

- A valid Diagram IR exists before drawing: `diagram_ir_ref` or inline `diagram_ir`.
- Diagram IR declares nodes, groups, edges, boundaries, and at least one primary main path.
- Edge relation semantics are chosen before line style; style comes from `diagram_tokens`.
- Weak influence/monitoring relations are annotations when they would create connector web noise.
- Route is `native_diagram` while within complexity limits; otherwise use `hybrid_overlay` or `svg_component` with editable labels/legend.
- Nodes are grouped into lanes, layers, regions, or modules.
- Connectors are meaningful and limited.
- Relationship types are visually distinguishable only when necessary.
- Ownership, trust, risk, or boundary lines are explicit when they matter.
- Stop and choose SVG/render/generated component if native PPT becomes connector noise.
- Node, boundary, connector, and relation styles come from `diagram_tokens`.

## Raster/SVG/Generated Components

- Route is allowed by Component Registry and recorded in Delivery Plan.
- Component is bounded, not full-slide unless approved.
- Core explanatory text remains editable.
- Prompt/source path is stored.
- Raster acceptance reason is recorded.
- Verification report discloses media count and rasterized components.
