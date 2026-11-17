# Storyboard

Storyboard connects Content Lock to the later Manifest/PPT IR. It records page-level expression planning without assuming every slide is a judgment slide.

## Deck Planning Context

- Source:
- Source rights: owned / licensed / external-reference / unknown
- Audience:
- Purpose:
- Presentation context:
- Usage boundary: private draft / internal review / public sharing / client delivery / training / publication
- Export target:
- Production profile: fast | standard | premium
- Core thesis:
- Style contract ref:
- Source coverage target:

## Visual Design Brief

- Article type:
- Formality target:
- Brand posture:
- Core metaphor:
- Emotional temperature:
- Visual density:
- Evidence mode:
- Audience posture:
- Chosen archetype family:
- Brand system:
- Dominant background family:
- Contrast mode, if any:
- Rejected visual directions:

## Slide Plan

### S01

- Slide role: cover
- Title role: navigation
- Working title:
- Judgment: not applicable
- Audience question:
- Message:
- Primary expression: conceptual_scene
- Primary expression reason:
- Supporting expressions:
  - caption
- Primary anchor:
- Page archetype: cover-hero
- Density: low | medium | high
- Density reason:
- Relationship triggers:
- Data triggers:
- Source coverage:
- Editable core:
- Visual component plan:
- Raster allowance:
- Candidate delivery route:
- Split condition:
- QA expectations:
- Delivery note:

### S02

- Slide role:
- Title role:
- Working title:
- Judgment: not applicable unless `title_role=judgment`
- Audience question:
- Message:
- Primary expression:
- Primary expression reason:
- Supporting expressions:
- Primary anchor:
- Page archetype:
- Density: low | medium | high
- Density reason:
- Relationship triggers:
- Data triggers:
- Source coverage:
- Editable core:
- Visual component plan:
- Raster allowance:
- Candidate delivery route:
- Split condition:
- QA expectations:
- Delivery note:

## Compact Table Option

For short decks, the same fields may be recorded as a table:

| ID | Slide role | Title role | Working title | Audience question | Message | Primary expression | Supporting expressions | Primary anchor | Page archetype | Density | Source coverage | Delivery note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S01 | cover | navigation |  |  |  | conceptual_scene | caption | hero visual | cover-hero | low | src-01 | native title + generated hero |

## Required Fields

Every slide must include:

- `slide_role`
- `title_role`
- `message`
- `primary_expression`
- `primary_expression_reason`
- `supporting_expressions`
- `primary_anchor`
- `density_reason`

Keep these fields when relevant:

- `audience_question`
- `page_archetype`
- `source_coverage`
- `editable_core`
- `visual_component_plan`

## Deprecated Legacy Fields

Do not use these as forward fields:

- `judgment_title` as a universal required field
- `expression_mode`
- `hybrid_panel`

Compatibility field:

- `legacy_expression_mode` may be retained for one migration cycle, but it is deprecated and must map to `primary_expression` before build.

## Storyboard Review

- [ ] Every slide has one `primary_expression`.
- [ ] Supporting expressions do not compete with the primary anchor.
- [ ] Every judgment slide has an evidence-supported judgment.
- [ ] Navigation and section slides do not manufacture conclusions.
- [ ] Relationship-heavy content has not defaulted to generic cards.
- [ ] Density has a stated reason.
- [ ] The chosen archetype matches the audience question.
- [ ] Source coverage remains complete.
- [ ] `legacy_expression_mode`, if present, is marked deprecated and migrated before build.

## Verification Planning

- HTML preview: required / optional / not available
- PPTX render: required / optional / not available
- Readback: required / optional / not available
- Text overflow check:
- Brand consistency check:
- Captions and reconstruction labels:
- Redactions:
- Remaining limits:
