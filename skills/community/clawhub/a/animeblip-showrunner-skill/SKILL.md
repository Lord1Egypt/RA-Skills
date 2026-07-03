---
name: animeblip-showrunner-skill
description: >-
  Animeblip Showrunner — create complete AI story videos at scale (screenplay → consistent characters → scene images → scene videos → final cut) in 900+ art styles, as short videos, films, or episodic series. Drives Animeblip's production agent end-to-end, acting as the producer/reviewer it lacks. Use when the user wants AI video generation, a multi-scene story video, a vertical anime micro-drama, an ad/promo, a storyboard, or to auto-produce an episodic series — to create, produce, or review an Animeblip video, episode, or series autonomously. Triggers animeblip, showrunner, AI video generation, text-to-video, story video, micro-drama, storyboard, episodic anime, "produce an episode", "auto-produce a series".
user-invocable: true
metadata:
  {
    "openclaw": {
      "emoji": "🎬",
      "requires": { "bins": ["python3"], "env": ["ANIMEBLIP_API_KEY"] },
      "primaryEnv": "ANIMEBLIP_API_KEY"
    }
  }
---

# Animeblip Showrunner

Animeblip's backend production agent owns the full pipeline (**screenplay → characters →
elements → scene images → scene videos → BGM → final cut**) but has **no built-in
reviewer**. Your job is to be that reviewer/producer: send the brief, **poll**
`query_session` on a cadence, critique the screenplay, and fix failures with **targeted
single-scene** edits (never full regen) — keeping a lid on spend. (See **Pipeline &
workflow modes** below — the elements step and whether scene images are even needed
depend on the story's `videoWorkflow`.)

You manage and review by polling and sending messages — there is no managed loop; YOU
(the agent) drive. The Animeblip agent does the creative generation.

## Setup

```bash
export ANIMEBLIP_API_KEY="ab_…"                       # your Animeblip API key — create one at studio.animeblip.com → API Keys
export ANIMEBLIP_BASE_URL="https://studio.animeblip.com"   # optional — defaults to prod
```

Python stdlib only. Call the per-op script directly, e.g. `python3 {baseDir}/scripts/create_project.py`,
`scripts/send_message.py`, `scripts/query_session.py`. `--dry-run` works on any command (nothing
that spends credits runs). Deep-dive docs live in `{baseDir}/docs/` (triage-rules,
cost-model-and-caps); this file stays the canonical command reference.

## Cost model (read first)

`generate_motion` (scene video) is the **expensive** op. NEVER full-regen — every fix
names the single failing scene so the agent uses `withReference` targets. Keep spend
bounded: as a rule of thumb stop after ~**2 retries per shot** / ~**6 fix-sends per
episode** and surface to the human rather than burning credits in a retry spiral.
(See docs/cost-model-and-caps.md.)

## Commands

| Command | Purpose |
|---|---|
| `create_project.py --title T --idea … --aspect 9:16` | New **project (series)** + its **episode 1 (story)** → storyId. (Story = episode, Series = project.) **Art style is fixed to the Anime6 preset** — do NOT pass a style; to change it, the user updates it on the website (the storyboard editor). |
| `send_message.py --story S --message "…"` | Send a message **verbatim** (nothing appended). Scope is up to you: a full end-to-end brief, or a single step like "Write the screenplay only, then stop." |
| `query_session.py --story S [--after-seq N]` | One status read: state / progress / `finalVideoUrl` / structured `failures[]` ({op, scene, error}) / new chat `messages[]` since the cursor + the next `cursor`. Pass `--after-seq` (0 first time, then the returned cursor) to read the agent's new questions/replies — so a pause-to-ask isn't mistaken for idle. This is your **poll channel**. |
| `get_project_state.py --story S` | Project-state read — the **review channel** (the SAME state the agent sees). Top-level: `videoWorkflow` + `artStyleName` + `aspectRatio`. `scenes[]` { order, visualDescription, characterKeys, elementKeys, durationSec, startSec, hasImage, hasMotion, imageUrl, videoUrl }. `characters[]` { key, name, description, appearance, status, hasUploadedRefs, imageUrl }. `elements[]` { key, name, type (location/prop), description, status, imageUrl }. `episodes[]` (series manifest). **`hasImage`/`hasMotion` are true ONLY for a READY asset** — a failed/blocked generation still leaves a record, so confirm success with `imageUrl != null` / `videoUrl != null`, and if a scene has no `videoUrl` check `query_session` `failures[]` for why (e.g. copyright). Use `description`/`appearance`/`status` to critique the actual designs; `videoWorkflow` decides which steps are needed (see **Pipeline & workflow modes**). |
| `create_episode.py --from S` | Next episode in the SAME series (reuses characters) |
| `list_projects.py [--limit N] [--cursor C]` | List projects (**series**) on the account, each with its full `episodes[]` ({order, storyId}) + `nextCursor` — use it to find a story to resume, or the latest episode's storyId to chain the next from. |

## Pipeline & workflow modes (know this before you plan steps)

The backend pipeline is:

**Screenplay → Characters → Elements → Scene Images → Scene Videos → BGM → Final Video**

- **Screenplay** creates the scenes AND the character *data* (names/descriptions) and each scene's `elementKeys` — but it does **not** create element data or any images.
- **Characters** = generate the character images (data already exists from the screenplay).
- **Elements** = the location/prop reference images (create the element data, then generate its image). This is a **real, required step** for a complete video even if the user never named locations/props — don't skip it. Locations render 16:9, props 1:1.
- **Scene Images** — REQUIRED or OPTIONAL depending on `videoWorkflow` (see below).
- **Scene Videos** then **BGM** (background music, optional) then **Final Video**.
- **Audio/narration is baked into the video** — there is no separate audio step. Don't ask for one.

**`videoWorkflow` (read it from `get_project_state`) decides whether scene images are needed:**

- **`reference`** → scene videos run off the character + element reference images, so **scene images are OPTIONAL**. Do NOT generate scene images as a prerequisite; only make a still if the user explicitly asks for one.
- **`start-frame`** → each scene's image **is the single first frame** of its video → **generate the scene image before its video**.
- **`storyboard-grid`** → each scene's image is a **2×2 multi-panel composite** that becomes the opening frame → **generate the scene image before its video**.
- For **both image-based modes**, always make sure a scene has an image before asking for its video (or it silently falls back to reference-to-video and loses the chosen look).

## Flow — instruction-driven (there is no mode flag)

Whether you run the whole pipeline in one shot or drive it step-by-step is decided by
**what message you send**, driven by the user's request. `query_session.py` is your
poll channel — it also returns the agent's new `messages[]` (so you can answer a question
it pauses to ask) and recovers `failures[]` even after the run clears; `get_project_state.py`
is your review read — scenes **and** the series characters[]/elements[] with their design images.

**DEFAULT — end-to-end (one shot).** The "just make the video" case. Send the full brief
*with* an end-to-end instruction, then poll to delivery:

```
1. create_project.py  → storyId                         (ep1; ep2+ use `create_episode.py --from <prevStory>`)
2. send_message.py --story S --message "<full brief>. Produce the complete final video
   end-to-end — do not stop for input."
3. query_session.py --story S   (poll ~every 60s)     → until the final video URL appears
```

While polling: if `failures[]` is non-empty, triage and send ONE targeted fix; if the agent
left new `messages[]` (a question), answer it via `send_message.py`; otherwise keep polling.

**PER-STEP — you self-review between steps.** When the user wants you to review as you go
(or the brief is risky/expensive). You scope each step and inspect before paying for the next:

```
1. send_message.py --story S --message "Write the screenplay only, then stop."
2. query_session.py --story S       (poll until idle)
3. get_project_state.py --story S   → read each scene (visualDescription / characterKeys /
                                      imageUrl) AND the characters[]/elements[]
                                      ({ key, name, imageUrl }); critique scenes and designs
4. send_message.py --story S --message "<edits, or: looks good — now generate the character images, then stop>"
5. repeat step 2–4 through: characters → elements → scene images (ONLY if `videoWorkflow`
                                      is image-based; skip for `reference`) → scene videos → BGM → final cut
```

**MANUAL review — pause for a human.** Same per-step loop, but after each step SURFACE the
`get_project_state.py` snapshot to the human and STOP until they say continue, before sending
the next scoped step.

## Triage rules (apply these whenever you handle a failure)

These are guidance you apply with judgment, not rigid rules:

- `batch_failed` + content/policy/copyright/moderation wording → **REWORD** that shot's prompt
  (don't just retry it unchanged). Reword to clear the flag **without changing the characters,
  their emotions, or the storyline** — keep the beat, change only the phrasing. Examples of how
  to reword (pick what fits; not a fixed recipe): soften/replace the flagged words, make it less
  explicit, or re-send that one shot's prompt **translated into Chinese** (the content checker
  behaves differently on Chinese prompts and often passes one the English version fails).
- `batch_failed` otherwise → **RETRY** just the affected scene(s).
- `agent_processing` / `batch_running` → keep polling (every ~60s, no faster).
- final video URL present → deliver it (and, if the user wants a human sign-off before publish
  or the next episode, surface it and STOP until they approve).
- **Keep spend bounded:** stop after ~2 retries per shot / ~6 fix-sends per episode and surface
  to the human rather than burning credits in a retry spiral.

## Scheduling (unattended)

Host as a Claude Code scheduled routine (cron). Each wake does ONE poll-and-act step; a
`409 busy` just means a run is still in progress, so exit and let the next tick resume. If
the user wants a human sign-off, a wake that finds an unapproved final video does nothing
but notify.

## Rules

- The Animeblip agent has NO web search — research facts yourself before writing the brief.
- One run per story at a time (`409` = busy → wait, retry).
- NEVER bypass the spend guidance to "just finish it"; if the user asked for a human sign-off, don't skip it.
- Do not full-regen to fix one shot — name the scene.
