
# Avatar Content Engine

> runtime (OpenClaw, Claude Code, and others), and works on OpenClaw, and also through **[PaioClaw.ai](https://paioclaw.ai)**.
> fill the `[BRAND]` slots with your own product. Runs on any AgentSkills-compatible

---
# UAIGC Avatar Engine- Create Viral Content (avatar-content-engine)
- Operate an AI-avatar short-form content engine — script, image, and video production for social-video avatars across TikTok, Reels, Shorts, and Facebook. 
- Use for avatar scripts, hooks, micro-moments, emotional arcs, brand vs niche content modes, avatar portrait generation, 2×2 reference grids, and Seedance / Kling / Wan lip-sync clips. 
- Trigger even when the request only names an avatar, a TikTok/Reel, a portrait, or a content pipeline — do not fall back to generic content advice when this pipeline applies.

---
\
A production system for generating emotionally-driven, platform-native short-form
video featuring AI avatars. It exists to solve one bottleneck: **creative supply**.
The value is velocity of distinct, high-quality creative — the raw material that ad
and recommendation algorithms need to optimize against — not a standalone acquisition
channel. Anchor every decision here.

The engine spans three stages:
1. **Script generation** — structured 16s two-clip scripts.
2. **Image generation** — consistent avatar portraits and reference grids.
3. **Video generation** — clip production, voice, and multi-clip continuity.

---

## 1. Core content philosophy

These principles override generic "best practice." Content that violates them reads
as hollow even when technically correct.

- **Emotion first, information last.** The goal is to mirror the viewer's exact
  internal state, not to inform them. A script should make a real person think
  *"this is me"* before it makes them think *"I learned something."* Push back on
  safe, fact-heavy drafts.
- **Channel division over repetition.** Voice, on-screen text, and visuals must each
  carry a *different* layer — emotion / the concrete point / the proof. When all
  three repeat the same thin message, the content feels empty. Specificity across
  channels is what makes sub-30s video feel substantial.
- **Specificity is the substance.** "A show" is dead; a named episode is alive.
  "A game" is dead; "your ping showing 20ms but the server feels like 300ms" is
  alive. Never generalize a micro-moment.
- **Payload discipline inside the format.** Each 8s clip carries roughly 18–22 words
  of dialogue and must land one concrete payload — a specific point, image, or proof —
  not filler. Word count is a symptom; the real fix is a defined payload per clip.

---

## 2. The avatars (example roster — customize)

Define a small roster of fixed personas. Each needs a locked persona, voice, target
audience, brand slot, and two content banks (a niche bank for no-brand content, a
brand bank for product-integrated content). Respect each avatar's voice and audience
exactly — voice drift is a known failure mode.

| Avatar | Brand slot | Persona | Voice (niche) | Core audience |
|---|---|---|---|---|
| **Nova** | `[BRAND]` | Gaming | Deadpan, self-aware Gen-Z gamer; dry humor; never tries too hard | Gamers 16–28, gym-gaming crossover, duo-queue culture |
| **Remy** | `[BRAND]` | Streaming | Enthusiastic, opinionated superfan; always has the hottest take | Binge-watchers, fandom communities, streaming obsessives |
| **Kai** | `[BRAND]` | AI Tech | Curious, slightly conspiratorial; "nobody talks about this" discoverer | Builders, solopreneurs, tech-curious 22–35, productivity obsessives |
| **Sable** | `[BRAND]` | Privacy / Security | Calm, precise, quietly alarming auditor; never conspiratorial; always cites specifics | Privacy-conscious individuals, compliance-aware businesses |

**Visual anchor:** give each avatar a fixed, describable look so generations stay
consistent — e.g. for Sable: 30s, glasses, dark crewneck, dual-monitor desk setup.

**Niche-mode rules (never mention the product in niche mode):**
- Gaming — name a specific game/mode/mechanic; use gamer vocabulary naturally.
- Streaming — name at least one real show, character, or actor; never "a show."
- AI Tech — reference a real tool by name (ChatGPT, Claude, Cursor, Notion AI, Make,
  Zapier, Perplexity); the moment must make a builder think *"I did this yesterday."*
- Privacy/Security — cite a concrete specific (a real breach pattern, a data-broker
  behavior, a permission most people never check); auditor energy, never fear-mongering.

**Trust-category caution:** trust-heavy categories (privacy, security, finance,
health) carry higher brand risk with AI-avatar content. Lead validation tests with
lighter categories (gaming, streaming) before exposing trust-heavy personas.

---

## 3. Script generation

### Output contract

Every script is a single JSON object. Never wrap it in markdown. Structure:

```json
{
  "hook_concept": "", "trend_used": "", "emotion_used": "", "micro_moment": "",
  "brand_integrated": false, "hook_score": 0, "tension_score": 0,
  "clip1": {"time":"0-8s","visual_direction":"","on_screen_text":"","dialogue":"","gesture":""},
  "clip2": {"time":"8-16s","visual_direction":"","on_screen_text":"","dialogue":"","gesture":""},
  "caption": "", "hashtags": ["","","","",""], "comment_cta": "", "why_it_works": ""
}
```

Optional blocks appear only when the matching system is on: `alt_hooks` (Hook A/B,
3 variants), `arc_posts` (5-post series). In silent/reaction mode both `dialogue`
fields are `"[silent]"` and the story is carried entirely by `on_screen_text` +
`gesture`.

### Hard structural rules

1. Hook stops the scroll in ≤2 seconds — emotion leads.
2. Every script is unique — a different micro-moment, opening line, or entry than any
   prior generation for that avatar.
3. Exactly one comment/tag mechanic is baked in.
4. Two clips × 8s = 16s total.
5. `visual_direction` ≤ 15 words and always includes clothing + camera angle + body
   position + one environment detail.

### Brand mode vs. niche mode

- **Niche mode** (default): no product mention. Script stays entirely in the avatar's
  world. Uses the niche bank.
- **Brand mode**: four integration styles —
  - `soft` — clip 1 pure pain; the product appears once, casually, at the end.
  - `story` — clip 1 frustration → clip 2 the product *is* the resolution.
  - `demo` — one feature solving the core pain, proven inside 16s.
  - `cta` — hook + problem → product value + direct CTA (link in bio).

### The 10 virality systems

Toggle these per generation. Sensible defaults on: emotion, moment, tension, drift,
duo, hooks, reformat.

1. **Emotion** — filter all output through one selected emotion (Rage, Nostalgia,
   Embarrassment, FOMO, Paranoia, Disbelief, Spite, Relief, Pride, Anxiety). Goal maps
   to an emotion set: awareness→relatable, engagement→argument-provoking,
   conversion→specific, viral→share-triggering.
2. **Micro-moment** — anchor the script to one hyper-specific moment pulled from the
   avatar's bank; avoid the last 5 used to prevent repetition.
3. **Audience flip** — write for the *secondary* audience (the partner watching the
   rager, the manager assigning manual work) in the same voice.
4. **Tension** — clip 1 must end unresolved so the viewer *needs* clip 2;
   `tension_score` ≥ 7 required, else flag for regeneration.
5. **Drift guard** — after every 5 generations for an avatar, deliberately shift
   register to avoid voice sameness.
6. **Duo hook** — imply an off-screen partner or bake "send this to your [specific
   person]" into clip 2.
7. **Series arc** — a 5-post narrative: establish pain → escalate → turning point →
   discovery → resolution. Advance one step per fresh generation.
8. **Hook A/B** — generate 3 clip-1 openers: emotion-led, curiosity-led,
   text-on-screen. Swappable without regenerating the body.
9. **Platform reformat** — adapt visual/on-screen/gesture (not the story) to another
   platform.
10. **Reaction / silent mode** — no dialogue; story told via on-screen text and gesture
    only.

### Platform natives

- **TikTok** — deadpan face-to-cam, trending audio, exaggerated micro-expressions,
  quick cuts.
- **Instagram Reels** — POV text overlays, polished, stomp-to-reveal transitions.
- **YouTube Shorts** — curiosity-hook opener, educational delayed reveal.
- **Facebook Reels** — warmer, more personal, slightly longer emotional setup.

---

## 4. Image generation (avatar portraits & reference grids)

**Tool:** a Gemini-based image model (e.g. Nano Banana Pro) works well here.

### Photographic language beats "hyperrealistic"

The uncanny plastic/CGI look comes from quality-adjective stacking. Fixes, applied as
rules:

- **Blocklist** these plastic-rendering words entirely: `hyperrealistic`, `8k`,
  `ultra-detailed`, and similar over-sharpening / perfection cues.
- **Anchor on real photography** instead: name a camera body, a lens, an aperture,
  film grain, and *visible imperfections* (skin texture, asymmetry, uneven light).
- **Avoid perfect symmetry and flat, even lighting** — both read as synthetic.
- Express aspect ratio in natural language, not as flags — Midjourney-style `--ar`
  flags are silently ignored by some models and pollute the prompt.

### 2×2 reference grid is the consistency method

Generate a **2×2 character grid** (1:1 aspect ratio) to get four consistent angles of
the same face in a single credit-efficient generation. Prefer this over separate
single-angle generations, which drift in identity. Always price the generation
(a `get_cost`-style check) before committing.

---

## 5. Video generation (clips, voice, continuity)

**Tools:** Seedance 2.0 (via a platform like Higgsfield) as primary; Kling 3.0; Wan
2.7 for lip-sync.

### Separate voice from video — always

Embedding dialogue inline in the video model triggers per-generation TTS: no voice
consistency, no prosody control, robotic output. Correct architecture:

1. Clone the avatar's voice **once** (a dedicated voice tool).
2. Generate the finished audio take.
3. Pass that audio into the video model as `@Audio1` for lip-sync — do not let the
   video model synthesize speech.

### Continuity across clips

- **End-frame chaining** — screenshot the last frame of a clip and upload it as the
  start image of the next generation to hold face continuity across a multi-clip
  sequence.
- **Single continuous prompt, never shot labels** — labeling parts "Shot 1 / Shot 2"
  makes the model treat each as an independent generation and breaks the face. Use one
  continuous prompt structured with `SCENE:` and `MOTION:` blocks.

### Anti-static vs. lip-sync is a real conflict

Head-movement / anti-static instructions fight lip-sync during dialogue. Resolve it by
**locking head movement during dialogue clips** and reserving motion instructions for
silent / B-roll clips only. Surface this tension proactively when both are requested.

---

## 6. Tooling & platform reference

### Generation MCP patterns

If your generation platform exposes an MCP server (e.g. Higgsfield), common patterns:

- An import-by-URL call to turn a CDN output into a reusable media ID for chaining.
- A job-display call to retrieve a generation's CDN URL.
- A cost check before committing any paid generation.
- Note that server-side CDN downloads are often blocked — download via browser instead.

### Script engine implementation

A common setup is a React artifact that calls a chat-completion endpoint to produce the
JSON script contract above. When run inside a host that provides a built-in proxy, no
API key is needed in that environment. Keep the generation and reformat prompts
versioned.

### Hosted UI routes

If the engine has a hosted UI, routes are rarely guessable — enumerate the real ones
with `document.querySelectorAll('a[href]')` rather than guessing paths.

### Browser automation

On a heavy, animated staging UI, `get_page_text` and `javascript_tool` tend to be more
reliable than screenshot-based validation. Avoid navigate + screenshot batch combos —
animated canvas rendering can cause timeouts.

---

## 7. Known gotchas

Check these before assuming a clean run:

- **Gateway timeouts on generation:** long synchronous generation requests (~40s+) can
  exceed a gateway timeout. Use an async job model for generation endpoints.
- **Stale trend data:** trend/ranking data can go empty or stale until a fresh ingest
  is triggered.
- **Persona-name drift:** watch for the same persona appearing under slightly different
  names across surfaces; keep names canonical.
- **Persona sprawl:** near-duplicate personas accumulate over time — consolidate.

---

## 8. Operating principles (how to work here)

- Give a brief heads-up on approach, then execute with full momentum — minimal
  mid-task check-ins.
- Think in reusable blocks: named templates, scored banks, unit economics
  (track cost-per-clip). Prefer systematized prompt engineering over ad hoc craft.
- Surface conflicts within the system proactively (anti-static vs. lip-sync is the
  model here) — they are welcome.
- Prefer emotionally triggering, scroll-stopping mechanics over safe, information-heavy
  content.
- Scale the roster gradually across verticals rather than all at once.
