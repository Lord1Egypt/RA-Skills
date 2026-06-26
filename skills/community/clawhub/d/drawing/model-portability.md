# Model Portability — Drawing

This skill is model-agnostic on purpose. The base prompt should stay reusable even if the user switches providers.

## OpenClaw

If the user wants generation inside OpenClaw:
- keep the prompt provider-neutral first
- rely on the active image model if one is already configured
- if needed, check model status and set an image fallback with the OpenClaw models command

Useful commands:

```bash
openclaw models status
openclaw models set-image <provider/model>
```

Do not block on configuration if the user only wants prompts.

## GPT Image

Works well with natural-language prompts and iterative edits.

Best moves:
- use the full prompt scaffold in plain language
- keep must-have and must-avoid constraints explicit
- for refinements, restate the invariants you want preserved
- for series consistency, reuse the same anchor block every turn

## Gemini / Nano Banana Style Workflows

These respond well to a clear sequence:
- subject
- context
- style
- composition
- negative constraints

Keep the prompt crisp. Too many stacked modifiers can lower control.

## Cross-Model Survival Rules

- Avoid provider-specific syntax in the reusable master prompt.
- Keep one master version and small adapters per provider.
- If a model handles text badly, remove text from the image and solve labeling outside the generation step.
- When switching providers, preserve the subject, style pack, and constraint block before changing anything else.

## When a Model Is Expensive

If the user cares about cost:
- draft the prompt in one cheap pass
- remove ambiguity before generating
- prefer one strong prompt plus one refinement instead of many random tries
- reduce scene complexity before paying for more attempts
