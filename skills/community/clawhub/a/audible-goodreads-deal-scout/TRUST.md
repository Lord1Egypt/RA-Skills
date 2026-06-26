# Trust and Data Access

Audible Goodreads Deal Scout is a ClawHub / OpenClaw skill for evaluating Audible deals against Goodreads data and optional personal taste notes.

It reports deal opportunities. It does not buy, reserve, check out, redeem credits, manage subscriptions, or complete purchases.

## What the skill may read

| Input | When used | Why |
| --- | --- | --- |
| Config file | Setup, daily deal checks, Want-to-Read scans, delivery | Stores marketplace, thresholds, paths, privacy mode, and optional delivery settings |
| Goodreads CSV | Only when configured | Detects read/currently-reading/to-read shelves and uses ratings/reviews for fit |
| Notes file or pasted notes | Only when configured | Adds personal reading preferences for fit explanations |
| Audible auth file | Only when explicitly created and passed | Checks member-visible cash prices for matched Audible titles |
| Generated artifacts/cache/state | During normal operation | Keeps deterministic prep output, report output, cached lookups, and duplicate scheduled-run state |

Only point configured paths at files you intend this skill to read.

## What the skill may write

| Output | Location |
| --- | --- |
| Config, state, reports, artifacts, and cache files | The configured storage directory, normally `.audible-goodreads-deal-scout/` in the active OpenClaw workspace |
| Optional delivery messages | A configured OpenClaw channel and target, only when delivery is enabled or requested |
| Optional cron entries | OpenClaw cron, only when daily automation registration is requested |

The skill should not write mutable user state inside the installed skill folder because OpenClaw can replace that folder during updates.

## Network access

The skill may fetch:

- Audible promotion, search, and product pages
- Audible authenticated product-price API responses when an Audible auth file is explicitly supplied
- Goodreads public pages for runtime score resolution and optional rating enrichment

Unauthenticated Audible HTML fetches are guarded to known HTTPS Audible hosts and daily-deal, search, or product paths before either the Python fetch path or curl fallback can request them.

It does not send data to a private server controlled by this repository.

## Optional Audible authentication

Audible authentication is optional. The skill works without it, but anonymous Audible pages often hide cash prices behind credit or membership UI.

If you choose to use authenticated price lookup:

- the skill creates a local auth file through the `audible-auth-start` and `audible-auth-finish` helper flow
- the auth flow requests cookie-style Audible/Amazon credential types for compatibility because anonymous Audible pages often hide member cash prices
- the auth file persists the bearer access/refresh token fields used for token refresh and product-price lookup
- the auth file is sensitive local state and should not be committed, pasted into chat, or published
- the auth file is used only for token refresh and Audible product-price lookup
- authenticated API calls are restricted in code to validated Audible product ids and allowlisted Audible/Amazon API domains
- authenticated `discounted` means a member-visible cash price is below list price, not proof of a limited-time sale

## Purchase behavior

The skill does not make purchases.

It does not:

- add items to a cart
- buy audiobooks
- redeem credits
- reserve deals
- manage subscriptions
- submit payment information

Any purchase decision remains manual and outside the skill.

## Privacy modes

`privacyMode: "normal"` allows the model-facing fit step to use configured Goodreads context and taste notes.

`privacyMode: "minimal"` prevents personal artifacts from being exposed to the model-facing runtime and produces recommendations from public data only.

## Publishing safety

Published bundles should exclude local/generated state, auth files, caches, tests, and private artifacts. Run before publishing:

```bash
sh ./scripts/audible-goodreads-deal-scout.sh publish-audit --tags latest
```

The publish audit checks required public files, generated/private artifact exclusions, and known private marker leaks.
