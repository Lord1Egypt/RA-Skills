---
name: floracat-architecture-diagram
description: Create or revise standalone HTML/SVG architecture diagrams, runtime flow diagrams, sequence diagrams, and PPT-like technical visuals. Use when a user wants human-readable publication-ready diagrams instead of Mermaid, or wants help improving node layout, arrow accuracy, spacing, overlap handling, Chinese labels, or overall visual style for architecture and flow charts.
---

# Architecture Diagram HTML/SVG

Use this skill to produce standalone HTML files with embedded SVG diagrams that feel like clean presentation slides rather than code-first diagrams.

## Output Form

- Default to a standalone HTML file with embedded SVG.
- Prefer sectioned “deck” structure when there are multiple diagrams on one page.
- Use SVG, not Mermaid, for final publication-quality layout control.
- Make the result readable without zooming and understandable by non-engineers.

## Visual Style

- Use a PPT-like information design style: warm background, panel cards, soft shadows, rounded nodes, restrained colors.
- Prefer clear Chinese labels when the audience is Chinese-speaking; keep only essential English technical terms.
- Use a small set of semantic colors and keep them consistent across sections.
- Keep arrowheads understated; do not make lines or markers visually aggressive.
- Favor balanced spacing over dense packing. The page should feel edited, not auto-generated.

## Diagram Building Workflow

1. Identify the user-facing purpose of each diagram.
2. Reduce the system into a few layers or stages before drawing.
3. Choose the simplest SVG structure that fits:
   - layered architecture
   - runtime flow
   - sequence/timing flow
   - subsystem drill-down
4. Place groups first, then nodes, then arrows, then notes.
5. After layout is stable, localize labels and tighten wording.
6. Do a dedicated arrow and overlap review before finishing.

## Node Rules

- Give every node one clear responsibility.
- Keep titles short; if a title is long, widen the node before shrinking text.
- Use subtitle lines for detail; keep them short and scannable.
- Avoid mixing multiple abstraction levels inside one node.
- Align sibling nodes rigorously.

## Arrow Rules

- Every arrow must start and end on a node edge, not inside a node.
- Prefer straight lines first. Add bends only to avoid collisions or ambiguity.
- When two arrows connect the same pair of areas, offset them vertically or horizontally.
- Use solid lines for primary runtime/data flow.
- Use dashed lines only for support, configuration, feedback, optional linkage, or on-demand reads.
- If arrows are long, shorten or reroute them so the direction remains obvious.
- Do not let text sit on top of an arrow.

## Editing Rules

- When refining an existing SVG, inspect coordinates instead of making semantic guesses.
- If a user reports overlap, fix geometry directly: move nodes, widen boxes, reroute paths, or adjust text anchors.
- If a user questions arrow meaning, verify the actual system relationship in code/docs first, then correct the line.
- Prefer explicit labels over decorative complexity.

## Diagram-Specific Guidance

### Overall Architecture

- Separate access surfaces, control plane/runtime, capability subsystems, and state/config areas.
- Use enclosing groups to show ownership or subsystem boundaries.
- Keep cross-group arrows sparse and precise.

### Runtime Flow

- Emphasize the main path first.
- Put configuration, session state, and plugin/runtime support below the main path as supporting layers.
- Use wording that reads like product behavior, not source code names, unless the source name is important.

### Sequence Diagram

- Reduce participants to the minimum needed to explain the flow.
- Name participants by role, not by file/module, unless implementation detail is the point.
- Use loops only where a real repeated interaction exists.
- Move loop labels close to the loop arrow.

## Final Review Checklist

Before finishing, read [references/review-checklist.md](references/review-checklist.md) and verify every item.
