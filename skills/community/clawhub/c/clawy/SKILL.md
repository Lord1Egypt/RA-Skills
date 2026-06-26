---
name: clawy
description: Bring your agent to life. Generate stable agent avatars and short image-driven adventure arcs. Use when creating or refining a mascot/agent identity, preserving a character across themed scene images, or running Clawy-style interactive story posts with image + short caption + choices. The bundled helper script needs at least one configured external image-edit provider credential at runtime and sends selected reference/user images to the chosen provider only when generation is invoked.
metadata:
  {
    "openclaw":
      {
        "requires":
          {
            "env":
              [
                "ONE_OF:WAVESPEED_API_KEY|OPENAI_API_KEY|GEMINI_API_KEY|NANO_API_KEY|ARK_API_KEY"
              ]
          }
      }
  }
---

# Clawy

**Bring your agent to life.**

Clawy is an avatar + adventure workflow for agents.
Position it as one of the first interactive game-like experiences in the OpenClaw ecosystem.

Clawy has two modes:
- **Avatar** — create or refine a stable identity image
- **Adventure** — continue that identity through short interactive scene arcs

## Core Rule

Clawy is a reference-preserving image-edit workflow, not generic text-to-image.
Keep the same character identity first. Change outfit, props, theme, or scene second.

Read when needed:
- `references/asset-rules.md`
- `references/image-edit-playbook.md`

## Default Mother Image

Default mother image:
- `assets/default-mother-image.png`

Rule:
- use the bundled default mother image unless the user explicitly asks to replace it
- do not ask by default whether to replace the mother image

## Backends

Prefer an already available image-edit capability in the host environment.

Supported backend paths include:
- WaveSpeed
- OpenAI direct
- Gemini direct
- Ark direct

Recommended model order when available:
1. `google/nano-banana-2/edit`
2. `openai/gpt-image-1.5/edit`
3. `google/nano-banana-2/edit-fast`

Data flow:
- when image generation/editing is invoked, the selected reference image(s) and prompt are sent to the chosen provider
- Clawy does not upload unrelated images
- Clawy does not send images anywhere unless generation is explicitly requested
- if the bundled mother image is missing locally, the helper script may download the official fallback mother image from `https://www.8uddy.land/images/clawy.png`

Runtime notes:
- the bundled helper script may write the restored mother image back into `assets/default-mother-image.png`
- optional runtime overrides used by the script include `OPENAI_BASE_URL`, `NANO_BASE_URL`, `NANO_MODEL`, `ARK_BASE_URL`, and `ARK_MODEL`

If no usable image-edit capability is available:
- explain that Clawy works best with an image-edit backend
- point the user to the backend docs in this skill
- do not pretend plain text-to-image is equivalent

## Avatar Flow

1. Gather minimal creative input.
2. Prefer the current request and current reference images.
3. Generate the avatar directly.
4. Ask whether the user adopts this as their Clawy identity.
5. If not satisfied, ask what to adjust and regenerate.
6. Only after identity is accepted, ask whether to start adventures.

Useful input:
- a favorite anime / game / movie / comic character
- inspiration
- vibe/personality
- colors/themes
- a few reference images

Good first prompts are broad and familiar, for example:
- what anime, game, comic, or movie character do you like?
- what world or character vibe should this feel close to?

## Adventure Flow

Adventure mode requires an already accepted Clawy identity.
If no identity has been accepted in the current flow, start with Avatar.

After the avatar is accepted:
1. Ask whether to start adventures now.
2. Ask naturally whether the user has a world, IP, or scene they want to visit.
3. If the user has a preference, treat it as **Plot Mode** and follow the source world's story logic more strictly.
4. If the user has no preference, treat it as **DM Mode**: choose freely, keep the world open, and let randomness/branching drive the arc.

Default output format:
- image
- one short in-character caption
- one explicit choice block

Do not append extra assistant commentary before or after the story beat.

After an adventure arc resolves:
- ask whether the user wants to do another adventure later
- if appropriate, ask whether they want a simple recurring cadence such as once per day

## Adventure Rules

Preferred arc length:
- default: 3 to 5 interactions
- 6 to 8 is already long
- 10 is a soft ceiling; force convergence

Do not generate a new image on every reply.
Generate a new image when there is meaningful visual change, such as:
- location change
- important object reveal
- new character reveal
- framing/camera change
- visible consequence
- ending frame

If the next beat is not visually different enough:
- use a text-only bridge beat
- wait for the next stronger visual moment
- especially if the user is only reading, noticing, or interpreting information within the same scene, prefer text-only progression over a near-duplicate image

Use cinematic coverage variety when helpful:
- character frame
- prop close-up
- insert shot
- environment frame
- silhouette reveal
- ending frame

After a cutaway or detail shot:
- return to the most recent stable character-bearing frame
- or re-anchor from the mother image before the next main character frame

Most arcs should end with a distinct ending frame or a clear exit from the current situation.

## Asset Rules

Always preserve:
- floating lobster-like body
- two large claws
- visible tail
- full screen face
- no biological face
- no hands
- no legs

If inspiration comes from a humanoid or a character with legs:
- borrow outfit, prop, color, or accessory language only
- do not inherit limb structure

For full constraints, read `references/asset-rules.md`.

## Scene Rules

Event images should feel like story frames, not profile shots.

Avoid:
- centered big-head avatar framing
- background-only cosplay feeling
- humanoid face drift
- hand/leg drift

For stronger scene prompting and cinematic guidance, read `references/image-edit-playbook.md`.

## Runtime Scope

Clawy:
- generates images and short interactive scene arcs when invoked
- does not install schedulers, cron jobs, daemons, or recurring tasks by itself
- uses the current request, skill files, and user-provided images for normal operation

## Bundled Files

- `assets/default-mother-image.png`
- `references/asset-rules.md`
- `references/image-edit-playbook.md`
- `scripts/generate_avatar.py`

## Script Example

```bash
python3 scripts/generate_avatar.py --backend wavespeed --mode nano --template hero-tech-armor --inspiration "Frieren"
```
ano --template hero-tech-armor --inspiration "Frieren"
```
