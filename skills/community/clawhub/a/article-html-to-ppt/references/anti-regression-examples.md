# Anti-Regression Examples

## Detailed Spec Literalism

Bad: follow every placeholder, coordinate, grid line, connector, and decorative mark from a spec until the slide looks like a wireframe.

Good: infer design intent, assign visual priorities, delete low-value objects, and preserve the primary anchor.

## Relationship Hidden In Cards

Bad: turn an ecosystem or architecture paragraph into six equal cards.

Good: use Expression Mode Gate; choose relationship visual or hybrid panel when dependencies, boundaries, flows, or loops matter.

## Connector Web

Bad: keep adding PPT connectors because the source mentions relationships.

Good: group into lanes/layers, cap connectors, split the slide, or use SVG/HTML/generated component for bounded complex maps.

## Raster Overuse

Bad: rasterize ordinary cards, tables, matrices, metric cards, or simple charts for polish.

Good: keep ordinary message-bearing components editable; reserve raster/SVG/generated components for bounded visual complexity.

## Topic Titles

Bad: `Market Trends`, `Architecture`, `Risks`.

Good: `Adoption is broad, but scaling still concentrates in a minority of operators`.

## Fake Verification

Bad: deliver only `deck.pptx` and claim final.

Good: render/read back representative slides, count objects/media where possible, and write `verification-report.md` with known limits.

## Connector Web Without Main Path

Bad: draw 8 nodes with 17 equal-weight lines and no dominant reading path.

Good: keep the main path primary, weaken secondary relations, cluster nodes into groups, and move weak relations into annotations.

## Relationship Hidden In Cards

Bad: convert a system call chain into six equal cards with no direction or dependency.

Good: choose `relationship_visual`, write Diagram IR, and preserve request/response/data-flow edges.

## Decorative Curves Everywhere

Bad: use curved connectors everywhere because it looks premium.

Good: use orthogonal lines for the main flow, curved lines for feedback, and dashed/muted lines for weak dependencies.

## Missing Responsibility Boundary

Bad: mix internal services and external tools in one region.

Good: add a trust/ownership/permission boundary and move external tools into an external zone.

## Paragraph Nodes

Bad: put full paragraphs inside nodes.

Good: use short labels, move descriptions to speaker notes, and add annotations only where they clarify.

## Swimlane Misuse

Bad: use four lanes when there is no role or system handoff.

Good: use `process_lane` or `timeline`, or remove lanes entirely.

## Dense Architecture Mural

Bad: put 18 nodes and 30 edges on one slide.

Good: keep 7-8 first-level nodes on the main page and split detailed call chains into follow-up pages.

## Whole Diagram Screenshot

Bad: embed title, nodes, labels, and legend in one PNG.

Good: use SVG or hybrid overlay for the bounded diagram base and keep title, labels, legend, and key annotations native/editable.

## Benchmark Coverage

Phase 7 benchmark cases should include small, stable examples for:

- all-bullets or long-paragraph copy;
- card overuse where a relationship visual is expected;
- connector-web diagrams;
- whole-slide raster;
- rasterized table and chart;
- palette drift;
- multiple primary anchors;
- fake judgment titles.

When a real production failure appears, add the smallest reproducible benchmark case and reference rubric instead of relying on memory or model preference.
