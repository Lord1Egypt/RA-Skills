# Diagram and visual guidelines

The six views in this skill share this reference.

## Diagram notation

- Provide complete Mermaid blocks. Use `flowchart` for static structure, `classDiagram` for code, and `sequenceDiagram` for dynamic interaction. See the [syntax reference](c4-syntax.md) for native C4 notation.
- Give each diagram a title, level, scope, and current or target status. Supply a legend for element types, boundaries, and line styles, and retain it in exports.
- Label nodes with names, types, and short responsibilities. Add technology to containers and components, or mark it unconfirmed. Use boundaries for ownership.
- Use directed arrows and specific verbs. Label protocols between containers. Distinguish source dependencies, runtime calls, and data flows. A sequence response does not automatically create a reverse static dependency.
- Keep names and identifiers consistent across diagrams. Name the parent in each expansion, with neighboring containers and external systems outside its boundary.
- Let each diagram answer one main question. Split crowded views by object or scenario, and reduce crossing lines and long labels.

## Light and dark colors

Default templates use muted fills, responsibility colors, and thin strokes. Theme changes preserve nodes, relationships, and layout.

| Responsibility | Dark accent | Light accent |
|---|---|---|
| Frontend and ingress | `#22D3EE` | `#0E7490` |
| Business services | `#34D399` | `#047857` |
| Background jobs | `#2DD4BF` | `#0F766E` |
| Data storage | `#C084FC` | `#7E22CE` |
| Security and identity | `#FB7185` | `#BE123C` |
| Messaging | `#F59E0B` | `#B45309` |
| Cloud and networking | `#FACC15` | `#A16207` |

| Element | Dark | Light |
|---|---|---|
| Canvas | `#07111F` | `#F8FAFC` |
| Body text | `#E6EDF3` | `#142238` |
| Secondary text | `#9AA9BC` | `#53647A` |
| Lines | `#B8C4D4` | `#52657D` |
| External node fill | `#101B2B` | `#F1F5F9` |
| External node stroke | `#66758A` | `#8090A4` |

## Nodes and boundaries

- Make node names bold, with responsibilities and technologies below. Use approximately 15px body text and 12px secondary text.
- Use approximately 1.2px node strokes and 8px corners. Groups use 1px strokes, 10px corners, and a `4 3` dash pattern.
- Color supplements labels and boundaries. Use only colors needed by the elements shown.
- Solid lines in static diagrams represent directed relationships. Sequence notation distinguishes calls and responses. Labels and legends explain asynchronous behavior.
- Use local fonts without remote icon dependencies. Check native C4 theme and layout support in the actual renderer.

## Export and review

- Set the export canvas color. Retain the title, scope, legend, and Mermaid source.
- Check text, arrow, and boundary contrast, along with label overlaps, wrapping, and crossing lines.
- Review at desktop width and native export size. Theme changes must preserve model meaning.
