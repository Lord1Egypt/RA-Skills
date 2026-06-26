# Report JSON Schema

Use this schema to build the input for `scripts/build_system_guidance_docx.py`.

## Required Fields

- `question` (string): User question or task objective.
- `sources` (array): At least one source object.
- `recommended_steps` (array): At least one recommended action.

## Optional Top-Level Fields

- `title` (string)
- `prepared_for` (string)
- `prepared_by` (string)
- `date` (string)
- `analysis_summary` (string)
- `assumptions` (array of strings)
- `validation_checks` (array of strings)
- `risks_open_items` (array of strings)
- `open_questions` (array of strings)
- `system_context` (object)
- `clarifications` (array)

## Source Object

- `title` (string)
- `publisher` (string)
- `url` (string)
- `published_or_updated` (string)
- `accessed` (string)
- `type` (string, example: `official-doc`, `consultant-article`)

## Recommended Step Object

Each step may be either a string or object.

Object form:

- `step` (string) or `action` (string)
- `rationale` (string, optional)
- `source_refs` (array, optional): Reference numbers aligned to source order (1-based)

## Clarification Item

Each item may be either a string or object.

Object form:

- `question` (string)
- `answer` (string)

## Minimal Example

See [example_report_input.json](example_report_input.json).
