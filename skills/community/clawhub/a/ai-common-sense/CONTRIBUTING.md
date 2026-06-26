# Contributing to AI Common Sense

Model information gets stale fast. Your contributions keep this reference accurate.

## What to Contribute

- **New model releases** — A provider launched a new model
- **Pricing changes** — API pricing was updated
- **Deprecations** — A model was deprecated or shutdown date announced
- **Corrections** — You found an error in our reference
- **New providers** — A major AI provider we don't cover yet

## How to Submit an Update

### Option 1: Open an Issue

If you found an error or a new model was released but don't want to edit files:

1. Open an Issue
2. Include: what changed, the source URL, the date you verified it

### Option 2: Submit a PR

1. Fork the repo
2. Edit the relevant file in `references/` (one file per provider)
3. Follow the format below
4. Submit a PR with a clear title (e.g., "Update OpenAI: add GPT-5.5")

## Format Requirements

### For model entries in `references/*.md`

Every model entry must include:
- **Model name** — Official name from the provider
- **API ID** — The exact string used in API calls
- **Release date** — When it became generally available
- **Pricing** — Per million tokens (input and output separately)
- **Source** — Where you verified this information

### Update the "Last verified" date

At the top of each `references/*.md` file:

```markdown
> Last verified: YYYY-MM-DD
> Source: [official docs URL]
```

Update this date when you verify or change information.

### For the Quick Reference in SKILL.md

If a model is important enough for the quick reference table (top ~15 models), also update `skills/ai-common-sense/SKILL.md`.

## Quality Standards

- **Official sources preferred** — Provider docs, blog posts, pricing pages
- **Third-party sources acceptable** — When official sources don't exist (e.g., xAI)
- **No speculation** — Don't add unannounced models. "Upcoming" section is for officially announced models only.
- **Exact API IDs** — Test them if possible. `gpt-5.4` and `GPT-5.4` are different strings.
- **Date everything** — Every piece of information should have a verification date.

## What NOT to Contribute

- Benchmark comparisons (too subjective and volatile)
- Opinion on which model is "best"
- Unverified rumors about upcoming models
- Marketing claims without technical substance
