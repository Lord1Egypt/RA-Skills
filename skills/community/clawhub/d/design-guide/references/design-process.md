# Design Process

Read this reference for new screens, major redesigns, ambiguous visual direction, workflow changes, or any task where implementation would make the design expensive to reconsider.

## Choose The Design Depth

Use the lightest process that resolves the real uncertainty.

- **Level 0 - Direct fix:** Use for isolated styling, copy, spacing, or component-state corrections. Preserve the existing design contract and implement directly.
- **Level 1 - Directed design:** Use when the product structure and visual language already exist. Write a concise design brief and layout/state outline, then proceed unless the user requested review.
- **Level 2 - Exploratory design:** Use for new products, new major screens, information-architecture changes, brand-defining pages, major redesigns, or competing plausible directions. Produce a reviewable artifact and obtain confirmation before full implementation.

Raise the level when uncertainty or reversal cost is high. Do not lower it merely to avoid asking for a decision.

## Produce The Design Brief

Define these items before choosing visual details:

- Product role and target audience.
- Primary job the user is trying to complete.
- Most frequent or highest-value workflow.
- Content and actions that deserve first, second, and third visual priority.
- Required routes, regions, states, and breakpoints.
- Existing brand, technical, accessibility, and content constraints.
- Observable success criteria for the design.

Keep the brief concise. Surface assumptions that would materially change the result.

## Map Structure And Flow

For Level 1, provide a compact page outline and name the important states.

For Level 2, show the primary flow and information architecture before polishing visuals. Include entry, main action, completion, empty, loading, error, and recovery paths when relevant.

Use a flow diagram only when it makes branching or state transitions easier to understand. Use a wireframe when region hierarchy or responsive behavior is the main question.

## Explore Directions

Create alternatives only when they represent meaningful choices. Vary hierarchy, density, navigation, interaction model, editorial tone, or visual language; do not present cosmetic color swaps as separate directions.

For each direction, state:

- The organizing idea.
- The user or product benefit.
- The main tradeoff.
- The reference anchors.
- Why it fits or conflicts with the design brief.

Recommend one direction. Do not force the user to compare more than three.

## Choose Review Artifacts

Create the lowest-cost artifact that can answer the open design question:

- Use a written layout outline for a narrow, well-understood screen.
- Use an ASCII or image wireframe for hierarchy and region placement.
- Use a standalone HTML prototype for responsive layout, interaction, density, or navigation.
- Use screenshots, a reference board, or a generated image for visual language, art direction, or asset-heavy pages.
- Use a motion prototype or short capture when timing and choreography are central.

Use representative domain content. Label placeholders and speculative assets. Do not present a polished mockup that hides unresolved workflow problems.

Store temporary review artifacts under `.codex/design/<design-id>/` by default. If the project has an established design-artifact location, use it instead. Read `references/artifact-presentation.md`, make the artifact immediately inspectable, and give the user a usable fallback URL or absolute path.

## Apply The Confirmation Gate

Require confirmation before full implementation when any of these is true:

- The user requested a preview, options, or approval step.
- The task is Level 2.
- The design changes navigation, information architecture, or a primary workflow.
- Two or more materially different directions remain credible.
- Brand-defining visuals or expensive custom assets would be difficult to reverse.
- A review artifact was presented specifically for user judgment.

When the gate applies:

1. Present the artifact through an opened browser, attached media, or another immediately usable review surface.
2. Ask the user to approve, choose an option, or describe changes.
3. Stop implementation while that decision is pending.
4. Incorporate the response and restate the approved design contract before continuing.

Do not create artificial pauses for Level 0 work, a precisely specified screenshot recreation, an existing locked design system, or work where the user explicitly authorizes autonomous design decisions. If a supposedly locked direction conflicts with the product goal or accessibility, surface the issue instead of silently following it.

## Lock The Design Contract

After approval, record the decisions that implementation must preserve:

- Page structure and primary workflow.
- Chosen direction and reference anchors.
- Color, typography, spacing, radius, elevation, icon, and motion rules.
- Responsive behavior and important states.
- Accepted tradeoffs and rejected alternatives.

Treat later implementation discoveries as design changes when they alter this contract. Return to the user only when the change is material; resolve small execution details autonomously.
