---
name: follow-scoutx
description: Installable digest skill for OpenClaw or Claude Code. Use when the user wants a personalized ScoutX briefing with conversational setup, local preference storage, and minimal end-user configuration.
---

# Follow ScoutX

Use this skill to give the user a personalized ScoutX digest with the same product shape as `follow-good-builders`:

- the backend centrally collects and normalizes content
- the user installs a skill in OpenClaw or Claude Code
- setup happens through conversation
- the user's preferences are stored locally
- each manual run or scheduled run pulls fresh content from the user's selected feeds at execution time
- users can choose the curated ScoutX media feed, first-party sources (X + podcasts), or both
- the user should not be asked for backend URLs or raw API tokens during normal setup
- in OpenClaw, recurring delivery should output the digest to stdout and use `--announce --channel <channel> --to <target>` for the actual chat/channel delivery

## When to use

Use this skill when the user says things like:

- `set up follow scoutx`
- `/follow-scoutx`
- `帮我订一个每天早上 9 点的 AI 摘要`
- `改成每周一早上推送`
- `只看 OpenAI、Anthropic 和 Cursor`
- `显示我当前的设置`

Do not use this skill for:

- backend ingestion debugging
- ScoutX source management
- service deployment work

## End-user model

The end user should only configure:

- frequency
- time
- language
- content interests
- source selection: ScoutX curated media, first-party sources, or both
- first-party source selection: X, podcasts, or both
- per-message item limits for first-party and ScoutX curated media
- digest style

The end user should not configure:

- `BASE_URL`
- `API_TOKEN`
- feed endpoint details
- X API tokens
- podcast RSS or transcript service keys
- raw JSON filters

Developer-only overrides may exist in the helper script, but do not surface them to normal users unless you are explicitly debugging the skill itself.

In OpenClaw, treat `delivery.channel=in_chat` as stdout output delivered by OpenClaw to the current channel. For Feishu or any external channel, use an explicit `delivery.channel` and `delivery.target` rather than relying on `last`.

If the bundled `service.json` still points to a placeholder domain such as `*.example.com`, that is an operator packaging problem, not an end-user setup problem. In that case:

- do not ask the user for a feed URL
- do not ask the user to inspect `service.json`
- say that setup is saved but the Follow ScoutX service is not configured on this installation yet
- tell the user the operator must update the packaged `service.json` or run `configure-service`

The bundled service endpoint is stored in:

- `service.json`

## Local files

The skill stores local state in:

```text
~/.follow_scoutx/
```

Important files:

- `profile.json`
- `state.json`
- `prompt_sync_state.json`
- `service.json` in `~/.follow_scoutx/` for local endpoint override
- `prompts/digest_intro.md`
- `prompts/summarize_content.md`
- `prompts/summarize_tweets.md`
- `prompts/summarize_podcast.md`
- `prompts/translate.md`

## Workflow

### 1. Bootstrap local files

Run:

```bash
python3 scripts/follow_scoutx.py configure
```

This creates the local directory and syncs bundled prompt files into the local prompt directory.
If an older bundled prompt already exists locally, the script updates it automatically and stores a backup under `~/.follow_scoutx/prompts/backups/`.
If the user has manually customized a local prompt after a previous sync, keep that customized file instead of overwriting it.

### 2. Gather preferences through conversation

Ask only for the user-facing preferences:

- daily or weekly
- what time
- whether to use ScoutX curated media, first-party sources, or both
- if using first-party sources, whether to include X, podcasts, or both
- optional separate item caps for first-party and ScoutX curated media
- what topics or companies to follow
- preferred language
- summary style

In OpenClaw, assume delivery is the current chat channel unless the user explicitly asks for a different target.
If the user wants Feishu delivery, save the exact channel and target:

```bash
python3 scripts/follow_scoutx.py configure \
  --delivery-channel feishu \
  --delivery-target "ou_xxx"
```

Translate conversational answers into the helper script arguments.

### 3. Save the profile

Use:

```bash
python3 scripts/follow_scoutx.py configure ...
```

Examples:

```bash
python3 scripts/follow_scoutx.py configure \
  --frequency daily \
  --time 09:00 \
  --language zh-CN \
  --source-mode scoutx \
  --delivery-channel in_chat \
  --topics "AI Agent,编程工具" \
  --keywords-include "OpenAI,Anthropic,Cursor" \
  --max-items 8 \
  --max-scoutx-items 8 \
  --length short
```

```bash
python3 scripts/follow_scoutx.py configure \
  --frequency weekly \
  --days mon,thu \
  --time 09:00 \
  --language bilingual \
  --source-types "scoutx,x,podcast" \
  --delivery-channel feishu \
  --delivery-target "ou_xxx" \
  --topics "AI Agent,模型发布" \
  --max-items 10 \
  --max-first-party-items 6 \
  --max-scoutx-items 4
```

First-party only example:

```bash
python3 scripts/follow_scoutx.py configure \
  --source-mode first_party \
  --topics "AI Agent,模型发布"
```

### 4. Show current settings

Use:

```bash
python3 scripts/follow_scoutx.py show-profile
```

### 4.1 Show bundled service config

Use:

```bash
python3 scripts/follow_scoutx.py show-service
```

This is for debugging or operator verification, not for normal end-user setup.

### 4.2 Configure the local service endpoint override

Use only when the current installation needs a specific feed endpoint, such as a temporary public IP before the final domain is ready.

```bash
python3 scripts/follow_scoutx.py configure-service \
  --feed-url "https://input.reai.group/v1/public/feed" \
  --meta-url "https://input.reai.group/v1/public/meta"
```

This writes the endpoint override into:

```text
~/.follow_scoutx/service.json
```

Do not ask normal users to do this unless you are acting as the operator of that OpenClaw installation.

### 5. Preview the next digest

Use:

```bash
python3 scripts/follow_scoutx.py preview
```

If the backend feed is not available yet, explain that setup is complete but the central feed endpoint is not reachable.

If the configured endpoint is obviously still a placeholder, explain that the package was shipped without a real Follow ScoutX feed address and escalate to the operator. Do not turn this into a question asking the end user for the feed URL.

### 5.1 Prepare a prompt-controlled digest payload for OpenClaw

When the result should be remixed by the agent with stable prompt control, use:

```bash
python3 scripts/follow_scoutx.py prepare-digest
```

This returns one JSON payload containing:

- the selected ScoutX items
- the local user config
- the digest prompts
- a strict output contract for the final message

Use this path when OpenClaw should produce the final message text with LLM help.
Even on this path, every selected item must still render as its own numbered entry; do not collapse item 4..n into "more updates" style placeholders.

### 5.2 Deliver the raw deterministic digest

When the result is meant to be sent back to the current OpenClaw chat channel, use:

```bash
python3 scripts/follow_scoutx.py deliver
```

This returns a deterministic plain-text digest directly from the selected ScoutX items.

Important behavior:

- ScoutX is the central content source
- X and podcast first-party content are also read from centrally prepared public feeds
- Follow ScoutX does not maintain a separate message cache
- every preview or delivery run fetches fresh data from the configured selected public feeds before filtering and formatting it
- if any selected feed fails to load, default behavior should be to continue with a partial digest but explicitly mark the run as partial and expose `failed_source_types` plus `errors`; use `FOLLOW_SCOUTX_ALLOW_PARTIAL_FEEDS=0` or omit partial mode only when you explicitly want hard failure behavior
- if both first-party sources and ScoutX curated media are selected, recurring OpenClaw delivery should still default to one cron job; the final digest should render one section per message group inside the same delivery
- `max_items` is still split logically across message groups; use `--max-first-party-items` and `--max-scoutx-items` when the user wants separate caps
- if the rendered digest is too long for the delivery channel, split it into multiple sequential messages before delivery, especially for Feishu

### 5.2.1 Validation and Acceptance

When the user asks to validate, inspect, or accept a digest run, prefer the raw JSON outputs:

```bash
python3 scripts/follow_scoutx.py preview --json
python3 scripts/follow_scoutx.py deliver --json
```

For validation, only rely on raw fields such as:

- `profile.preferences`
- `groups[*].group_id`
- `groups[*].item_count`
- `stats.group_counts`
- `items[*].title`
- `items[*].source_type`
- `delivery.message_count` or the returned `messages` array length
- `errors`

Do not invent secondary labels or content judgments such as:

- `AI相关: ✅/⚠️/❌`
- `边界内容`
- `每日热点导览`
- `当前无 AI 相关内容`

If the user explicitly asks for an acceptance verdict, derive it only from the raw counts, titles, and delivery results. Do not replace the script's output with your own semantic classifier.
If `status` is `partial` or `errors` is non-empty, report that the run degraded and name the failed sources; do not misreport it as a clean filtering result.

### 5.3 Show the recommended OpenClaw cron command

When the user wants recurring delivery in OpenClaw, use:

```bash
python3 scripts/follow_scoutx.py show-openclaw-cron
```

This prints a recommended `openclaw cron add` command derived from:

- the saved schedule in `profile.json`
- the saved `delivery.channel` and `delivery.target`
- the current local service override in `~/.follow_scoutx/service.json`

If the installation still relies on a temporary public IP, first run `configure-service`, then use `show-openclaw-cron`.

### 5.4 Install the OpenClaw cron job directly

Once setup is confirmed, you can create the OpenClaw cron job directly:

```bash
python3 scripts/follow_scoutx.py install-openclaw-cron
python3 scripts/follow_scoutx.py install-openclaw-cron --apply
python3 scripts/follow_scoutx.py install-openclaw-cron --replace-existing --apply
```

Without `--apply`, the command returns a dry-run JSON payload for inspection. Check `delivery_diagnostics.stable` before applying. The default stable path requires an explicit Feishu target. If the user wants current-chat delivery, use `--main-session-system-event` so OpenClaw routes through the main session instead of relying on `--channel last`.

Use this after:

1. `configure-service` is correct for the current installation
2. the user's schedule and preferences are already saved with `configure`
3. delivery is saved with an explicit Feishu channel and target, such as `--delivery-channel feishu --delivery-target ou_xxx`, unless the user explicitly chooses the main-session system event path for current-chat delivery

### 6. Recurring delivery in OpenClaw

For OpenClaw recurring delivery, prefer the native channel flow instead of shell cron + inbox.
Use the deterministic `deliver --json` path by default for English or when the output can safely stay close to the source text.
If the user's preferred language is `zh-CN` or `bilingual` and first-party sources (`x` or `podcast`) are enabled, prefer `prepare-digest` so the agent can generate localized summaries that actually respect `config.language`.

For OpenClaw, `delivery.method=stdout` is a local skill preference: it means `follow_scoutx.py deliver` writes the digest to stdout. It is not the Feishu transport. Feishu transport still requires OpenClaw cron delivery via `--announce --channel feishu --to <target>`.

Do not use `delivery.mode=session` with `--session isolated` for Feishu delivery. Isolated sessions do not have a previous chat channel to inherit, and this can fail with "Channel is required".

Stable target shape for the current chat:

```bash
openclaw cron add \
  --name "follow-scoutx-daily" \
  --cron "0 9 * * *" \
  --agent main \
  --session main \
  --system-event "Run `python3 scripts/follow_scoutx.py deliver --json`, then send each returned message chunk in order without rewriting. Use the last chunk as your final answer." \
  --exact \
  --timeout-seconds 120
```

Target shape for Feishu:

```bash
openclaw cron add \
  --name "follow-scoutx-daily" \
  --cron "0 9 * * *" \
  --session isolated \
  --agent main \
  --message "Run `FOLLOW_SCOUTX_FEED_URL=https://input.reai.group/v1/public/feed FOLLOW_SCOUTX_DELIVERY_CHANNEL_HINT=feishu python3 /root/work/follow-scoutx/scripts/follow_scoutx.py deliver --json`, then send each returned message chunk in order without rewriting. Use the last chunk as your final answer." \
  --announce \
  --channel feishu \
  --to "ou_xxx" \
  --best-effort-deliver \
  --exact \
  --timeout-seconds 180
```

If the user wants Chinese output for first-party sources, the generated cron command should switch from `deliver --json` to `prepare-digest` and instruct the agent to write the final digest in `config.language` rather than returning raw source text.

Important:

- default recurring delivery should require an explicit Feishu target
- for current-chat delivery, use `install-openclaw-cron --main-session-system-event --apply` so OpenClaw sends a system event to the main session instead of hard-coding a target
- if `delivery.channel=feishu`, do not use `--main-session-system-event`; Feishu delivery must use explicit `--channel feishu --to <target>`
- `install-openclaw-cron --apply` refuses `channel=last` by default; use `--allow-channel-last` only for internal compatibility testing after manually verifying this OpenClaw installation can reliably route `last`
- for Feishu, always pass `--channel feishu --to <target>` with a raw `ou_...` user open_id or `oc_...` group chat_id
- when both message groups are selected, `show-openclaw-cron` and `install-openclaw-cron` should still default to one cron job; the digest body should use grouped sections instead of separate jobs
- OpenClaw cron has no name-based update; if replacing a previously installed job, use `install-openclaw-cron --replace-existing --apply`, which lists jobs with `openclaw cron list --json` and removes matching generated names by id before creating the replacement
- use `deliver` as the default recurring delivery path for English or near-source deterministic output
- if `language` is `zh-CN` or `bilingual` and first-party sources are enabled, prefer `prepare-digest` so first-party summaries are localized instead of staying in raw English
- if `language=zh-CN` and `prepare-digest` is used, localize first-party item titles and summary paragraphs into Chinese instead of only translating section labels
- use `prepare-digest` only when you explicitly need prompt-controlled LLM remixing and have confirmed the platform path does not re-parse or rewrite the result
- if `prepare-digest` is used, keep one numbered entry per selected item and never fold trailing items into catch-all text such as `更多动态`
- keep inbox/file output only as fallback or debugging
- after user confirmation, prefer `install-openclaw-cron --apply` instead of asking the user to copy a cron command manually
- for validation and acceptance, prefer `preview --json` / `deliver --json` and quote raw fields instead of adding your own `AI相关`-style annotations

## `/follow-scoutx` Setup Flow

When the user enters `/follow-scoutx` or asks to enable the Follow ScoutX skill, use this flow:

1. Explain briefly what the skill does
2. Ask only the user-facing setup questions
3. Save preferences with `configure`
4. If this OpenClaw installation needs a fixed feed endpoint, apply it with `configure-service`
5. Offer a preview
6. Ask whether the user wants recurring delivery in the current chat
7. If yes, run `install-openclaw-cron` first and inspect `delivery_diagnostics`
8. If the user wants Feishu delivery, save an explicit target and create the cron job with `install-openclaw-cron --apply`
9. If the user wants current-chat delivery, create the cron job with `install-openclaw-cron --main-session-system-event --apply`
10. If an existing job needs replacement, use `install-openclaw-cron --replace-existing --apply`, or manually use `openclaw cron list --json` to find the matching job id and `openclaw cron rm <id>` before adding the replacement
11. Confirm that future results will be delivered through the configured route

Recommended setup questions:

- daily or weekly
- what time
- ScoutX curated media, first-party sources, or both
- X, podcasts, or both if first-party sources are enabled
- what topics or companies to follow
- what to exclude
- which language
- how many items per digest

Do not ask the user for:

- feed URLs
- API tokens
- X bearer tokens
- podcast transcript API keys
- webhook addresses
- raw cron expressions

If preview or delivery cannot proceed because the packaged service endpoint is still placeholder-only, tell the user the installation is not fully configured by the operator yet. Do not ask the user to supply that address manually.

### 7. Advanced prompt customization

If the user asks to change tone or style in a durable way:

- update the saved profile when the preference maps to structured fields like `length` or `tone`
- for richer customization, edit the local prompt files in `~/.follow_scoutx/prompts/`

## Guidance

- Prefer plain-language conversation over asking the user to write JSON.
- When the user says `show my settings`, read `show-profile` and summarize it naturally.
- When the user says `make it shorter`, update `--length short`.
- When the user says `只看一手信息源`, update `--source-mode first_party`.
- When the user says `只看 X 平台`, update `--source-types x`.
- When the user says `切回 ScoutX 优质媒体源`, update `--source-mode scoutx`.
- When the user says `一手信息源最多 N 条`, update `--max-first-party-items N`.
- When the user says `ScoutX 优质自媒体最多 N 条`, update `--max-scoutx-items N`.
- When the user says `focus more on builders shipping products`, add that preference to the local prompt file instead of inventing backend settings.
- Treat backend endpoint details as implementation details hidden behind the skill.
- In OpenClaw, prefer native cron/channel delivery over asking the user to copy shell cron lines.
