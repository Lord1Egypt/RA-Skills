# Fulcra Annotations

Create Fulcra annotation definitions and record annotation events from an agent workflow.

Fulcra gives agents and their humans scoped, secure access to read and write real-world context and shared human/agent memory: attention, events, location, calendar, health, wearables, and other streams. This skill is the write path: agents can create reusable annotation definitions and record moments, booleans, numeric values, and scale ratings after user approval.

## What It Does

- Lists existing Fulcra annotation definitions.
- Creates, updates, and deletes annotation definitions, including definition-level tags.
- Records annotation events, including historical timestamps.
- Supports moment, boolean, numeric, and scale annotations.
- Supports record-level tags for individual logged events.
- Verifies writes by reading the event back after ingest.

## Requirements

- Python 3.11 or newer.
- Authenticated Fulcra account for the target user. No API key is required.
- `uv tool run fulcra-api auth login` completed, or `FULCRA_ACCESS_TOKEN` supplied by a trusted secret manager.

Fulcra accounts can be created through the CLI auth flow and include 5 GB of storage free forever. Users who want biometrics, location, calendar, and other mobile context can install the Context iOS app and sign in with the same account; the app uses the same free storage and is no longer subscription gated. Android is coming soon.

For remote agents, run `uv tool run fulcra-api auth login` on the agent host, keep it polling, and surface only the printed device authorization URL and user code to the intended user in chat through the active trusted user channel. The user can approve from any browser on any device. Never send access tokens or credential files.

If credentials live outside the process home, set `FULCRA_HOME` to the home directory that contains the Fulcra CLI credentials. Set `FULCRA_CLI_COMMAND` only when you need to override the default `uv tool run fulcra-api` command.

## Quick Start

```bash
python3 skills/fulcra-annotations/scripts/fulcra_annotations.py list
```

Create a reusable moment annotation definition:

```bash
python3 skills/fulcra-annotations/scripts/fulcra_annotations.py create \
  --type moment \
  --name "Asked Agent to Do Something New" \
  --description "Logged when the user asks the agent to try a new category of work" \
  --tag agent \
  --tag new-task
```

Record a moment now:

```bash
python3 skills/fulcra-annotations/scripts/fulcra_annotations.py record \
  --name "Asked Agent to Do Something New" \
  --note "User asked for a new annotation workflow" \
  --tag new-task
```

Record a historical moment:

```bash
python3 skills/fulcra-annotations/scripts/fulcra_annotations.py record \
  --name "Asked Agent to Do Something New" \
  --recorded-at "2026-05-15T10:00:00-04:00" \
  --note "Backfilled from user request" \
  --tag backfill
```

The script returns JSON. Treat the write as confirmed only when `verified_matches` is at least `1`.

## First-Run Flow

For a new user, keep the first annotation loop tight:

1. Offer 2-3 concrete tracking ideas instead of asking an open-ended question.
2. Check auth with `uv tool run fulcra-api user-info`; if needed, run `uv tool run fulcra-api auth login` and send only the device URL/code.
3. Create 1-3 definitions, saving the returned `annotation.id`, `source_id`, and type in your working notes.
4. Ask one direct question, record the first value with `record --id ...`, and verify `verified_matches >= 1`.
5. Hand off with the definitions created, the timestamp written, and a concrete next step such as mobile logging, Context Web, another annotation, or a small dashboard.

For public demos or group chats, use synthetic values unless the user explicitly approves sharing real Fulcra records.

Create a numeric count annotation:

```bash
python3 skills/fulcra-annotations/scripts/fulcra_annotations.py create \
  --type numeric \
  --name "Coffee Count" \
  --description "Number of coffees consumed today" \
  --measurement-type count \
  --tag health \
  --tag intake
```

For specialized measurement units, inspect the live schema through the bundled helper before adding script support:

```bash
python3 skills/fulcra-annotations/scripts/fulcra_annotations.py measurement-schema
```

Use `measurement-schema --raw` only for local debugging. Do not paste raw private account output into chat.

Update or delete definitions only after user approval:

```bash
python3 skills/fulcra-annotations/scripts/fulcra_annotations.py update \
  --id "<annotation-id>" \
  --description "Updated description" \
  --tag health \
  --tag workflow

python3 skills/fulcra-annotations/scripts/fulcra_annotations.py delete \
  --id "<annotation-id>"
```

## Idempotent Pipelines

For recurring imports or backfills, keep a local ledger keyed by stable source facts. Write unseen records once, retry pending/failed records, and mark a record verified only after Fulcra readback. Keep dedupe keys out of visible notes; store them in local state, metadata, or source bookkeeping.

## Tags

Tags can apply to either the definition or an individual record.

Use definition tags for stable categories that describe the annotation itself:

```bash
python3 skills/fulcra-annotations/scripts/fulcra_annotations.py create \
  --type moment \
  --name "Medication Taken" \
  --tag health \
  --tag adherence
```

Use record tags for context that only applies to one event:

```bash
python3 skills/fulcra-annotations/scripts/fulcra_annotations.py record \
  --name "Medication Taken" \
  --note "Backfilled after travel" \
  --tag backfill \
  --tag travel
```

Use short, reusable, lowercase tags such as `health`, `agent`, `research`, `new-task`, `manual-test`, or `backfill`. Tags should be filter dimensions. For geography, prefer actual place tags such as `town-springfield`, `village-riverside`, `neighborhood-downtown`, or `place-main-campus`, not abstract scope labels. Do not put timestamps, private notes, dedupe keys, or one-off sentences in tags.

## Safety

- Do not print access tokens, direct capability URLs, or private Fulcra records in chat or logs.
- Use dry-run mode before risky writes.
- Ask before deleting or changing an existing annotation definition.
