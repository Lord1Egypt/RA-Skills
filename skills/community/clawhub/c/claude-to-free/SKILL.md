---
name: claude-to-free
description: Migrate OpenClaw from Claude subscription OAuth to a free or cheap model provider (OpenRouter, Gemini, Ollama). Use when the user says Claude stopped working, gets an auth error, mentions the Anthropic April 2026 subscription ban, or asks to switch models without paying Anthropic more.
---

# Model Migration Skill

Help the user migrate OpenClaw from Claude subscription OAuth to a free or cheap provider.

## When to use this skill

- User says Claude is blocked, not working, or requires "extra usage"
- User mentions the April 2026 Anthropic harness policy change
- User wants to switch to Gemini, OpenRouter, Ollama, or any non-Claude provider
- User asks "how do I use OpenClaw without Claude?"

---

## Step 1 — Diagnose

Read the current config and identify what's broken:

```bash
cat ~/.openclaw/openclaw.json | python3 -c "
import json,sys
d=json.load(sys.stdin)
auth = d.get('auth',{})
profiles = auth.get('profiles',{})
model = d.get('agents',{}).get('defaults',{}).get('model',{}).get('primary','not set')
print('Current model:', model)
for name, p in profiles.items():
    print(f'Auth profile: {name} provider={p.get(\"provider\")} mode={p.get(\"mode\")}')
"
```

If you see `provider=anthropic mode=oauth` — that's the blocked profile. Proceed.

---

## Step 2 — Recommend a path

Ask the user one question: **"Do you want free (no cost) or are you okay with a small per-token charge for better quality?"**

### Free path (recommended for most users)
→ OpenRouter free tier — no credit card, no cost

Best free models right now:
- `openrouter/free` — auto-picks the best free model (zero config)
- `openrouter/meta-llama/llama-3.3-70b-instruct:free` — strong general model
- `openrouter/qwen/qwen3-coder:free` — best free coding model (262k context)
- `openrouter/qwen/qwen3.6-plus:free` — 1M context, free

### Cheap paid path ($0.10/MTok — roughly $1–5/month for typical use)
- `openrouter/google/gemini-2.5-flash-lite` — Google's fast model, 1M context
- `openrouter/google/gemini-2.0-flash-001` — excellent quality/price
- `openrouter/meta-llama/llama-3.3-70b-instruct` — same as free but reliable

### Free + local path (privacy-first)
→ Ollama — runs on the user's machine, zero cost, fully private

### Free direct (Gemini API)
→ Google AI Studio free tier — check current limits at aistudio.google.com (varies by account/region)

---

## Step 3 — Migrate using OpenClaw CLI (preferred)

Use native OpenClaw commands — `openclaw onboard` creates the auth profile and config in one shot:

```bash
# 1. Add your provider (example: OpenRouter free)
openclaw onboard --non-interactive --accept-risk --auth-choice openrouter-api-key --openrouter-api-key YOUR_OPENROUTER_KEY --skip-channels --skip-skills --skip-search --skip-daemon --skip-health --skip-ui

# 2. Set a free model
openclaw models set openrouter/qwen/qwen3.6-plus:free

# 3. Restart
openclaw gateway restart
```

Or use the interactive auth helper:

```bash
openclaw models auth login --provider openrouter
# (follow prompts to paste your key)
openclaw models set openrouter/qwen/qwen3.6-plus:free
openclaw gateway restart
```

Get a free OpenRouter key at https://openrouter.ai/keys (no credit card required).

---

## Step 4 — Manual config (if wizard doesn't work)

### Option A: OpenRouter free (zero cost)

1. Get a free API key at https://openrouter.ai/keys (no credit card)
2. Run: `openclaw onboard --non-interactive --accept-risk --auth-choice openrouter-api-key --openrouter-api-key YOUR_KEY --skip-channels --skip-skills --skip-search --skip-daemon --skip-health --skip-ui`
3. Set model: `openclaw models set openrouter/meta-llama/llama-3.3-70b-instruct:free`
4. Restart: `openclaw gateway restart`

### Option B: Gemini direct (free tier)

1. Get key at https://aistudio.google.com → Get API key
2. Run: `openclaw onboard --non-interactive --accept-risk --auth-choice gemini-api-key --gemini-api-key YOUR_KEY --skip-channels --skip-skills --skip-search --skip-daemon --skip-health --skip-ui`
3. Set model: `openclaw models set google/gemini-2.5-flash-lite`
4. Restart: `openclaw gateway restart`

### Option C: Ollama (local or cloud free tier)

1. Install: `curl -fsSL https://ollama.com/install.sh | sh` (or use cloud: ollama.com)
2. Pull a model: `ollama pull llama3.2`
3. Run: `openclaw onboard --non-interactive --auth-choice ollama --accept-risk`
4. Set model: `openclaw models set ollama/llama3.2`
5. Restart: `openclaw gateway restart`

---

## Step 5 — Verify

**First, confirm the auth profile exists for the new provider:**

```bash
openclaw models status
```

Check that the output lists the expected auth profile (e.g. `openrouter`, `google`, `ollama`). **If it's missing, the gateway will silently fall back to the first working provider (usually Anthropic) — the model set in config doesn't matter without a matching auth profile.**

If the auth profile is missing → go back to Step 3/4 and run `openclaw onboard` for that provider first. Then re-run `openclaw models set` and restart.

Only once the auth profile is confirmed, verify the active model:

```bash
openclaw models status --plain | grep -i "primary\|model"
```

`openclaw models status` verifies the configured model/auth state, not necessarily the live runtime model already attached to an existing Telegram chat session.

To verify the live runtime model, start a new chat/session (or reset the current one) and then check `/status`.

If the config still looks stale after confirming the auth profile exists, restart the gateway with the portable CLI command:

```bash
openclaw gateway restart
```

---

## Common errors

| Error | Cause | Fix |
|-------|-------|-----|
| `401 Unauthorized` | Invalid API key | Re-enter key, check for typos |
| `model not found` | Wrong model ID | Check exact ID in guide |
| `connection refused` | Ollama not running | Run `ollama serve` |
| `RESOURCE_EXHAUSTED` | Free tier rate limit | Wait or switch to paid tier |
| Config not applied | Gateway cached old config | Full restart via systemd |

---

## Resources

- Full guides: <https://github.com/BlueBirdBack/openclaw-without-claude>
- Free model list: <https://github.com/BlueBirdBack/openclaw-without-claude/blob/main/guides/model-comparison.md>
- Model-migration skill (ClawHub source): <https://github.com/BlueBirdBack/openclaw-without-claude/tree/main/skills/model-migration>
- Need hands-on help: <https://bluebirdback.com> (OpenClaw rescue, $99 fixed)

---

## Changelog

- **v1.0.2** (2026-04-04): Add required `--accept-risk` to non-interactive onboarding examples. Add `--skip-health` alongside `--skip-daemon` so the examples work on broken/stopped local gateways. Clarify that `openclaw models status` verifies configured state, not necessarily the live runtime model in an existing Telegram session. Switch fallback restart guidance back to portable `openclaw gateway restart`.
- **v1.0.1** (2026-04-04): Fix broken CLI commands — `--auth-choice apiKey --token-provider openrouter` was never valid. Updated to `--auth-choice openrouter-api-key --openrouter-api-key KEY` with `--skip-*` flags for non-interactive flow. Fixed Gemini auth from `google-api-key` to `gemini-api-key`. Added `openclaw models auth login` as alternative flow. Updated verification to use `--plain` flag.
