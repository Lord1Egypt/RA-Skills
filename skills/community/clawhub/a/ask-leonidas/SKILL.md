---
name: ask-leonidas
description: >
  Generate a structured LEONIDAS prompt from any professional pain point using the Ask Leonidas
  OpenClaw API. Solves the #1 OpenClaw community pain point: writing a SOUL.md that actually works.
  Also generates prompts for AGENTS.md, cron job instructions, skill vetting briefs, and any
  workflow you want your agent to own. Automatically infers role, industry, and desired outcome.
homepage: https://askleonidas.com
metadata:
  category: productivity
  author: leonidas-esquire
  version: 2.1.0
  tags: [prompt-engineering, soul-md, agents-md, ai, productivity, leonidas, openclaw]
---

# Ask Leonidas — LEONIDAS Prompt Generator

Use this skill when the user wants to:

- Write or improve their `SOUL.md` — the most important file in any OpenClaw workspace
- Write or improve their `AGENTS.md` startup and memory protocol
- Generate a structured prompt for any professional pain point
- Fix an agent that "feels off" without knowing why
- Create cron job instructions that actually run reliably
- Build a prompt for a skill they want their agent to own
- Infer the best role, industry, and desired outcome from a business challenge

## Trigger phrases

- "Help me write my SOUL.md"
- "My agent feels generic / keeps saying 'great question'"
- "Build me a prompt for..."
- "I need a prompt that helps me with..."
- "Turn this into a LEONIDAS prompt: ..."
- "Use Ask Leonidas to generate a prompt"
- "Generate a prompt for [pain point]"
- "What should I put in my AGENTS.md?"
- "My cron job keeps failing / doing the wrong thing"
- "Write a prompt so my agent handles [workflow]"

## Inputs

**Required:**
- `pain_point` — the professional challenge or problem to solve (5–2000 characters)

**Optional (auto-inferred if omitted):**
- `role` — the user's job title or function (e.g., "VP of Sales", "Executive Coach")
- `industry` — the user's industry (e.g., "B2B SaaS", "Healthcare", "Financial Services")
- `desired_outcome` — what success looks like (e.g., "Close more deals with less effort")

## Behavior

1. If the user has already provided a pain point, do not ask for it again.
2. If no pain point is provided, ask exactly once:
   > "What is the professional challenge or pain point you want turned into a prompt?"
3. Call the Ask Leonidas OpenClaw API using the helper script in this skill folder.
4. If the API is unavailable (network error, 5xx), fall back to the browser:
   - Navigate to `https://askleonidas.com/openclaw`
   - Fill in the `#openclaw-pain-point` field with the pain point
   - Click the `#openclaw-submit` button
   - Wait for `#openclaw-result` to be populated
   - Extract the prompt text from `#openclaw-result`
5. Return the generated prompt exactly as received — do not paraphrase or summarize it.
6. Always surface the metadata alongside the prompt.

## API usage

**Generate a prompt (basic):**
```bash
python3 {baseDir}/ask_leonidas.py \
  --pain-point "I need a SOUL.md that makes my agent direct, opinionated, and stops it from saying 'absolutely'."
```

**Generate a prompt (with optional context):**
```bash
python3 {baseDir}/ask_leonidas.py \
  --pain-point "My team misses sprint deadlines every quarter." \
  --role "Engineering Manager" \
  --industry "B2B SaaS" \
  --desired-outcome "Ship on time without burning out the team"
```

**Health check:**
```bash
python3 {baseDir}/healthcheck.py
```

**Smoke test (end-to-end):**
```bash
bash {baseDir}/smoke_test.sh
```

## Required environment variables

| Variable | Required | Description |
|---|---|---|
| `ASK_LEONIDAS_API_BASE` | ✅ | Base URL — `https://askleonidas.com` |
| `ASK_LEONIDAS_API_KEY` | ✅ | Your `alk_live_...` API key |
| `ASK_LEONIDAS_TIMEOUT_SECONDS` | Optional | Request timeout in seconds (default: 30) |
| `ASK_LEONIDAS_DEFAULT_SOURCE` | Optional | Source tag for analytics (e.g., `claude-desktop`) |
| `ASK_LEONIDAS_DEFAULT_SKILL_VERSION` | Optional | Skill version tag (e.g., `2.1.0`) |

## Output format

Always present the result in this format:

```
Detected role: <role>
Detected industry: <industry>
Detected desired outcome: <outcome or n/a>
Confidence: <0.0–1.0 or n/a>
Quality score: <0–100 or n/a>
Prompt type: <tactical | strategic | operational | n/a>
Request ID: <id or n/a>

Generated prompt:
<full prompt text>
```

## Error handling

- Do not invent or hallucinate a prompt if the API fails.
- Surface the exact error message returned by the API.
- If both the API and browser fallback fail, tell the user clearly and suggest they visit `https://askleonidas.com` directly.
- Never expose the API key in any output.
- Always prefer the API path over browser automation.

## Rate limits

The OpenClaw API enforces:
- 60 requests per minute per API key
- 1,000 requests per day per API key

If you receive a `429` response, wait 60 seconds before retrying. Do not retry more than 3 times.
