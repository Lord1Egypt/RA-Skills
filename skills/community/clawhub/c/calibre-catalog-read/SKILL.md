---
name: calibre-catalog-read
description: Read-only Calibre catalog lookup (including ID-based read-only lookups like "ID 1021 を確認して") and one-book analysis-comments workflow over a running Content server. Use for any list/search/id viewing even when a specific ID is mentioned. Never for title/authors/tags/series/series_index metadata edits.
metadata: {"openclaw":{"requires":{"bins":["node","uv","calibredb","ebook-convert"],"env":["CALIBRE_PASSWORD"]},"optionalEnv":["CALIBRE_USERNAME"],"primaryEnv":"CALIBRE_PASSWORD","dependsOnSkills":["subagent-spawn-command-builder"],"localWrites":["skills/calibre-catalog-read/state/runs.json","skills/calibre-catalog-read/state/calibre_analysis.sqlite","skills/calibre-catalog-read/state/cache/**"],"modifiesRemoteData":["calibre:comments-metadata"]}}
---

# calibre-catalog-read

Use this skill for:
- Read-only catalog lookup (`list/search/id`)
- ID-based read-only lookups: "ID 1021 を確認して", "1021番の詳細", "show me book 1021", "ID 1021 の情報を見せて"
- One-book AI reading workflow (`export -> analyze -> cache -> comments HTML apply`)
- Natural conversational book-reference turns where a lightweight read-only lookup would improve the reply
  - Examples: the user mentions a book that may exist in the library, suggests "if you're interested, read it", asks whether it is in the library, or continues a reading-related conversation without using explicit command wording

## Skill selection contract (strict)

- This skill is read-only for catalog lookup + analysis workflow.
- This skill may also be selected from natural conversation when the likely user need is a lightweight library check or book lookup, even if the user does not use explicit command-style wording.
- In such conversational cases, prefer the smallest useful action first:
  - first choice: `id/search/list` style read-only lookup
  - do not jump directly into heavy analysis unless the user clearly asks for it
  - do not treat casual book talk as metadata-edit intent
- If user intent includes metadata edit/fix/update (title/authors/series/series_index/tags/publisher/pubdate/languages),
  route to `calibre-metadata-apply` and do not execute edit paths here.

Do NOT use this skill for:
- Editing title/authors/series/series_index/tags/publisher/pubdate/languages
- Any user request that says "metadata edit", "title fix", "ID指定で編集"
- Heavy one-book analysis when the user only made a casual conversational reference and did not ask for reading/analysis
- Those must use `calibre-metadata-apply`

### Routing: ID in request ≠ edit intent
- ID が含まれるリクエストはデフォルトで読み取り専用 → このスキル
- `calibre-metadata-apply` へのルーティングは明示的な編集動詞がある場合のみ (修正/編集/変更/直す/fix/edit/update/change)
- 確認/見せて/教えて/詳細/check/show/view は読み取り → このスキル

## Requirements

- `calibredb` available on PATH in the runtime where scripts are executed.
- `ebook-convert` available for text extraction.
- `subagent-spawn-command-builder` installed (for spawn payload generation).
- Reachable Calibre Content server URL in `--with-library` format:
  - `http://HOST:PORT/#LIBRARY_ID`
  - If `LIBRARY_ID` is unknown, use `#-` once to list available IDs on the server.
- Do not assume localhost/127.0.0.1; always pass explicit reachable `HOST:PORT`.
- `--with-library` can be omitted only when one of these is configured:
  - env: `CALIBRE_WITH_LIBRARY` or `CALIBRE_LIBRARY_URL` or `CALIBRE_CONTENT_SERVER_URL`
  - optional library id completion: `CALIBRE_LIBRARY_ID`
- Read the "Calibre Content Server" section of TOOLS.md for the correct `--with-library` URL.
- Host failover (IP change resilience):
  - Optional env: `CALIBRE_SERVER_HOSTS=host1,host2,...`
  - Script auto-tries candidates, including WSL host-side `nameserver` from `/etc/resolv.conf`.
- If auth is enabled:
  - Preferred: set in `/home/altair/.openclaw/.env`
    - `CALIBRE_USERNAME=<user>`
    - `CALIBRE_PASSWORD=<password>`
  - Auth scheme policy for this workflow:
    - Non-SSL deployment assumes **Digest** authentication.
    - Do not pass auth mode arguments such as `--auth-mode` / `--auth-scheme`.
  - Then pass only `--password-env CALIBRE_PASSWORD` (username auto-loads from env)
  - You can still override with `--username <user>` explicitly.

## Commands

List books (JSON):

```bash
node skills/calibre-catalog-read/scripts/calibredb_read.mjs list \
  --with-library "http://192.168.11.20:8080/#Calibreライブラリ" \
  --password-env CALIBRE_PASSWORD \
  --limit 50
```

Search books (JSON):

```bash
node skills/calibre-catalog-read/scripts/calibredb_read.mjs search \
  --with-library "http://192.168.11.20:8080/#Calibreライブラリ" \
  --password-env CALIBRE_PASSWORD \
  --query 'series:"中公文庫"'
```

Get one book by id (JSON):

```bash
node skills/calibre-catalog-read/scripts/calibredb_read.mjs id \
  --with-library "http://192.168.11.20:8080/#Calibreライブラリ" \
  --password-env CALIBRE_PASSWORD \
  --book-id 3
```

Run one-book pipeline (analyze + comments HTML apply + cache):

```bash
uv run python skills/calibre-catalog-read/scripts/run_analysis_pipeline.py \
  --with-library "http://192.168.11.20:8080/#Calibreライブラリ" \
  --password-env CALIBRE_PASSWORD \
  --book-id 3 --lang ja
```

## Cache DB

Initialize DB schema:

```bash
uv run python skills/calibre-catalog-read/scripts/analysis_db.py init \
  --db skills/calibre-catalog-read/state/calibre_analysis.sqlite
```

Check current hash state:

```bash
uv run python skills/calibre-catalog-read/scripts/analysis_db.py status \
  --db skills/calibre-catalog-read/state/calibre_analysis.sqlite \
  --book-id 3 --format EPUB
```


## Main vs Subagent responsibility (strict split)

Use this split to avoid long blocking turns on chat listeners.

### Main agent (fast control plane)
- Validate user intent and target `book_id`.
- Confirm subagent runtime knobs: `model`, `thinking`, `runTimeoutSeconds`.
- Start subagent and return a short progress reply quickly.
- After subagent result arrives, run DB upsert + Calibre apply.
- Report final result to user.

### Subagent (heavy analysis plane)
- Read extracted source payload.
- Generate analysis JSON strictly by schema.
- Do not run metadata apply or user-facing channel actions.

### Never do in main when avoidable
- Long-form content analysis generation.
- Multi-step heavy reasoning over full excerpts.

### Turn policy
- One book per run.
- Prefer asynchronous flow: quick ack first, final result after analysis.
- If analysis is unavailable, either ask user or use fallback only when explicitly acceptable.

## Subagent pre-flight (required)

Before first subagent run in a session, confirm once:
- `model`
- `thinking` (`low`/`medium`/`high`)
- `runTimeoutSeconds`

Do not ask on every run. Reuse the confirmed settings for subsequent books in the same session unless the user asks to change them.

## Subagent support (model-agnostic)

Book-reading analysis is a heavy task. Use a subagent with a lightweight model for analysis generation, then return results to main agent for cache/apply steps.

- Prompt template: `references/subagent-analysis.prompt.md`
- Input schema: `references/subagent-input.schema.json`
- Output schema: `references/subagent-analysis.schema.json`
- Input preparation helper: `scripts/prepare_subagent_input.mjs`
  - Splits extracted text into multiple files to avoid read-tool single-line size issues.

Rules:
- Use subagent only for heavy analysis generation; keep main agent lightweight and non-blocking.
- In this environment, Python commands must use `uv run python`.
- Use the strict prompt template (`references/subagent-analysis.prompt.md`) as mandatory base; do not send ad-hoc relaxed read instructions.
- Keep final DB upsert and Calibre metadata apply in main agent.
- Process one book per run.
- Confirm model/thinking/timeout once per session, then reuse; do not hardcode provider-specific model IDs in the skill.
- Configure callback/announce behavior and rate-limit fallbacks using OpenClaw default model/subagent/fallback settings (not hardcoded in this skill).
- Exclude manga/comic-centric books from this text pipeline (skip when title/tags indicate manga/comic).
- If extracted text is too short, stop and ask user for confirmation before continuing.
  - The pipeline returns `reason: low_text_requires_confirmation` with `prompt_en` text.
- For read operations in agent/chat, prefer `node .../calibredb_read.mjs` instead of direct `calibredb` calls.
- Never run `calibre-server` from this skill.
  - This workflow always connects to an already-running Calibre Content server.

## Connection bootstrap (mandatory)

- Do not ask the user for `--with-library` first.
- First, run read commands (`list/search/id`) without explicit `--with-library` and use saved defaults.
  - Scripts auto-load `.env` and resolve `CALIBRE_WITH_LIBRARY` / `CALIBRE_CONTENT_SERVER_URL`.
- This same rule applies to conversational lookup turns: try the lightweight read-only check first before asking the user for connection details.
- Ask user for URL only if resolution fails (`missing --with-library` / `unable to resolve usable --with-library`).

## Language policy

- Do not hardcode user-language prose in pipeline scripts.
- Generate user-visible analysis text from subagent output, with language controlled by user-selected settings and `lang` input.
- Fallback local analysis in scripts is generic/minimal; preferred path is subagent output following the prompt template.


## Orchestration note (important)

`run_analysis_pipeline.py` is a local script and does **not** call OpenClaw tools by itself.
Subagent execution must be orchestrated by the agent layer using `sessions_spawn`.

Required runtime sequence:
1. Main agent prepares `subagent_input.json` + chunked `source_files` from extracted text.
   - Use:
   ```bash
   node skills/calibre-catalog-read/scripts/prepare_subagent_input.mjs \
     --book-id <id> --title "<title>" --lang ja \
     --text-path /tmp/book_<id>.txt --out-dir /tmp/calibre_subagent_<id>
   ```
2. Main agent uses the shared builder skill `subagent-spawn-command-builder` to generate the `sessions_spawn` payload, then calls `sessions_spawn`.
   - Build with profile `calibre-read` and run-specific analysis task text.
   - Use the generated JSON as-is (or merge minimal run-specific fields such as label/task text).
3. Subagent reads all `source_files` and returns analysis JSON (schema-conformant).
4. Main agent passes that file via `--analysis-json` to `run_analysis_pipeline.py` for DB/apply.

If step 2 is skipped and `--analysis-json` is not provided, the pipeline returns `updated: false, analysis_mode: fallback` without writing to DB or Calibre comments. Pass `--allow-fallback` to force-persist local analysis (testing only).


## Chat execution model (required, strict)

For Discord/chat, always run as **two separate turns**.

### Turn A: start only (must be fast)
- Select one target book.
- Build spawn payload with `subagent-spawn-command-builder` (`--profile calibre-read` + run-specific `--task`).
- Call `sessions_spawn` using that payload.
- Record run state (`runId`) via `run_state.mjs upsert`.
- Reply to user with selected title + "running in background".
- **Stop turn here.**

### Turn B: completion only (separate later turn)
Trigger: completion announce/event for that run.
- Run one command only (completion handler):
  - `scripts/handle_completion.mjs` (`get -> apply -> remove`, and `fail` on error).
- If `runId` is missing, handler returns `stale_or_duplicate` and does nothing.
- Send completion/failure reply from handler result.

Hard rule:
- Never poll/wait/apply in Turn A.
- Never keep a chat listener turn open waiting for subagent completion.

## Run state management (single-file, required)

For one-book-at-a-time operation, keep a single JSON state file:
- `skills/calibre-catalog-read/state/runs.json`

Use `runId` as the primary key (subagent execution id).

Lifecycle:
1. On spawn acceptance, upsert one record:
   - `runId`, `book_id`, `title`, `status: "running"`, `started_at`
2. Do not wait/poll inside the same chat turn.
3. On completion announce, load record by `runId` and run apply.
4. On successful apply, delete that record immediately.
5. On failure, set `status: "failed"` + `error` and keep record for retry/debug.

Rules:
- Keep this file small and operational (active/failed records only).
- Ignore duplicate completion events when record is already removed.
- If record is missing at completion time, report as stale/unknown run and do not apply blindly.

Use helper scripts (avoid ad-hoc env var mistakes):

```bash
# Turn A: register running task
node skills/calibre-catalog-read/scripts/run_state.mjs upsert \
  --state skills/calibre-catalog-read/state/runs.json \
  --run-id <RUN_ID> --book-id <BOOK_ID> --title "<TITLE>"

# Turn B: completion handler (preferred)
node skills/calibre-catalog-read/scripts/handle_completion.mjs \
  --state skills/calibre-catalog-read/state/runs.json \
  --run-id <RUN_ID> \
  --analysis-json /tmp/calibre_<BOOK_ID>/analysis.json \
  --with-library "http://HOST:PORT/#LIBRARY_ID" \
  --password-env CALIBRE_PASSWORD --lang ja
```
