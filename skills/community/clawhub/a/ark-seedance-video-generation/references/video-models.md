# Video Models

Use this file when the agent needs to present model choices before generation.

The canonical machine-readable source is `references/video-models.json`.

## Selection Rule

Use only the two approved model IDs in this skill package.

Approved choices:

- `doubao-seedance-1-0-pro-250528`
- `doubao-seedance-2-0-260128`

Default model:

- `doubao-seedance-1-0-pro-250528`

Before generation:

1. If the user already specified one of the two approved IDs, use it.
2. If the user did not specify a model, the agent workflow should default to `doubao-seedance-1-0-pro-250528` and pass it explicitly with `--model`.
3. The script itself does not provide a default model.
4. Do not use any model outside the approved pair unless the skill package is intentionally updated.

## Representative Model Set

- `doubao-seedance-2-0-260128` -> Seedance 2.0
- `doubao-seedance-1-0-pro-250528` -> Seedance 1.0 Pro

## Agent Workflow

- If no explicit model was provided by the user, the agent should explicitly pass `--model doubao-seedance-1-0-pro-250528`.
- Keep this approved-model restriction at the skill or agent workflow layer. The bundled script is a generic runner and should not enforce this pair.
- Present these two model IDs from this reference file or `references/video-models.json`, not from a script command.

## Source Notes

- `doubao-seedance-2-0-260128` is present in the official Ark create-task API example.
- `doubao-seedance-1-0-pro-250528` is listed in the official LAS Seedance supported model section.
