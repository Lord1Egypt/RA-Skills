# 8917-minimax-toolkit Trust & Transparency Note

## Why a safety scanner may flag this skill as "caution" or "suspicious"

This skill can look sensitive because it does two things that security scanners treat conservatively:

1. It may read a MiniMax Token Plan API key from:
   - `MINIMAX_API_KEY`
   - or `~/.openclaw/openclaw.json` when running inside OpenClaw

2. It may upload user-provided media files to MiniMax APIs, such as:
   - reference images
   - audio samples for voice cloning
   - media inputs for video templates

These behaviors are intentional and required for the skill to work, but they must be disclosed clearly.

## What this skill does **not** do

- It does **not** hardcode API keys
- It does **not** claim to process media locally when it actually uploads it
- It does **not** silently write outputs to a hidden personal path anymore

## Transparency rules for this skill

- Output paths must be shown clearly to the user
- Token Plan request usage must be disclosed before execution
- OpenClaw config lookup must be described explicitly
- Media upload behavior must be disclosed explicitly

## One-line summary

This skill is not dangerous by design, but it performs sensitive actions (key lookup and third-party media upload) that require explicit disclosure to appear trustworthy to users and scanners.
