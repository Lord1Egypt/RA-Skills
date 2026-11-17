---
name: frameferry
description: Archive public Instagram media through InstaCognito with bounded archive/sync runs, section-aware outcomes, durable receipts, and optional local ZIP export.
license: MIT
homepage: https://github.com/saju01/frameferry
metadata: { "openclaw": { "emoji": "🛶", "requires": { "bins": ["node", "npm"] } } }
---

# FrameFerry

Use this skill when the user wants a standalone free archive or periodic sync of public Instagram media through InstaCognito for personal or explicitly authorized public-profile archiving. InstaCognito advertises free public-profile viewing/download with no login at `https://instacognito.com/en/photo`; its terms at `https://instacognito.com/terms-and-conditions` prohibit commercial-scale scraping/archiving without authorization, copyright infringement, privacy abuse, private-access circumvention, and overburdening. Do not use this skill for logins, cookies, paid APIs, proxy rotation, signature reversal, anti-bot bypass, commercial scrape platforms, or unlimited/guaranteed-complete claims.

## Optional model-tiered delegation

When the owner asks for a cheaper worker and a stronger reviewer, follow
[the orchestration guide](references/orchestration.md). The primary assistant
owns the request, permissions, model selection, and final answer; one isolated
worker runs the CLI, then one separate reviewer checks the evidence. The Node
CLI performs pagination, downloading, hashing, and deduplication without LLM
calls. Do not spawn a model per post or media file.

Choose worker/reviewer models from the owner's available configured models.
Use explicit choices unchanged; never silently switch cost tiers. Review every
run when requested; otherwise agree whether routine unchanged syncs need
separate review. Keep the same output path, bounded CLI limits, and all safety
rules below. Delegation grants no extra permissions. Completion: the worker has
actually exited, required review is complete, and the parent reports the real
outcome. A child reporting success is not verification.

## Bootstrap from an installed skill root

From the skill directory itself:

```bash
cd {baseDir}
npm ci
npx playwright install chromium
node ./bin/frameferry.js doctor
```

Do not assume a globally linked `frameferry` binary. Use `node ./bin/frameferry.js ...` from `{baseDir}` unless the owner explicitly chose `npm link`.

## Archive workflow

1. Confirm the handle is public content the owner is allowed to archive and choose a dedicated output directory.
2. Run the archive with the exact sections needed, for example:

   ```bash
   cd {baseDir}
   node ./bin/frameferry.js archive example_handle --output /path/to/archive/example_handle --categories posts,reels,stories,highlights --media-types image,video
   ```

3. For a portable package of an existing local archive, run:

   ```bash
   cd {baseDir}
   node ./bin/frameferry.js export example_handle --output /path/to/archive/example_handle --zip /path/to/export/frameferry-example.zip
   ```

4. Verify the current state:

   ```bash
   cd {baseDir}
   node ./bin/frameferry.js status example_handle --output /path/to/archive/example_handle
   ```

## Behaviour you must state honestly

- `posts` are stable and repeat-sync without re-downloading when verified receipts still match.
- `reels` are category-qualified to avoid colliding with posts.
- `stories` and `highlights` have no stable provider shortcode in the public DOM, so later syncs re-fetch them and dedupe after hashing.
- Section outcomes can be `COMPLETE`, `PARTIAL`, `UNAVAILABLE`, `BLOCKED`, `DEFERRED`, or `ACTION_REQUIRED` depending on what the provider visibly exposed.
- A successful ZIP package does not prove the archive itself is complete; the completeness split is recorded inside the ZIP metadata.
- Pagination follows the element the provider's own `IntersectionObserver` watches, not the last rendered card; where that probe is unavailable it falls back fail-closed to the trailing same-`data-id` run, then the last card.
- Dates are never guessed: a provider string with no explicit year, or one that does not parse, is preserved verbatim, so `dateParsed` is not always a timestamp and must be checked before use.

## ZIP safety

Only verified media plus generated metadata go into the ZIP. Never include locks, browser profiles, credentials, logs, private reports, or signed provider URLs. ZIP export is bounded to ZIP32-safe archives in this release: max 2 GiB output, max 5000 entries, max 3000 source files.

## Verification

Runtime smoke path from the repo/installed skill root: `node ./bin/frameferry.js doctor`, then `node ./bin/frameferry.js status <handle> --output <path>`. Repository verification before publication: `npm test`, `npm run test:sandbox`, run the installed OpenClaw `skill-creator` quick validator against this repository (the validator path is installation-specific), and `npm pack --dry-run`.