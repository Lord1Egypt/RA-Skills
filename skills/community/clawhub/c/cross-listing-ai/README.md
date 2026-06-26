# Cross Listing AI

`Cross Listing AI` is a docs-only OpenClaw skill repository for a listing AI that turns seller photos into priced, marketplace-ready listings and copy-paste-ready listing descriptions.

The repo keeps the skill prompt, agent metadata, and reference material together in one place.

## What The Skill Does

- turns item photos into a hidden reviewed-item record
- uses freeform clarification to resolve identity, condition, and completeness
- suggests a price from live comps, with heuristics only as fallback
- generates copy-paste-ready listings for eBay, Mercari, Facebook Marketplace, Craigslist, and TCGPlayer
- keeps TCGPlayer gated on card-specific fields

The required phase flow is:

`intake -> extract -> clarify -> price -> confirm -> generate -> revise`

## Repo Contents

- [`SKILL.md`](./SKILL.md): root skill instructions and reference routing
- [`agents/openai.yaml`](./agents/openai.yaml): agent metadata for environments that consume OpenAI-style skill descriptors
- [`references/workflow.md`](./references/workflow.md): end-to-end seller flow and hidden reviewed-item record
- [`references/extraction.md`](./references/extraction.md): image extraction and clarification guidance
- [`references/pricing.md`](./references/pricing.md): live comp and pricing guidance
- [`references/final-output.md`](./references/final-output.md): seller-facing response shape
- marketplace-specific output rules under `references/marketplaces/`
- [`references/examples.md`](./references/examples.md): compact sequencing examples

## How To Use The Skill

Start with [`SKILL.md`](./SKILL.md). Use `$cross-listing-ai` when you want the agent to turn item photos into a price suggestion and marketplace-ready listings. The skill tells the agent:

- what the non-negotiable rules are
- which reference file to open at each phase
- how to keep the reviewed-item record internal
- when to block or skip TCGPlayer

The references are meant to be opened progressively, not all at once. `SKILL.md` is the router; the files under `references/` supply the operational detail.

## Core Constraints

- Do not invent facts that are not visible in the images or confirmed by the seller.
- Keep the reviewed-item record internal and seller-facing responses conversational.
- Use live comps first for pricing, with heuristics only when market data is thin.
- Only generate TCGPlayer output when `card name`, `game`, and `set` are known.

## Publishing

Publishing expects a clean git tree.

- ClawHub: install and authenticate `clawhub`, then run `npm run publish:clawhub -- 0.1.0` or `scripts/publish-clawhub.sh 0.1.0`
- skills.sh: from a clean local `main` checkout that already matches `origin/main`, run `npm run publish:skills` or `scripts/publish-skills.sh`
- Both: from that same pushed `main` state, run `npm run publish:all -- 0.1.0` or `scripts/publish-all.sh 0.1.0`

skills.sh uses the GitHub-backed default branch as the install target, so this command validates that pushed state and the install command rather than uploading a separate package.

Optional positional arguments for the ClawHub entrypoint are `[changelog] [tags]`.

## License

Cross Listing AI is released under the terms in [`LICENSE`](./LICENSE).
