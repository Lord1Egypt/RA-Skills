# Integration Notes

## Design goal

Claw Xiaoai should feel like a consistent character, while staying easy to port across different OpenClaw plugins or repos.

## Recommended separation

Split the implementation into three layers:

1. **Persona layer**
   - Backstory
   - Tone of voice
   - Visual identity
   - Behavioral rules

2. **Trigger layer**
   - Which user requests should trigger selfies
   - How mirror vs direct mode is selected
   - Whether proactive selfie behavior is enabled

3. **Provider layer**
   - Image backend
   - API keys / secrets
   - Model names
   - Optional TTS backend

## Naming guidance

Use `claw-xiaoai` as the skill/package identity, but keep the in-character display name as `Claw Xiaoai`.

## Porting rules

- Do not hardcode provider credentials in prompt text.
- Do not mix installation instructions into the persona file.
- Keep the persona reusable even if the backend changes from fal.ai to another provider.
- If a repo uses SOUL.md-style persona injection, place only the in-character prompt there; keep config elsewhere.

## Good defaults

- Start with direct selfie replies only; enable proactive selfies later.
- Keep responses short and natural unless the user asks for richer roleplay.
- Treat visuals as an extension of persona, not the entire personality.
