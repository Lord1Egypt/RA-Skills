# Native Connector and Visual Quality Gate

## Purpose

Prevent technically valid but visually degraded PPTX delivery.

## Bound Arrow Contract

A native editable process arrow must be one connector object. It must contain an arrow end and bind to both endpoint shapes.

Required PPTX evidence:

- `a:stCxn`
- `a:endCxn`
- `a:tailEnd` or `a:headEnd` with triangle/arrow type
- no separate triangle or chevron used as the arrowhead

Moving either endpoint shape in PowerPoint must preserve the relationship.

## Complex Diagram Qualification

The minimal Python Builder is qualified for simple process lanes only. It is not automatically qualified for:

- layered architecture
- capability landscape
- comparison matrix
- flywheel
- causal chain
- stakeholder network
- ecosystem map
- commercial staircase

Standard or Premium must stop when no qualified implementation exists. Generic cards or a single text box are not valid semantic fallbacks.

## Orphan Solid Block Gate

An empty solid-color shape with meaningful area must have a declared role in its object name:

- `Decoration:`
- `Background:`
- `Material:`
- `Connector:`

Undeclared solid blocks fail QA. Declared objects must still be intentional and non-occluding.

## Visual Acceptance

Structural inspection is not sufficient. Render, review the whole contact sheet, then enlarge every diagram-heavy page. Fail the deck for accidental lower-page emptiness, tiny low-content tables, unseparated title/body text, disconnected lines, wrong diagram type, occlusion, or raw-wireframe appearance.
