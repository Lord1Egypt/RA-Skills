# Model routing

## Principle

The voice skill should not hard-code a separate AI model.
It should pass transcript context to OpenClaw and let OpenClaw decide how to answer.
The default should feel like a normal chat agent first, with custom model choice optional later.

## Recommended routing order

1. **Session-backed OpenClaw reply**
   - best for owned conversation state and tool use
2. **HTTP OpenClaw reply**
   - good fallback when session routing is unavailable
3. **Local/simple reply path**
   - good for short status/help/time style prompts

## Helpful config ideas

- `OPENCLAW_AGENT_ID` — which OpenClaw agent owns the voice session
- `OPENCLAW_MODEL` — model alias used by the agent runtime
- `OPENCLAW_REPLY_STRATEGY` — `session-first`, `http-first`, `session-only`, `http-only`
- `OPENCLAW_FAST_ANSWER_FIRST` — ask for the short answer first
- `DISCORD_VOICE_FAST_LOCAL_FIRST` — answer tiny prompts locally before the remote call

## What to tell users

- If they already have Discord installed, they should usually only need the voice channel id.
- If not, they need Discord setup first, then the voice channel id.
- By default, it should behave like OpenClaw’s normal chat agent.
- Users can change the model later if they want a different voice persona or speed profile.
