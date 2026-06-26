# Biotech BP Architect

Install this folder as an OpenClaw skill.

## Contents
- `SKILL.md`: main skill definition
- `README.md`: usage notes

## What this skill does
Biotech BP Architect helps users build and critique biotech fundraising decks and business plans from user-owned, user-authorized, or public materials.

It is designed for work such as:
- non-confidential first-look investor decks
- non-confidential first-meeting decks
- confidential investor diligence decks
- strategic partner or BD decks

It can help users:
- turn scientific slides, notes, papers, and internal materials into an investor-ready story
- diagnose weak BP logic, weak evidence, and missing milestones
- choose slide order based on company type, stage, and strongest proof point
- separate confidential and non-confidential versions clearly
- rewrite scientific claims so they connect to investor meaning and financing logic

## What makes this skill useful
- It requires an audience and disclosure decision before drafting.
- It treats confidential and non-confidential decks as different outputs, not minor variants.
- It uses company type and stage to shape deck structure instead of forcing one generic template.
- It helps translate science into investor-readable logic without pushing unnecessary disclosure.
- It flags missing evidence, weak differentiation, and unclear milestone logic early.

## Source and privacy boundary
Use this skill only with materials that the user owns, is authorized to share, or that are already public.

Do not use this skill to extract, summarize, or reproduce non-public third-party information, including:
- internal decks or diligence materials
- unpublished datasets or research updates
- internal timelines, milestone plans, or program reviews
- non-public deal terms, licensing economics, or cap-table details
- unannounced partners, investors, or customers
- proprietary assay conditions, screening workflows, manufacturing details, or other trade secrets

Do not unnecessarily include:
- patient-level or subject-level data
- names of investigators, trial sites, hospitals, or sample providers unless already public and necessary
- personal contact details
- employee personal details beyond role and public biography
- traceable technical identifiers such as accession numbers, sequence-level details, or batch numbers unless already public and necessary

When using reference materials, extract structure and logic only. Do not reproduce wording, numbers, figures, layouts, or clues that could identify a non-public source.

## Reliability boundary
This skill should not invent or overstate missing facts.

It should not fabricate or imply certainty about:
- datasets, results, or validation status
- regulatory interactions or agency feedback
- partnership status, investor interest, customer traction, or endorsements
- IP status, freedom-to-operate conclusions, or legal certainty
- timelines, milestones, development plans, or use-of-proceeds details that the user did not provide

It should label hypotheses, early signals, internal data, animal data, planned studies, and working assumptions clearly.

## Typical use cases
Use this skill when the user wants to:
- write a biotech investor deck or BP from scratch
- improve an existing fundraising deck
- turn scientific materials into a financing narrative
- decide whether a deck should be confidential or non-confidential
- get a page-by-page outline with key claims, evidence needs, and rewrite suggestions
- compare a draft against public or user-authorized reference patterns

Do not use this skill for:
- pure scientific paper writing
- clinical protocol writing
- legal review
- grant-only writing unless investor logic is also needed
- detailed financial modeling beyond high-level financing logic

## Expected workflow
The skill will usually:
1. confirm source status, audience, disclosure level, company type, stage, and raise objective
2. decide whether the output should be non-confidential, confidential, or split into separate versions
3. identify the core thesis and strongest proof point
4. build a page-by-page investor narrative
5. flag weak logic, missing evidence, disclosure mistakes, and unsupported claims

## Output style
Typical output includes:
- recommended deck version
- core thesis sentence
- audience and disclosure recommendation
- recommended slide order
- page-by-page logic
- missing evidence or weak logic
- rewrite suggestions
- open founder questions that should be answered before sending the deck

## Suggested directory structure
biotech-bp-architect/
- `SKILL.md`
- `README.md`