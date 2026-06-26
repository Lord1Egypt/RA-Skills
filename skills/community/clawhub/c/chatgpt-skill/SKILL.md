---
name: chatgpt-skill
description: Automate ChatGPT Web conversations through a local browser session with persistent login state, one-shot prompts, reusable multi-turn sessions, and conversation metadata storage. Use when OpenClaw/Codex needs ChatGPT-style normal dialogue through the web UI instead of the OpenAI API, including login setup, continued conversations, session reuse, or browser-based troubleshooting.
---

# ChatGPT Web Skill

Use this skill to drive the ChatGPT Web UI through a local browser profile.

## Core Purpose

- Reuse ChatGPT login state stored inside the skill directory
- Start a fresh conversation or reopen an existing one
- Ask one-off questions through a normal browser page
- Keep a long-lived browser session for multi-turn dialogue

## Always Use `python3 scripts/run.py`

Always run commands through the wrapper:

```bash
python3 scripts/run.py auth_manager.py status
python3 scripts/run.py auth_manager.py validate
python3 scripts/run.py auth_manager.py setup
python3 scripts/run.py ask_chatgpt.py --question "你好"
python3 scripts/run.py session_manager.py create
```

The wrapper ensures the local `.venv` exists, installs dependencies, and runs the target script with the correct interpreter.

## Authentication Flow

1. Check local state:

```bash
python3 scripts/run.py auth_manager.py status
```

2. Validate the real browser state:

```bash
python3 scripts/run.py auth_manager.py validate
```

3. If needed, complete login manually in a visible browser:

```bash
python3 scripts/run.py auth_manager.py setup
```

4. To clear local auth/profile data:

```bash
python3 scripts/run.py auth_manager.py logout
```

## Basic Chat Flow

One-shot question:

```bash
python3 scripts/run.py ask_chatgpt.py --question "你好"
```

Debug in visible browser:

```bash
python3 scripts/run.py ask_chatgpt.py --question "总结这段文本" --show-browser
```

Continue a known conversation id:

```bash
python3 scripts/run.py ask_chatgpt.py --conversation-id <conversation_id> --question "继续"
```

Ask with an explicit model workflow and save a proof screenshot:

```bash
python3 scripts/run.py ask_chatgpt.py \
  --new-chat \
  --model "GPT 5.4 Thinking" \
  --extended-thinking \
  --proof-screenshot \
  --question "请你推荐最近一个月，RLVR领域的论文"
```

## Persistent Session Flow

Create a reusable session:

```bash
python3 scripts/run.py session_manager.py create
python3 scripts/run.py session_manager.py create --conversation-id <conversation_id>
```

Ask follow-up questions in the same tab:

```bash
python3 scripts/run.py session_manager.py ask --session-id <session_id> --question "继续问"
```

You can also switch model, force a fresh chat, enable `Extended thinking`, and save a proof screenshot in the same call:

```bash
python3 scripts/run.py session_manager.py ask --session-id <session_id> --new-chat --model "GPT 5.4 Thinking" --extended-thinking --proof-screenshot --question "请你推荐最近一个月，RLVR领域的论文"
```

Inspect or maintain sessions:

```bash
python3 scripts/run.py session_manager.py list
python3 scripts/run.py session_manager.py info --session-id <session_id>
python3 scripts/run.py session_manager.py reset --session-id <session_id>
python3 scripts/run.py session_manager.py close --session-id <session_id>
python3 scripts/run.py session_manager.py gc
```

## Data Storage

All data stays inside the skill directory:

- `data/auth_info.json` — auth metadata and last validation status
- `data/browser_state/` — cookies, storage state, persistent browser profile
- `data/conversations.json` — discovered/opened conversation metadata
- `data/sessions.json` — persistent session metadata
- `data/session_runtime/` — daemon socket, pid, and runtime artifacts
- `data/screenshots/` — debug screenshots captured on failures

## Error Model

The scripts return explicit machine-readable errors for cases such as:

- not logged in
- redirected to login
- account chooser encountered
- CAPTCHA / 2FA / human verification required
- page load failed
- prompt input missing
- send path unavailable
- reply timeout
- empty reply
- page structure changed
- session not found
- invalid conversation id
- session daemon unavailable
- browser profile in use
- network or proxy failure

## Best Practices

- Validate auth before deeper automation
- Use `--show-browser` when the UI changes
- Prefer persistent sessions for multi-turn workflows
- Keep proxy env vars explicit on Linux when network behavior is unstable
- Inspect `data/screenshots/` and JSON error payloads before patching selectors

## Limitations

- ChatGPT Web selectors can change without notice
- A blank new chat may still not expose a stable server conversation id until the first message is sent; the skill also probes frontend state, storage, and resource history, and may fall back to a client thread id such as `WEB:...` when ChatGPT keeps the URL at `/`
- Some login or risk-review flows require manual intervention
- Conversation deletion is intentionally left unimplemented until the web flow is stable enough
