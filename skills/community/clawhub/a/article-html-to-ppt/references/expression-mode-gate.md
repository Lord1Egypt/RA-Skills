# Expression Mode Gate

Use this gate before `storyboard.md` or `ppt-ir.json` is finalized. It decides how each slide expresses its message without assuming every slide must be a judgment slide.

## Forward Contract

Every slide must choose exactly one `primary_expression`.

A slide may also declare zero or more `supporting_expressions`, but supporting expressions must remain visually subordinate and must not create a second primary anchor.

Forward fields:

```text
title_role
primary_expression
primary_expression_reason
supporting_expressions
audience_question
primary_anchor
```

For relationship visuals and conceptual scenes, also define:

```text
visual_component_plan
visual_component_delivery
```

## Primary Expressions

Allowed `primary_expression` values:

- `textual_argument`
- `structured_cards`
- `table_matrix`
- `data_visual`
- `relationship_visual`
- `conceptual_scene`

## Supporting Expressions

Allowed `supporting_expressions` values:

- `interpretation`
- `kpi`
- `source_note`
- `risk_callout`
- `legend`
- `caption`
- `supporting_image`

Supporting expressions clarify, label, qualify, evidence, or interpret the primary expression. They must not duplicate the primary component or create a second storyline.

## Deprecated Legacy Fields

Deprecated:

```text
expression_mode
expression_mode_reason
hybrid_panel
```

`hybrid_panel` is no longer a primary expression. It was a page-composition pattern: a primary visual plus supporting explanation.

Migration examples:

```text
hybrid_panel with a chart and commentary
-> primary_expression: data_visual
-> supporting_expressions: [interpretation]

hybrid_panel with architecture and risk note
-> primary_expression: relationship_visual
-> supporting_expressions: [risk_callout]
```

During migration, `legacy_expression_mode` may be recorded for traceability, but new work must use `primary_expression`.

## Selection Order

Step 1: What question does the audience need answered?

Step 2: What evidence or relationship best answers it?

Step 3: Which expression preserves that evidence most directly?

Step 4: What minimal supporting expression is necessary?

Step 5: Can the slide still maintain one primary anchor?

## Title Role Is Independent

`title_role` and `primary_expression` are independent decisions.

Examples:

- a section slide may use `title_role=section` and `primary_expression=conceptual_scene`;
- a data slide may use `title_role=judgment` and `primary_expression=data_visual`;
- an agenda slide may use `title_role=navigation` and `primary_expression=structured_cards`.

Do not invent a judgment title for a section, navigation, reference, instruction, cover, or closing slide.

## Core Question

What must the audience understand or decide after this slide?

- If they must believe one claim and two or three proof points are enough, use `textual_argument`.
- If they must compare parallel items, use `structured_cards` or `table_matrix`.
- If they must perform exact lookup or comparison, prefer `table_matrix`.
- If they must understand magnitude, trend, ranking, contrast, distribution, or composition, use `data_visual`.
- If they must understand how parts connect, influence, route, depend, govern, loop, exchange value, or cross boundaries, use `relationship_visual`.
- If they must remember or feel an abstract idea, use `conceptual_scene`.

## Do Not Default To Cards

Do not choose `structured_cards` merely because the source contains three or four paragraphs.

Prefer `relationship_visual` when meaning depends on:

- sequence;
- dependency;
- ownership;
- handoff;
- approval;
- data flow;
- control flow;
- trust boundary;
- feedback;
- hierarchy;
- cause and effect.
- state transition;
- multi-party relationship.

Prefer `table_matrix` when the audience must perform exact lookup or comparison.

Prefer `textual_argument` when one claim and two or three proof points are enough.

## Relationship-Visual Strong Triggers

Classify as `relationship_visual` when the source contains one strong trigger:

1. Many-to-many relationships.
2. Directional flow.
3. System, ownership, security, data, organization, or trust boundaries.
4. Feedback loops or flywheels.
5. Ecosystem or stakeholder structure.
6. Causal chains.
7. Architecture or operating model.
8. Spatial metaphor carrying meaning.

## Relationship-Visual Medium Triggers

Classify as `relationship_visual` when two or more are true:

1. Relationship verbs dominate: connects, routes, depends, triggers, loops, governs, orchestrates, integrates.
2. Prose repeats `A affects B`, `B depends on C`, or `actor -> action -> system` patterns.
3. The same entities recur across multiple paragraphs with changing roles.
4. Prose needs several sentences before the relationship is understandable.
5. A table hides the main insight because interaction matters more than cell values.
6. Cards would falsely imply the items are parallel.
7. A reader would ask how things connect, who controls what, or where data goes.
8. Risk, security, control, ownership, or trust boundaries are essential.

## Anti-Misclassification Rules

Do not choose `textual_argument` merely because the source is prose. Articles often encode relationships in paragraphs.

Do not choose `structured_cards` merely because there are 4-8 named items. If those items depend on, route to, control, reinforce, or constrain each other, use `relationship_visual`.

Do not choose `table_matrix` merely because attributes repeat. If the point is interaction or flow, the table is secondary evidence, not the primary anchor.

Do not choose `relationship_visual` for decorative diagrams. If the audience can understand faster through a two-column contrast, chart, or card group, use the simpler editable structure.

## Visual Component Plan

Slides with `relationship_visual` or `conceptual_scene` must define:

- `component_type`
- `audience_question`
- `primary_entities`
- `relationship_types`
- `simplification_strategy`
- `editable_core`
- `visual_component_delivery`
- `raster_acceptance_reason` when using generated or raster output

For `relationship_visual`, also create or reference a valid Diagram IR before build:

```text
diagram_ir_ref OR diagram_ir
diagram_type
nodes
groups
edges
main_paths
boundaries
layout_constraints
delivery_contract
```

Do not let a Builder draw directly from prose. If the content depends on sequence, dependency, ownership, handoff, approval, data flow, control flow, cause/effect, feedback, hierarchy, boundary, state transition, or multi-party relationships, the relationship semantics must live in Diagram IR first.

## Default Diagnostic Budgets

These are default diagnostic budgets, not universal hard limits:

- simple relationship page: 3-9 meaningful connectors
- normal architecture page: up to 8 primary nodes
- normal KPI page: up to 4 KPI cards
- normal image-supported page: up to 3 images
- normal table page: up to 5x6 visible cells

Escalate based on context:

```text
budget_severity:
  within_budget: pass
  moderately_over_budget: warning
  severely_over_budget_with_clear_structure: review
  severely_over_budget_without_clear_structure: fail
```

Budget interpretation depends on:

- `slide_role`
- `page_archetype`
- `presentation_context`
- `audience`
- `content_complexity`
- `physical_slide_size`

Examples:

- A normal body slide with 11 connectors usually warrants a warning.
- An architecture slide whose only primary anchor is a relationship map may legitimately need 11 connectors.
- Any slide still fails when connectors cross heavily, pass through nodes, or leave the main path unclear.

## Delivery Priority

1. Use editable PPT when the relationship can be simplified into a clean lane, group, layer, issue tree, or architecture map.
2. Use SVG/HTML render for deterministic complex diagrams.
3. Use generated or rasterized localized components for complex ecosystems, soft boundaries, conceptual scenes, dense architecture murals, or spatial metaphors.
4. If image generation is unavailable, split the slide or simplify into editable groups.

## Verification

The verification report must list relationship and conceptual slides and confirm planned delivery route, editable core, bounded raster use, and why simpler editable alternatives were accepted or rejected.
