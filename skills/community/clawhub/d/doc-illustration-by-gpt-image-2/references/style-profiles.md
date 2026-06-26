# Style Profiles

## `flat-tech-infographic` (default)

- Best for technical docs, AI notes, and repo architecture inserts
- Flat shapes, clean grouping, and icon-assisted modules
- Soft but professional colors
- Readable bilingual labels
- Balanced whitespace

## `flat-illustration`

- Best for concept explanation with lighter technical density
- More decorative than the default
- Still keep labels short and structured

## `sketchnote`

- Best for study notes, tutorial summaries, and prompt-engineering cards
- Hand-drawn accents, notebook feel, softer linework

## `soft-tech-diagram`

- Best for architecture, system boundaries, and knowledge graphs
- Gentle technical diagram feel
- Dashed containers and subtle node relationships

## `repo-architecture-clean`

- Best for codebase structure and ownership diagrams
- Minimal decoration
- Crisp block hierarchy
- Strong spacing and labeling discipline

## Style selection rule

- If the user explicitly names a style profile, use it.
- If the user provides a reference image, use the reference image to adapt the selected profile.
- If the user does not specify a style, use `flat-tech-infographic`.
