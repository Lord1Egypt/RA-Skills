# clawlyra — announcement / listing copy

Copy for ClawHub, social, and READMEs. All claims are verified working.

## Tagline

**Give your OpenClaw agent a face. clawlyra turns Lyra into the talking, lip-synced body for your own agent.**

## Short listing blurb (skill card)

> Every OpenClaw user wants a real talking avatar — and the guides all fall short
> on latency and lip-sync. **clawlyra** fixes that. It makes **Lyra** — a
> self-hosted 3D avatar companion — the face and voice of *your own* OpenClaw
> agent: it connects to your Gateway as an operator, streams your agent's replies
> straight into her voice with **exact lip-sync**, and she *performs* them —
> expressions, gestures, scene changes. Your brain, memory, and tools stay 100%
> inside OpenClaw. **Zero model config, fully local, fully yours.**

## Announcement post (longer)

**clawlyra — your OpenClaw agent, with a face and a voice**

Everyone's tried to give their agent an avatar. The results are usually a
pre-rendered clip you wait ten seconds for, with lip-sync that doesn't track.
That's not a companion — that's voicemail.

clawlyra does it properly. It pairs your OpenClaw agent with **Lyra**, an open,
self-hosted 3D avatar, using OpenClaw's own operator WebSocket:

- 🗣️ **Streams your agent's reply** token-by-token into a real voice — she starts
  talking as it generates, not after.
- 👄 **Exact lip-sync** (word-timestamped), not a loose loop.
- 🎭 **She performs** — the skill teaches your agent to emit inline tags, so she
  smiles, tilts, winks, changes the scene, shifts her mood mid-sentence.
- 🧠 **Zero model config** — the brain, memory, and tools stay entirely in *your*
  OpenClaw. Lyra is just the face.
- 🔒 **Local & private** — runs on your machine; the friends-never-romantic
  boundary is baked into every character and always on (an optional content guard
  adds an extra moderation pass).

**Get it:**
1. `openclaw skills install @Freespirits/clawlyra`
2. Run Lyra with `LLM_PROVIDER=openclaw` + your gateway token
3. Talk to your agent — and watch it come alive.

On ClawHub: **clawhub.ai/Freespirits/clawlyra** · App source (PolyForm Noncommercial): **github.com/Freespirits/lyra-ai-companion**
