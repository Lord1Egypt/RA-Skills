---
name: date-publisher
description: Prepare platform-specific drafts and publish an explicitly approved public adult dating profile from one canonical showme card. Use for authorized public distribution; do not use to create accounts, scrape apps, or send private outreach.
---

# Date Publisher

Turn one user-approved `showme/v1` dating card into a controlled distribution plan. Keep the canonical card as the source of truth and record every public URL created from it.

## Workflow

1. Read the canonical card and identify exactly which name, city, photo, biography, interests, and contact method are approved for this target. Do not reuse a contact method simply because it was public somewhere else.
2. Classify each target using [platform-modes.md](references/platform-modes.md). State whether the result is a draft, an assisted manual action, or a supported official API action.
3. Produce a short target-specific draft and a publication preview containing the exact text, links, images, visibility, and account that will be used.
4. Require an explicit per-target confirmation before creating an account, authorizing OAuth, opening a pull request, publishing a post, or sending a message. A broad request to "promote me everywhere" is not confirmation for an individual target.
5. After an approved action, record the public URL and date in the distribution log. Refresh or remove the post only with new authorization.

## Supported First Targets

- **GitHub Registry**: create or update the owner's `profiles/github/<username>.json` pull request in `dongsheng123132/showme-registry`.
- **Personal static page**: publish the same card as `profile.json` only to a site and deployment account the owner authorizes.
- **GitHub/Agent communities**: prepare a text post linking to the registry or skill release; submit only through the owner's authorized account.

## Boundaries

- Never automate sign-up flows, CAPTCHAs, age checks, identity checks, swipes, or messages on third-party dating apps.
- Do not scrape private profiles, bypass platform limits, invent traits, or claim the user is a member of a community they have not joined.
- Keep this dating-only. Work, hiring, supplier, and business material belongs in `find-work` and BossCLI.
- Prefer a dedicated public contact channel. Do not disclose private chat IDs, home/work address, or sensitive data by default.

## Output Quality

Make the source card recognizable across platforms while adapting length and tone. Say that the profile is public and voluntary; do not promise a match or pressure anyone to respond.
