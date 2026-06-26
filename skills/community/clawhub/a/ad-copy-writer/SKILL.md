---
name: ad-copy-writer
description: Create, generate, convert, and polish ad copy, marketing copy, product copy, landing page copy, headline variants, CTA variants, and promotional messaging through the WeryAI chat completion API. Use when you need advertising copy, campaign copy, product messaging, launch copy, performance copy variations, or concise persuasive text for marketing channels.
metadata: { "openclaw": { "emoji": "🎯", "primaryEnv": "WERYAI_API_KEY", "paid": true, "network_required": true, "requires": { "env": ["WERYAI_API_KEY"], "bins": ["node"], "node": ">=18" } } }
---

# Ad Copy Writer

Write ad copy, marketing copy, product copy, headline variants, CTA variants, and promotional messaging that are concise, persuasive, and channel-aware. Use this skill when the user wants to draft, rewrite, or polish persuasive copy for ads, landing pages, launches, or campaigns.

## Prerequisites

- `WERYAI_API_KEY` must be set before calling the API.
- Node.js `>=18` is required because the runtime uses built-in `fetch`.
- Real runs use the WeryAI chat completion API and may consume credits.

## Example Prompts

- `Write 5 ad copy variations for a productivity app launch.`
- `Turn this product brief into landing page copy with a stronger CTA.`
- `Rewrite this ad so it sounds less generic and more benefit-driven.`
- `Draft short paid social copy for a skincare product in English.`

## Quick Summary

- Main jobs: `ad copy writing`, `marketing copy`, `landing page copy`, `headline variants`, `cta variants`, `promotional rewrite`
- Default model: `GPT_5_4`
- Main optional controls: `product`, `brand`, `audience`, `tone`, `format`, `cta`, `keywords`, `mustInclude`, `avoid`
- Main trust signals: dry-run support, model lookup, channel-aware preset, direct copy-ready output

## Workflow

1. Capture the product, offer, audience, channel, tone, and desired call to action.
2. If the user wants a specific ad shape such as headline set, landing page copy, CTA variants, or paid social copy, read [references/domain.md](references/domain.md) and match the closest pattern.
3. Ask only for the smallest missing detail needed to write persuasive copy.
4. Use `--dry-run` first when you want to inspect the final payload.
5. Run `node {baseDir}/scripts/write.js --json '...'` and return the final copy directly.

## Commands

```sh
# List available chat models
node {baseDir}/scripts/models.js

# Write ad copy
node {baseDir}/scripts/write.js --json '{
  "prompt":"Write 5 ad copy variations for a productivity app launch",
  "product":"AI productivity app",
  "audience":"busy professionals",
  "format":"paid social ad",
  "cta":"Start free trial"
}'

# Rewrite marketing copy without calling the API
node {baseDir}/scripts/write.js --json '{
  "prompt":"Rewrite this ad so it feels sharper and more benefit-driven",
  "sourceText":"...",
  "product":"skincare serum",
  "tone":"premium but clear"
}' --dry-run
```

## Definition of Done

- The final output reads like persuasive copy rather than a memo or explanation.
- The wording matches the requested channel, audience, and CTA closely enough to use as a draft.
- If the user asked for variations, the output clearly separates them.

## When Not to Use

- Do not use this for long-form articles or blog posts.
- Do not use this for pure translation without copy adaptation; use `copy-translator` instead.
- Do not use this for general brainstorming with no copy deliverable.

## Re-run Behavior

- Re-running `write.js` creates fresh copy variations and may consume additional credits.
- Re-running `write.js --dry-run` is safe and does not call the API.
- Re-running `models.js` is safe and only refreshes the available chat model list.

## Resources

- Ad copy patterns and channel guidance: [references/domain.md](references/domain.md)
