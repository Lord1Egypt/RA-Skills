# Input Contract

## Supported Source Types

V0.1 accepts text-only inputs through `tools/source_normalizer.py`:

- `manual`: user notes or manually written summaries
- `wiki`: fandom wiki or encyclopedia-style summaries
- `quotes`: quote collections or direct dialogue snippets
- `plot`: plot summaries or event recaps

## Minimum Input

Each import should include:

- a source type
- a text file
- enough context to know which character the material belongs to

For intake-first generation, the minimum user-provided request bundle should include:

- source decision policy
- character name
- source work or an explicit decision that the character is fully original
- whether low-confidence persona inference is allowed when evidence is thin

If these fields are incomplete, the generator should ask follow-up intake questions before creating the child skill.
The generator should ask one unresolved intake question at a time instead of dumping the entire form in one message.
Already resolved slots must not be asked again unless the answer is ambiguous, conflicts with another answer, or the user explicitly changes it.
No character files should be created or modified before the user confirms the intake summary.

`target_use` is no longer a hard intake requirement.
If the user does not specify it, default to `openclaw roleplay conversation`.
`input_mode` is only required when the source decision policy includes user-provided materials.
If the source decision policy is `official_quick`, the generator should skip the rest of the intake questions and move to a generated draft preview before final confirmation.

## Normalized Shape

The normalizer outputs JSON with this structure:

```json
{
  "schema_version": "0.1",
  "source": {
    "source_type": "manual",
    "input_path": "path/to/source.txt",
    "normalized_at": "2026-04-09T00:00:00Z"
  },
  "entries": [
    {
      "entry_id": "manual-001",
      "text": "Character statement or paragraph",
      "kind": "note",
      "line_start": 1,
      "line_end": 3
    }
  ]
}
```

## Guidance

- Use one file per source import when possible.
- Preserve paragraph boundaries for plot and wiki text.
- Preserve line boundaries for quote collections.
- Do not pre-merge unrelated source files before normalization.
