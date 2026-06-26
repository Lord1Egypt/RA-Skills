---
name: cnki-watch
description: "Query CNKI by journal name or research topic, and create journal or topic subscriptions that periodically push new CNKI paper metadata into the main OpenClaw chat. Use for one-off CNKI lookups and recurring CNKI monitoring."
metadata: { "openclaw": { "emoji": "📚", "requires": { "bins": ["node", "openclaw"] } } }
---

# CNKI Watch

Use this skill when the user wants CNKI results in either of these modes:

- manual journal query: return papers from a named journal,
- manual topic query: return CNKI papers related to a research topic,
- journal subscription: periodically push new papers from a named journal,
- topic subscription: periodically push new papers for a research topic.

## When to use

- The user gives a journal name and wants a one-off CNKI query.
- The user gives a research topic and wants titles plus source metadata.
- The user wants a recurring CNKI watch delivered back into OpenClaw.

## Preconditions

- The skill ships as a normal npm project with a root `package.json` and declared dependencies.
- Preferred runtime is still the OpenClaw gateway container, but local development runs are supported on Windows/macOS/Linux with Node.js 22+.
- On local runs, the script auto-installs missing JavaScript dependencies from `package.json` on first use. Browser discovery supports Playwright-managed Chromium plus common Chrome/Edge installs. No custom `NODE_PATH` is required.
- Prefer `CNKI_COOKIE`. `CNKI_USERNAME` plus `CNKI_PASSWORD` is a fallback path for establishing a CNKI login session.
- If CNKI shows captcha, slider verification, or another human-check page, stop and ask for a fresh `CNKI_COOKIE` or a manually refreshed session. Do not invent alternative scraping logic in the model.
- Treat OpenClaw runtime behavior as authoritative. The docs define the public contract; do not optimize for `quick_validate.py` quirks at the expense of runtime compatibility.

Reference files:

- `references/config.md`
- `references/schedule.md`
- `references/commands.md`

## Canonical entrypoint

Always use the bundled script instead of ad hoc CNKI browsing:

```bash
node {baseDir}/scripts/cnki-watch.mjs <command> [flags]
```

For local development outside OpenClaw:

```bash
cd {baseDir}
npm install
node scripts/cnki-watch.mjs --help
npx cnki-watch query-topic --topic "人工智能" --json
```

## Core commands

### One-off journal lookup

```bash
node {baseDir}/scripts/cnki-watch.mjs query-journal --journal "计算机学报" --json
```

### One-off topic lookup

```bash
node {baseDir}/scripts/cnki-watch.mjs query-topic --topic "大模型安全" --json
```

### Create a journal subscription

```bash
node {baseDir}/scripts/cnki-watch.mjs subscribe-journal --journal "计算机学报" --schedule "daily@09:00" --json
```

### Create a topic subscription

```bash
node {baseDir}/scripts/cnki-watch.mjs subscribe-topic --topic "大模型安全" --schedule "weekly@mon@09:00" --json
```

### List and remove subscriptions

```bash
node {baseDir}/scripts/cnki-watch.mjs list-subscriptions --json
node {baseDir}/scripts/cnki-watch.mjs unsubscribe --id "<subscription-id>" --json
node {baseDir}/scripts/cnki-watch.mjs run-subscription --id "<subscription-id>" --json
```

## Workflow

1. Decide whether the user wants a manual query or a subscription.
2. Preserve the journal name or topic text exactly unless the user explicitly asks to normalize it.
3. Use `query-journal` for a journal lookup and `query-topic` for a topic lookup.
4. Use `subscribe-journal` or `subscribe-topic` for recurring pushes. If the user does not supply a schedule, use the configured `defaultSchedule`.
5. Respect skill config for `browserProfile`, `timezone`, `defaultSchedule`, `maxManualResults`, and `maxPushResults`.
6. After creating, listing, running, or removing a subscription, report the subscription id, schedule, timezone, and status returned by the script.

## Delivery rules

- Subscription jobs run as isolated cron turns with no automatic announce delivery.
- The script is responsible for posting new findings back to the main OpenClaw chat, typically through `chat.inject`.
- Manual queries return metadata to the current turn and do not create subscription state.
- Subscription runs should push only new items and stay silent when there is no delta.
- Return metadata and CNKI links only. Do not promise PDFs, full text, or other copyrighted payloads.

## Failure handling

- If the script reports missing browser dependencies or an unusable runtime, fix the OpenClaw runtime and retry.
- If CNKI blocks the session with captcha or another verification flow, stop and ask for a fresh `CNKI_COOKIE` or a manually refreshed CNKI session.
- If a journal lookup returns weak matches, verify the exact journal name and tell the user that source filtering may need the precise CNKI source string.
- If credentials are missing, ask the user to populate `CNKI_COOKIE`, or `CNKI_USERNAME` plus `CNKI_PASSWORD`, in the skill env config before retrying.
