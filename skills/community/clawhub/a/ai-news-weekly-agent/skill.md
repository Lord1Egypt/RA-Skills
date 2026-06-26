# AI News Weekly Agent

Generate a weekly AI report in Markdown, including OpenClaw top skills, official announcements, industry news, and capped paper ratio.

## When to use
- User asks for weekly AI digest/report
- User wants OpenClaw skills ranking + AI news summary

## Command
```bash
python3 run_daily_digest.py --use-llm --llm-provider auto --window-hours 168 --max-paper-ratio 0.2 --min-official-items 3
```

## Required environment variables
- Ark mode:
  - `ARK_API_KEY`
  - `ARK_MODEL`
  - `ARK_ENDPOINT_ID` (recommended, `ep-xxx`)
- OpenAI-compatible mode:
  - `OPENAI_API_KEY`
  - `OPENAI_BASE_URL` (if ends with `/v1`, script auto-expands to `/chat/completions`)
  - `OPENAI_MODEL` (optional, but recommended)

Notes:
- In OpenClaw, these variables may be injected by the runtime.
- If not injected, users must provide them manually in runtime env or local `.env`.
- `--llm-provider auto` prefers Ark when Ark vars exist; otherwise uses OpenAI-compatible mode.
- Default security policy requires HTTPS endpoint and allowlisted LLM hosts.

## Optional environment variables
- `DIGEST_WEBHOOK_URL`: webhook for send notifications when using `--send`

## Environment template
Use runtime env injection in OpenClaw, or copy this template to local `.env`:

```env
ARK_API_KEY=
ARK_MODEL=Doubao-Seed-1.6-lite
ARK_ENDPOINT_ID=
OPENAI_API_KEY=
OPENAI_BASE_URL=
OPENAI_MODEL=
DIGEST_WEBHOOK_URL=
```

## External network access
This skill may access these external endpoints during execution:
- `https://ark.cn-beijing.volces.com` (Ark LLM API)
- `OPENAI_BASE_URL` target (OpenAI-compatible provider endpoint)
- `https://topclawhubskills.com` (OpenClaw leaderboard snapshot)
- RSS/news URLs listed in `sources.json`
- Optional webhook hosts for notification: Feishu/Lark or DingTalk

## Security and data handling
- No API keys are hardcoded in repository files.
- `.env` is not tracked and should never be committed.
- Only report-generation inputs are sent to LLM when `--use-llm` is enabled.
- Users should review and trust the configured endpoints before running.
- SSL verification is enabled by default. Insecure SSL fallback requires explicit `--allow-insecure-ssl`.
- Custom LLM endpoint hosts are blocked by default unless `--allow-custom-llm-endpoint` is provided.
- Optional extension: set `LLM_ALLOWED_HOSTS` (comma-separated) to add trusted hosts.
- Webhook only supports HTTPS and official Feishu/Lark/DingTalk domains.

## Publishing note
- For ClawHub publish, confirm the MIT-0 license checkbox in the web UI.