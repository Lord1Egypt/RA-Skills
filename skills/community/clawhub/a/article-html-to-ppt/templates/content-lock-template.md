# Content Lock

Content Lock records what the deck is allowed to say before layout and implementation decisions are made. Do not use this template to lock coordinates, card counts, font sizes, colors, connector styles, SVG routes, or native implementation details.

## Deck Context

- Source:
- Source rights: owned / licensed / external-reference / unknown
- Audience:
- Purpose:
- Presentation context:
- Usage boundary: private draft / internal review / public sharing / client delivery / training / publication
- Export target:
- Core thesis:
- Required source sections:
- Known assumptions:
- Sensitive or uncertain claims:
- Items that must not appear in slide-visible text:

## Slide Content Locks

### S01

- Slide role: cover
- Title role: navigation
- Working title:
- Audience question:
- Message:
- Judgment: not applicable
- Evidence:
  - Evidence item:
    - Type: direct | inferred | assumption
    - Source:
    - Locator:
    - Supports:
    - Confidence:
- Source references:
- Inferences:
- Assumptions:
- Must-keep terms:
- Must-not-overclaim:
- Relationship clues:
- Data clues:
- Candidate split:
- Coverage status: locked | review | missing

### S02

- Slide role:
- Title role:
- Working title:
- Audience question:
- Message:
- Judgment: not applicable unless `title_role=judgment`
- Evidence:
  - Evidence item:
    - Type: direct | inferred | assumption
    - Source:
    - Locator:
    - Supports:
    - Confidence:
- Source references:
- Inferences:
- Assumptions:
- Must-keep terms:
- Must-not-overclaim:
- Relationship clues:
- Data clues:
- Candidate split:
- Coverage status: locked | review | missing

## Field Rules

- `Slide role` describes the page duty: cover, agenda, section, body, data, diagram, reference, closing, or another explicit role.
- `Title role` describes what the title is doing: `judgment`, `navigation`, `section`, `instruction`, `reference`, or `closing`.
- `Judgment` is required only when `Title role` is `judgment`.
- Non-judgment pages must not invent conclusions merely to satisfy a title rule.
- `Message` is required for every slide, including navigation and section slides.
- `Relationship clues` and `Data clues` preserve signals for later expression selection; they do not choose layout.

## Content Lock Gate

- [ ] Every slide has a `slide_role`.
- [ ] Every slide has a `title_role`.
- [ ] Judgment is present only when required.
- [ ] Every slide has a `message`.
- [ ] Every major claim has a direct, inferred, or assumption label.
- [ ] No required source section is silently omitted.
- [ ] Relationship clues are preserved for Expression Mode selection.
- [ ] Data clues are preserved for chart/table decisions.
- [ ] Dense paragraphs have been decomposed into semantic units.
- [ ] No coordinates, card counts, font sizes, colors, connector styles, SVG routes, or native implementation routes are locked here.

## Legacy Migration Notes

- `judgment_title` -> `working_title` + `title_role`; add `judgment` only when `title_role=judgment`.
- `Locked title` -> `Working title` until the storyboard locks the final title.
- `One-message takeaway` -> `Message`.
- `Source evidence` -> structured `Evidence` + `Source references`.
