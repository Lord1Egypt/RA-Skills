# clawlyra — give your OpenClaw agent a face and a voice

**On ClawHub:** https://clawhub.ai/Freespirits/clawlyra — `openclaw skills install @Freespirits/clawlyra`

This is an [OpenClaw](https://github.com/openclaw/openclaw) AgentSkill that turns
**[Lyra](https://github.com/Freespirits/lyra-ai-companion)** — a self-hosted 3D
avatar companion — into the talking, lip-synced, *performing* face of **your own
OpenClaw agent**.

## How it works (skill + sidecar)

An AgentSkill can't render anything itself — it teaches your agent *how* to speak.
So this is two pieces:

- **This skill** teaches your OpenClaw agent to reply as Lyra and to emit her
  inline control tags (`[affect:...]`, `[gesture:...]`, `[scene:...]`, and
  audio-emotion cues) — see `SKILL.md`.
- **Lyra** (the app) is the sidecar that *renders* it: it connects to your
  OpenClaw Gateway as an operator, streams your agent's reply into her voice and
  3D body with exact lip-sync, and performs every tag. Your brain, memory, and
  tools stay entirely inside OpenClaw — **zero model configuration.**

## Setup

1. **Install the skill** into your OpenClaw:
   ```
   openclaw skills install @Freespirits/clawlyra
   ```
   (or `openclaw skills install ./skills/clawlyra --as clawlyra` from a checkout)

2. **Run Lyra** pointed at your gateway — set in Lyra's `.env`:
   ```
   LLM_PROVIDER=openclaw
   OPENCLAW_TOKEN=<gateway.auth.token from ~/.openclaw/openclaw.json>
   ```
   then `npm run dev`. See the [Lyra README](https://github.com/Freespirits/lyra-ai-companion)
   for full install (avatar assets, voice, content guard).

3. **Talk to her.** Your OpenClaw agent answers; Lyra speaks and performs it.

## Notes

- **The boundary:** the characters are friends, never romantic — that boundary is
  baked into their personas and is **always on**, independent of your agent and of
  any toggle. Lyra also ships an *optional* content guard (a keyword moderation
  pass, **off by default**) you can switch on with `LYRA_GUARD=on` for an extra
  layer; see the Lyra README.
- **Compatibility:** the exact tag vocabulary in `SKILL.md` mirrors Lyra's
  `server/protocol.js`. If you extend Lyra's gestures/affects/scenes, update the
  skill's lists to match.
- **License:** this skill (`SKILL.md`) is **MIT-0** on ClawHub — free to use,
  modify, and redistribute, no attribution. The **Lyra app** it drives is a
  separate project under **PolyForm Noncommercial 1.0.0** (personal use free;
  commercial use needs a license from the author).
