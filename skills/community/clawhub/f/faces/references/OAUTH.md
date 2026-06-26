# OAuth — Connect ChatGPT (connect plan only)

Connect-plan users can link their own ChatGPT Plus/Pro account so inference routes through their subscription at $0 cost.

**The human must approve once in their browser. After that, tokens are stored server-side and the agent never asks again.**

```bash
# 1. Check if already connected — do this first, skip below if openai is listed
faces auth:connections --json

# 2. If not connected — start the flow (opens browser automatically, or use --manual on headless)
faces auth:connect openai
# → prints URL, waits, detects completion automatically via polling

# 3. Confirm
faces auth:connections --json   # should show openai

# 4. Disconnect
faces auth:disconnect openai
```

**`--manual` flag** (headless / no browser on this machine): prints the authorize URL for the human to open on any device, polls for completion, also accepts a pasted callback URL as fallback.

**Tasking the human:** if `auth:connections` returns `[]`, tell the human: *"Run `faces auth:connect openai` in your terminal, or open the authorize URL in your browser and approve access. I'll detect it automatically."*

Once connected, OAuth routing is transparent — no flag needed on inference commands. Requests to gpt-5.x models via `chat:responses` route through the user's ChatGPT subscription automatically. Fallback to system key happens silently if the token is invalid.
