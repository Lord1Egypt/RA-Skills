# chatgpt-skill

Automate normal ChatGPT Web conversations through a local browser session instead of the OpenAI API.

## What it does

- Reuse local ChatGPT login state
- Validate browser auth state
- Ask one-off questions
- Reuse persistent multi-turn sessions
- Start a fresh chat, switch model, enable Extended thinking, and optionally save a proof screenshot
- Persist conversation/session metadata locally for reuse

## Requirements

- Python 3
- A local browser environment supported by Patchright
- A valid ChatGPT Web login
- On Linux, explicit proxy environment variables may be needed when network conditions are unstable

## Quick start

```bash
python3 scripts/run.py auth_manager.py status
python3 scripts/run.py auth_manager.py validate
python3 scripts/run.py auth_manager.py setup
python3 scripts/run.py ask_chatgpt.py --question "你好"
python3 scripts/run.py session_manager.py create
```

## Model workflow example

```bash
python3 scripts/run.py ask_chatgpt.py \
  --new-chat \
  --model "GPT 5.4 Thinking" \
  --extended-thinking \
  --proof-screenshot \
  --question "请你推荐最近一个月，Tool-Calling 领域的论文"
```

## Persistent session example

```bash
python3 scripts/run.py session_manager.py create
python3 scripts/run.py session_manager.py ask --session-id <session_id> --question "继续"
```

## Privacy and local state

This package does not ship with any login state, browser profile, screenshots, or session data. Runtime artifacts are created locally under `data/` on first use.

## Limitations

- ChatGPT Web selectors can change without notice
- Some login, CAPTCHA, 2FA, or risk-review flows still require manual intervention
- Network and proxy conditions can affect page load stability
- Conversation deletion is intentionally not implemented yet

See `SKILL.md` and `references/` for detailed usage and troubleshooting.
