# Export Route Eligibility

Route eligibility must stay explicit and reviewable. Do not invent route heuristics ad hoc inside a renderer.

## Route eligibility matrix

| Route | Structural prerequisites | First fallback | Terminal behavior |
|------|---------------------------|----------------|-------------------|
| `freeflow` | Any valid blueprint with at least one renderable node or relation | None | If integrity still fails, export exits non-zero with a structural diagnostics payload |
| `architecture-template` | Recognizable L→R architecture shape, categorized systems, limited per-layer density, and no route-breaking overflow risk | `freeflow` | Same as above |
| `poster` | Clear layer/group structure with bounded peer density per row or wrapped-row support | wrapped poster or `freeflow` | Same as above |
| `swimlane` | Actor-owned flow steps with meaningful lane grouping | `freeflow` | Same as above |
| `hierarchy` | Stable tree/group relationship with low ambiguity in parent-child grouping | `freeflow` | Same as above |
| `evolution` | Ordered chronological or staged progression data | `freeflow` | Same as above |

## Selection policy

- If a request matches a supported, standard export template, use that template.
- If there is no standard export template for the requested diagram, fall back to `freeflow`.
- Do **not** substitute `swimlane`, `matrix`, `product tree`, or other generic views just because they are available.
- When embedding a blueprint diagram into a report or ad hoc analysis, `freeflow` is the safe default unless the user explicitly asks for a supported standard template.

## Fallback chain

```
requested route → check prerequisites → pass: use it / fail: fallback route → ... → freeflow → fail: non-zero exit with diagnostics
```

If a standard template would create a squeezed, clipped, or overcrowded diagram, stop using the fixed template geometry and fall back to `freeflow` or a wrapped multi-row layout.

## Architecture diagram route

When user requests an architecture diagram (keywords: "架构图", "architecture diagram", "diagram"):

1. Read `references/architecture-design-system.md` for the complete design system.
2. Read the appropriate template from `references/architecture-templates/`:
   - AWS/Serverless/Lambda → `serverless.md`
   - Microservices/Kubernetes/微服务 → `microservices.md`
   - Other → use `serverless.md` as a structural reference
3. If the request does not match a supported template, stay on `freeflow`.

## Geometry integrity

Geometry-sensitive integrity checks must use the numeric thresholds from `evals/export-integrity-thresholds.json`, not prose heuristics.

## Output

- Default: SVG + HTML viewer in `solution.exports/`
- `--format drawio|excalidraw|mermaid` for other formats
- Architecture diagrams: single HTML file `{blueprint_stem}.html` alongside the blueprint JSON
- No external dependencies (except Google Fonts CDN for JetBrains Mono)
