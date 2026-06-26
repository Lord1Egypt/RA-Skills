# Safety

This template is intentionally conservative.

## Defaults

- Draft first
- Review first
- Publish only after explicit approval
- Treat deletion as high risk

## Publish Guardrails

- Require exact title confirmation
- Require existing login state or cookies you already control
- Validate success by success page or content-list check

## Deletion Guardrails

- Preview first
- Match exact title and publish time
- Do not rely on fuzzy matching

## Current Limitation

For many Xiaohongshu creator pages, `archive back to draft` is not stable enough to treat as a default capability.

If you share this repo publicly, describe deletion conservatively:

- preview and identify precisely
- only perform live delete after explicit confirmation
