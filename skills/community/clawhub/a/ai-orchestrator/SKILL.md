---
name: ai-orchestrator
description: >
  DeepSeek AI access via Puppeteer browser automation with CDP interceptor. Persistent daemon (~35ms startup),
  health checks, graceful shutdown, PM2 management. Configurable via `.deepseek.json`.
  Use when: (1) need DeepSeek responses without API key, (2) code analysis, review, or generation,
  (3) text analysis, summarization, translation, (4) "consult DeepSeek" or ask-deepseek.sh.
---

# AI Orchestrator v2.0.11

**What this is:** Browser automation that talks to DeepSeek via Puppeteer.
**What this is NOT:** A general AI router or multi-model orchestrator. It's one browser → one LLM.

## Execution

**Working directory rule:** Unless a command here uses an absolute path, run ai-orchestrator commands from the skill root: `~/.openclaw/workspace/skills/ai-orchestrator`.
If you are not already there, run:

```bash
cd ~/.openclaw/workspace/skills/ai-orchestrator
```

Relative paths such as `.daemon-ws-endpoint`, `.profile/`, `.deepseek.json`, and `scripts/setup-daemon.sh` assume this directory.

## Quick Start
```bash
# Simple question
ask-deepseek.sh "What is HTTP?"

# Session (keeps context between questions)
ask-deepseek.sh "Explain OAuth2" --session work
ask-deepseek.sh "What about OpenID Connect?" --session work
ask-deepseek.sh --session work --end-session

# With daemon (fast startup ~35ms vs ~15s cold)
ask-deepseek.sh "Question" --daemon

# Pipe code or long prompts
cat code.py | ask-deepseek.sh "Find bugs"
ask-deepseek.sh --stdin < code.py
ask-deepseek.sh <<'EOF'
Long multi-line prompt here
EOF
```

## When to use ai-orchestrator

| Task | ai-orchestrator | Direct API | Manual browser |
|------|----------------|------------|----------------|
| Code analysis / review | ✅ Fast, no API key | Needs API | ❌ Slow |
| Text analysis / summary | ✅ (with --daemon) | Needs API | ❌ Tedious |
| Brainstorming | ❌ (use Dual Thinking skill) | Needs API | ❌ |
| Web scraping | ❌ Wrong tool | ❌ | ✅ |
| API testing | ❌ Overkill | ✅ | ❌ |
| CAPTCHA solving | ❌ Will fail | ❌ | ✅ (manual) |

**Rule:** Need LLM reasoning without API key → ai-orchestrator.
Need browser tasks (scrape, click, fill forms) → use `agent-browser` skill instead.

**Default site mode:** ai-orchestrator must keep DeepSeek in **Expert** mode whenever the site exposes the `Instant` / `Expert` switch. Treat `Expert` as the canonical default. Do not fall back to `Instant` unless a future implementation explicitly adds an override and the user asks for it.

**Session continuity:** in daemon mode, follow-up requests using `--session NAME` must restore the exact saved DeepSeek `chatUrl` for that session unless `--new-chat` was explicitly requested. Reusing an arbitrary open DeepSeek tab is incorrect because it breaks multi-round review continuity.

## All Flags
| Flag | Purpose |
|------|---------|
| `--session NAME` | Persistent context across requests (keeps chat history) |
| `--daemon` | Use running Chrome daemon (~35ms startup) |
| `--search` | Enable DeepSeek web search capability |
| `--think` | Enable DeepThink site mode (deeper reasoning) |
| `--new-chat` | Start new chat within existing session |
| `--end-session` | Close and clean up session |
| `--visible` | Open visible browser (for auth/CAPTCHA fixes) |
| `--wait` | Wait for manual auth completion (with --visible) |
| `--close` | Force close browser after request |
| `--dry-run` | Test auth + composer without sending prompt |
| `--stdin` | Explicitly read prompt body from stdin |
| `--debug` | Verbose debug output |
| `--verbose` | More detailed logs |
| `-h, --help` | Show help |

## Health check
```bash
# 1. Daemon running?
pm2 status | grep -q "deepseek.*online" || echo "Daemon down"

# 2. Dry-run path works?
ask-deepseek.sh --dry-run --daemon || echo "DeepSeek dry-run failed"  # Checks auth + composer through the daemon path

# 3. Real response path works?
ask-deepseek.sh "OK" --daemon | grep -q "OK" || echo "DeepSeek not responding"
```

If any step fails, do not improvise. Use the troubleshooting ladder below.

## Failure Recovery (mandatory routing)

### First failure rule — do not skip
When any command fails:
1. **STOP** — do not try a random second fix yet
2. **CAPTURE** — read the exact error you saw
3. **MATCH** — find the closest symptom row below
4. **RUN** — execute that row's exact command
5. **VERIFY** — retry with the specified verification command

### Symptom → exact command
| If you see this symptom | Run this exact command | Then verify with |
|---|---|---|
| `Connection refused`, `ECONNREFUSED`, daemon not online | `pm2 restart deepseek-daemon && sleep 8 && ask-deepseek.sh --dry-run --daemon` | `ask-deepseek.sh "Say OK" --daemon` |
| `auth expired`, `CAPTCHA`, login page, `401`, `403` | `cd ~/.openclaw/workspace/skills/ai-orchestrator && pm2 stop deepseek-daemon && rm -f .daemon-ws-endpoint && bash ask-deepseek.sh --visible --wait --dry-run && pm2 start deepseek-daemon` | `bash ask-deepseek.sh --dry-run --daemon` |
| response cuts off / incomplete long answer | `ask-deepseek.sh "Part 1" --session temp && ask-deepseek.sh "Continue with next part" --session temp` | `ask-deepseek.sh --session temp --end-session` |
| `lock`, `Singleton`, profile already in use | `cd ~/.openclaw/workspace/skills/ai-orchestrator && rm -f .profile/Singleton* && pm2 restart deepseek-daemon` | `bash ask-deepseek.sh --dry-run` |
| `timeout`, selector missing, composer not found | `ask-deepseek.sh --dry-run --visible` | only after manual inspection consider selector edits |

### If 3 fixes failed already
Do not keep guessing. Reset to a known-good baseline:

```bash
cd ~/.openclaw/workspace/skills/ai-orchestrator
pm2 stop deepseek-daemon
pkill -f puppeteer || true
rm -f .daemon-ws-endpoint .profile/Singleton*
bash scripts/setup-daemon.sh
bash ask-deepseek.sh "Say OK" --daemon
```

If that still fails, escalate to manual auth/inspection with `--visible --wait`.

## Manual Auth with --wait

`--wait` blocks until you complete auth in the visible browser or interrupt the command yourself.
There is no automatic timeout documented here.
Use Ctrl+C if you need to abort.

## Daemon Setup
**One-liner:**
```bash
cd ~/.openclaw/workspace/skills/ai-orchestrator && bash scripts/setup-daemon.sh
```

**Or manual:**
```bash
bash scripts/setup-daemon.sh  # Or run step-by-step below
npm install   # First time only
pm2 start deepseek-daemon.js --name deepseek-daemon --no-autorestart
pm2 save
pm2 startup   # Auto-start on boot
```

## Exit Codes
| Code | Meaning | Action |
|------|---------|--------|
| 0 | Success — response received | Continue |
| 1 | Config/arg error | Check flags, run `--help` |
| 2 | DeepSeek unreachable or daemon unavailable | Check network, daemon endpoint, pm2 status |
| 3 | Blocked or rate limited | Wait 5s, retry, or use --visible |

**Note:** Partial success (truncated response) still returns 0. Use "Continue" button handling.

## Known Limitations (v2.0.11)
- **Exact-string prompts:** DeepSeek may prepend explanation text before the requested suffix. For machine-sensitive checks, prefer structured JSON prompts when possible, or validate that the returned payload still contains the expected terminal token instead of assuming exact literal obedience.
- **Oversized prompts:** if a giant single-shot prompt does not actually leave the page, ai-orchestrator now validates submit outcome, retries with adaptive shortening, and fails explicitly with `DEEPSEEK_SUBMIT_BLOCKED_OVERSIZE_PROMPT` if delivery never succeeds.
- **Publish hygiene:** local runtime state must not be published. Before ClawHub publish, verify that `.clawhubignore` excludes local profile, diagnostics, logs, sessions, and daemon state files.

## DeepSeek Free Tier Limits
- **Per response: ~13,000 characters** (verified 2026-04-03)
- **Button "Continue"** auto-clicked up to 30 times
- **Rate limit:** 5 seconds between requests
- **Session limit:** Use `--session` for long conversations instead of single huge prompts

### Workaround for Long Answers (>13k chars)
```bash
ask-deepseek.sh "Write a Python backend guide" --session guide
ask-deepseek.sh "Now cover async and databases" --session guide  # Continue
ask-deepseek.sh --session guide --end-session  # Done
```

## Logging
After important orchestrator runs, append to `memory/episodic/YYYY-MM-DD.md`:
```markdown
## ai-orchestrator
- Task: code review app.js (tool: deepseek, duration: 12s, status: success)
- Failure: CAPTCHA on deepseek (fallback: manual via --visible)
```
Not every request needs logging. Log decisions and failures, not routine questions.

## What NOT to do
- ❌ Use for web scraping or browser automation (wrong tool — use agent-browser skill)
- ❌ Bypass Dual Thinking for complex decisions (orchestrator executes, doesn't think)
- ❌ Ignore failure logs (they tell you what's broken)
- ❌ Run without --daemon unless debugging (cold start = 15s vs 35ms)
- ❌ Guess random fixes when a known failure case already matches
- ❌ Open a visible browser first if the problem is only a dead daemon — restart daemon first
- ❌ Keep reusing one broken long prompt after free-tier cutoff — switch to `--session` chunks instead

## Configuration (.deepseek.json)
```json
{
  "idleTimeout": 15000,
  "heartbeatInterval": 15000,
  "domErrorIdleMs": 25000,
  "maxContinueRounds": 30,
  "logToFile": true,
  "logPath": ".logs/deepseek.log"
}
```

## Minimal Contract for Weak Runtimes
- **Exit codes:** `0` = success, `1` = config/runtime error, `2` = DeepSeek unreachable or daemon unavailable, `3` = blocked or rate-limited. Never treat `2` or `3` as success.
- **Mode enforcement:** when DeepSeek shows `Instant` / `Expert`, ai-orchestrator must use `Expert` unless the user explicitly requests otherwise via a future supported override.
- **Session restore:** `--session NAME` must restore the exact saved `chatUrl` unless `--new-chat` was explicitly requested.
- **Publish hygiene:** before publishing to ClawHub, ensure `.clawhubignore` exists and excludes local runtime state.

## Minimal Decision Rules for Weak Models

When choosing what to do next, use these defaults:
- Need fastest normal run → use `--daemon`
- Need context across multiple prompts on one topic → use `--session`
- Need a brand new DeepSeek chat for that topic → add `--new-chat`
- Need to close the topic chat → use `--end-session`
- Need auth/login repair → stop daemon first, then `--visible --wait --dry-run`
- Need a health check without sending a real prompt → use `--dry-run`
- Need a long answer → use `--session` and split it into chunks
- Need browser automation on websites → stop and use `agent-browser`, not ai-orchestrator`
- Need failure recovery → do not guess; use the symptom table above
- Before every real prompt send, keep the DeepSeek site in `Expert` mode when that switch exists
- If `--think` is used, enable the site `DeepThink` toggle before sending the prompt

## Troubleshooting → REFERENCE.md
See **REFERENCE.md** for:
- Architecture overview (Puppeteer + CDP interceptor)
- Complete troubleshooting guide
- Diagnostic system (trace + metrics + summary JSON + file log)
- Performance benchmarks
- Common issues: CAPTCHA, rate limits, selector changes, visible-browser vs daemon behavior
