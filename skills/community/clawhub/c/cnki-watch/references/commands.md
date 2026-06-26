# Command Contract

This file defines the public contract that the `cnki-watch` script should satisfy at runtime.

For local development, the skill should also behave like a normal npm project:

```bash
npm install
node scripts/cnki-watch.mjs --help
npm test
npx cnki-watch query-topic --topic "<topic-name>" --json
```

## Manual queries

Use these commands for one-off lookups:

```bash
node {baseDir}/scripts/cnki-watch.mjs query-journal --journal "<journal-name>" [--limit <n>] [--json]
node {baseDir}/scripts/cnki-watch.mjs query-topic --topic "<topic-name>" [--limit <n>] [--json]
```

Expected behavior:

- `query-journal` searches CNKI for papers whose source matches the named journal.
- `query-topic` searches CNKI for papers related to the named research topic.
- If `--limit` is omitted, the script should use `maxManualResults`.
- Manual queries return metadata only and do not create or mutate subscription state.

## Subscription commands

Use these commands for recurring CNKI watches:

```bash
node {baseDir}/scripts/cnki-watch.mjs subscribe-journal --journal "<journal-name>" [--schedule "<schedule>"] [--json]
node {baseDir}/scripts/cnki-watch.mjs subscribe-topic --topic "<topic-name>" [--schedule "<schedule>"] [--json]
node {baseDir}/scripts/cnki-watch.mjs list-subscriptions [--json]
node {baseDir}/scripts/cnki-watch.mjs unsubscribe --id "<subscription-id>" [--json]
node {baseDir}/scripts/cnki-watch.mjs run-subscription --id "<subscription-id>" [--json]
```

Expected behavior:

- If `--schedule` is omitted, use `defaultSchedule`.
- Store enough state to avoid re-sending the same paper on every run.
- Subscription runs post updates into the main OpenClaw chat rather than the isolated cron turn.
- If a run finds no new papers, it should stay silent or return a clear no-op status.
- Push output should respect `maxPushResults`.

## Result shape

Manual query and subscription payloads should expose paper metadata, not full text. The normalized record shape should include:

- `record_id`
- `title`
- `authors`
- `source`
- `publish_date`
- `url`
- `matched_type`
- `matched_query`

Topic lookups must include the paper title and source. Journal lookups should keep the requested journal name visible in either `source` or `matched_query`.

## Authentication and CNKI access

Credential precedence:

1. `CNKI_COOKIE`
2. `CNKI_USERNAME` plus `CNKI_PASSWORD`

Runtime expectations:

- Prefer an existing CNKI cookie session when available.
- Treat username/password as a fallback login path only.
- If CNKI shows captcha, slider verification, MFA, or other human verification, stop and surface an actionable error instead of looping.

## Delivery contract

Subscription pushes are intended for the main OpenClaw chat session:

- no automatic announce channel is required,
- new items are injected back into the main chat,
- no-new-result runs stay quiet,
- errors should still surface clearly so the user can fix credentials, browser runtime, or CNKI session state.
