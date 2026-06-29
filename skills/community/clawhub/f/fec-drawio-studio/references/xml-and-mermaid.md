# XML And Mermaid

Use this reference to choose the lightest editable diagram source that still meets the user's maintenance and fidelity needs.

## Route Choice

- Use Mermaid for common flowcharts, sequence diagrams, class diagrams, state diagrams, ERDs, timelines, mind maps and other text-first diagrams that will live in Markdown.
- Use draw.io XML when the diagram needs exact shapes, vendor symbols, nested containers, layers, tags, metadata, custom colors or a durable `.drawio` source.
- Use CSV only as a short import path for tabular structures such as org charts or simple relationship maps; save the resulting editable source when possible.
- Use URL creation for preview and handoff, not as the only artifact for important diagrams.

## XML Structure

- Include root cells `id="0"` and `id="1"` in every diagram.
- Give every visible vertex and edge a stable unique id.
- Put child nodes inside their visual container by setting `parent` to the container id and using coordinates relative to that container.
- Put edges that cross container boundaries at `parent="1"` so they are not clipped by a lane or group.
- Every edge must contain `<mxGeometry relative="1" as="geometry"/>`; do not use self-closing edge cells.
- Use `&#xa;` for forced line breaks in `value` attributes. Literal `\n` renders as text in draw.io and should be treated as a quality issue.
- Keep manually placed vertices on a 10px grid, within `pageWidth` / `pageHeight`, and with stable dimensions so hover, labels and exports do not shift the layout.
- For manually authored flowcharts, keep `pageWidth` at or below 800 unless the diagram is deliberately a wide matrix or cross-functional table.

## Containers And Process Layout

- Use titled swimlanes for actor, tier or bounded-context groupings.
- Use nested swimlanes for real hierarchy such as region, VPC, availability zone and workload.
- Use a table layout for cross-functional flows where both actor rows and phase columns matter.
- Use plain groups only when a visual boundary is unnecessary and the group should not capture connectors.

## Layers, Tags And Metadata

- Use layers for major visibility sets, such as logical view, physical view, annotations or migration phases.
- Use tags for cross-cutting filters such as critical, deprecated, external, v2 or owner names.
- Use object metadata and placeholders when a shape represents a record with fields such as owner, status, IP, service tier or version.
- Keep visible labels concise; put secondary facts in metadata or notes when the diagram would otherwise become hard to scan.

## Labels And Dark Mode

- Match diagram label language to the user's language.
- Add `html=1` whenever labels contain HTML markup or escaped `<br>` formatting.
- Include `whiteSpace=wrap;html=1` on normal shape labels so long text wraps consistently.
- Escape XML attribute values: `&`, `<`, `>`, and `"` must be entities.
- Prefer adaptive colors and simple palettes; specify dark-mode overrides only when automatic inversion makes labels or shapes unclear.

## Mermaid Import Notes

- Pick the Mermaid header deliberately: `flowchart`, `sequenceDiagram`, `classDiagram`, `stateDiagram-v2`, `erDiagram`, `timeline`, `mindmap`, `gantt`, `C4Context` and similar headers select different parsers.
- Quote labels that include punctuation, spaces, parentheses or non-ASCII text.
- Keep node ids simple and put display text in labels.
- For large, highly styled or vendor-specific diagrams, move to XML before final delivery.

## XML Well-Formedness

- Do not include XML comments.
- Do not leave raw ampersands or angle brackets inside attribute values.
- Do not use duplicate ids.
- Do not leave edges pointing to missing source or target cells.
- Run `diagram-lint.mjs` before final handoff. Use `--strict` when the exported artifact is a final deliverable so warnings such as overlaps, literal line breaks, missing wrapping styles, tiny fonts, grid drift and page overflow block the handoff.
