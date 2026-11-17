# Generation models and Effects

Use stable BeatAPI model IDs only. Discover the current catalog before choosing
a model; never expose or invent internal provider routes.

## Image and video models

Call `beatapi_list_generation_models` or `GET /v1/media/models` before
generation. Choose only an ID from the current response, then consult
`beatapi.openapi.yaml` for the exact request variant and validation rules.

Model availability evolves independently from this Skill. Do not hardcode a
closed model list in agent logic, and do not substitute a similar model without
the user's approval. Preserve the selected model ID exactly.

Copy `assets/image-generation.json` or `assets/video-generation.json` to a
temporary request. Add only fields accepted by that model's schema. In
particular, do not combine frame images with reference inputs when the selected
model forbids it, and satisfy any audio-reference dependency before creating a
paid task.

## Effects

Effects are versioned published capabilities, not model aliases.

1. List active Effects with `beatapi_list_effects` or `beatapi effects list`.
2. Read the selected Effect with `beatapi_get_effect` or
   `beatapi effects get EFFECT_ID`.
3. Validate image count, MIME types, dimensions, subject requirements, and
   supported options against that returned version.
4. Copy `assets/effect-task.json`, preserve the selected `effect_id`, and omit
   unsupported options.
5. Create with `beatapi_create_effect` or `beatapi effects create --file ...`.
   Use one stable idempotency key for retries of the same request.
6. Poll the shared task endpoint and require hosted output before reporting
   completion.

The catalog exposes only publication-safe fields. Never infer provider names,
template IDs, internal costs, or execution context.
