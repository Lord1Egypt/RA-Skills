---
name: find-love
description: Create, publish, and search a consent-first public dating intent using showme/v1 and the datecli registry. Use when someone wants to find a romantic partner or draft a public dating profile; do not use for private outreach, impersonation, or covert matching.
---

# Find Love

Help the user publish a small, honest, public dating intent that people and AI agents can discover. The user owns the profile and controls where it is published; the registry is an index, not a dating platform or a private-data store.

## Workflow

1. Establish the user's goal, city or remote preference, relationship intent, and the public contact method they are comfortable disclosing. Do not infer sensitive details.
2. Draft a concise card using the `dating` intent in [intent-card.md](references/intent-card.md). Ask the user to verify every public field before any publication.
3. When `datecli` is available, generate the base card with `datecli init` and `datecli showme init`; add the optional `intents` block to `~/.datecli/showme/profile.json`, then run `datecli showme validate <path>`.
4. Publish only to targets the user authorizes. The lowest-cost default is a pull request to `dongsheng123132/showme-registry`; use `datecli showme register --type github` for the exact file path. A personal static page can host the same `profile.json`.
5. For discovery, sync the public index with `datecli findme sync`, filter locally, and explain why a candidate may fit. Never claim compatibility is certain.

## Publication Rules

- Treat the card as public and durable. Exclude legal names, home or work addresses, ID numbers, private photos, passwords, API keys, and contact details the user does not want searchable.
- State only voluntary, lawful, adult-to-adult dating intent. Do not help target minors, evade consent, harass people, or scrape closed platforms.
- Use a contact method with a clear boundary, such as a dedicated email address or public social profile. Do not expose a private chat identifier by default.
- Do not send messages, create accounts, open pull requests, or publish to any platform until the user explicitly approves that external action.
- Keep `showme/v1` required fields intact. In this dating-only registry, any optional `intents` entry must use `kind: "dating"`; professional needs belong in the separate BossCLI Registry.

## Output Quality

Write in the user's natural tone. Describe who they are, what kind of relationship they seek, a few real shared-interest hooks, and practical boundaries. Prefer specific, verifiable details over marketing language. Give the user a short final preview of the exact public text and target URLs before publishing.
