# Section Briefs

Do not write long-form sections directly from the source corpus. First create a section brief for each target section.

## Why this matters

Section briefs separate planning from prose. They reduce drift, repetition, and source misuse.

For multi-agent work, the section brief is the contract. A section without a brief is not ready to draft.

## Required fields

Each brief should include:

- `section_id`
- `section_title`
- `purpose`
- `must_cover`
- `primary_sources`
- `secondary_sources`
- `allowed_generic_material`
- `exclusions`
- `expected_tables_or_figures`
- `target_length`
- `open_questions`

## Drafting boundary

Use the brief to define what belongs in the section and what does not.

Examples:

- A technical design section may describe architecture, functions, deployment, and interfaces.
- A construction section may describe survey, installation, commissioning, and acceptance.
- A management section may use generic process content, but it still must not conflict with project facts.

## Suggested build order

1. Parse the target outline.
2. Create one brief per target section.
3. Fill in purpose and must-cover points first.
4. Attach sources next.
5. Add exclusions to prevent overlap.
6. Add figure or table slots only where they support the argument.

## Heuristics

- If a section has no clear primary sources, do not start drafting. Either narrow the scope or mark it as generic-support content.
- If two sections share the same factual center, assign one as the owner and let the other cross-reference in the working notes.
- If the user has a fixed template, preserve its chapter order and naming even when the source corpus is organized differently.

## Minimal brief template

```md
## {section_id} {section_title}

- Purpose:
- Must cover:
- Primary sources:
- Secondary sources:
- Allowed generic material:
- Exclusions:
- Expected tables or figures:
- Target length:
- Open questions:
```

## Tooling

Use [scripts/plan_sections.py](../scripts/plan_sections.py) to bootstrap brief stubs from a plain-text outline.
