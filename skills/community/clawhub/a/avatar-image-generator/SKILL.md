---
name: avatar-image-generator
description: Generate avatars, profile pictures, PFPs, social media headshots, gaming avatars, and portrait icons. Use when the user asks for an avatar, profile picture, pfp, portrait icon, or personal brand headshot.
version: 0.5.0
metadata: { "pattern": ["generator", "pipeline"], "openclaw": { "emoji": "🙂", "primaryEnv": "IMAGE_GEN_API_KEY", "requires": { "env": ["IMAGE_GEN_API_KEY"], "anyBins": ["bun", "npx"], "bins": ["node", "npm"] } } }
---

# Avatar Image Generator (`avatar-image-generator`)

This skill is optimized for profile-picture style images that still read clearly at small sizes.

This skill keeps the same single-gateway runtime, readiness gate, model-selection flow, and CLI behavior as `image-generation`, but narrows the briefing and prompt construction for **avatar image generator** work.

## Safety & Scope

- **Network**: This skill calls the WeryAI gateway over HTTPS (`https://api.weryai.com`).
- **Auth**: Uses `IMAGE_GEN_API_KEY`. The key is never printed. It may be persisted **only** when you explicitly run `npm run setup -- --persist-api-key`.
- **Reference images**: Must be public URLs (`https://` recommended). `http://` may work but is insecure. Local file paths and `data:` URLs are rejected.
- **No arbitrary shell**: The generation runtime does not execute arbitrary shell commands.
- **Files written**: Output images and optional local config under `.image-skills/avatar-image-generator/` (project) and/or `~/.image-skills/avatar-image-generator/` (home).

## Use Cases

- social profile pictures
- creator or founder avatars
- gaming profile icons
- stylized self-portrait directions
- team member profile images

## First Trigger Rules

Before the first generation run in a new project or environment:

1. Run `npm run ensure-ready -- --project . --workflow <workflow>`
2. If runtime dependencies are missing, ask for approval and install them
3. If `IMAGE_GEN_API_KEY` is missing, offer to configure it now
4. If no model is configured yet, initialize **Nano Banana 2** (`GEMINI_3_1_FLASH_IMAGE`) as the default

Do not ask the user to edit config files manually. Treat API keys as secrets and never echo them back.

## Clarify These Decisions

Ask **one question at a time**. Prioritize:

1. who or what the avatar represents
2. realistic, illustrated, anime, or stylized look
3. mood or personality: friendly, confident, mysterious, playful, etc.
4. background preference: plain color, gradient, glow, or environmental hint
5. crop preference: face only, bust portrait, or shoulder-up

## Recommended Defaults

- aspect ratio: `1:1`
- recommended style: `photoreal`, `editorial`, or `anime` depending on request
- composition: centered face, strong eye contact, clean silhouette
- background: simple and contrast-friendly for small-size display

## Prompt Blueprint

Build the prompt in this order:

1. Identity: person, character, brand mascot, or abstract persona.
2. Look: realistic, illustrated, anime, cartoon, cinematic, etc.
3. Crop: face only, shoulder-up, or bust portrait.
4. Expression + lighting: approachable, intense, premium, dramatic, soft, etc.
5. Background: simple color, gradient, soft blur, glow halo, or minimal context.

Use one clean prompt direction at a time instead of mixing many competing ideas.

## Prompt Rules

- Optimize for instant recognition at thumbnail size.
- Prefer one dominant face or subject; avoid crowded scenes.
- If the user wants a personal-brand avatar, bias toward clean lighting and controlled background.
- If the avatar is fictional, lock hairstyle, outfit cue, and color identity clearly in the prompt.

## Avoid

- busy environments behind the face
- multiple people in one avatar unless explicitly requested
- low-contrast face/background combinations
- tiny accessories that disappear at small size

## Workflow

1. Run the readiness gate and resolve `IMAGE_GEN_API_KEY`
2. Clarify the scenario-specific decisions above
3. Build a single strong prompt from the blueprint
4. Choose a recommended style only if it helps the request
5. Generate the image
6. If the user wants variations, change one major variable at a time and re-generate

## Script

`{baseDir}` is the directory containing this file. `${BUN_X}` is either `bun` or `npx -y bun`.

| Path | Purpose |
| --- | --- |
| `{baseDir}/scripts/main.ts` | the only execution entrypoint |

## Usage Examples

```bash
# examples only; M should be chosen by the user or resolved by the agent
M=<chosen model key>

${BUN_X} {baseDir}/scripts/main.ts --prompt "clean creator avatar for a tech founder, shoulder-up portrait, confident expression, soft studio lighting, dark blue gradient background, highly recognizable at small size" --style editorial --image avatar.png --ar 1:1 -m "$M"

${BUN_X} {baseDir}/scripts/main.ts --prompt "anime gaming avatar, silver hair, red eyes, black cyber jacket, neon rim light, centered face, dark purple glow background, strong icon readability" --style anime --image avatar-anime.png --ar 1:1 -m "$M"
```

## Delivery Rules

- Tell the user what you are generating and which model is being used before you start
- Show the image directly when it is ready; do not reply with only a filename
- If the user asks for revisions, only change the necessary direction instead of restarting everything
- If the request is underspecified, use the clarification order above before writing the final prompt

## References

- [references/config/first-time-setup.md](references/config/first-time-setup.md)
- [references/config/preferences-schema.md](references/config/preferences-schema.md)
- [references/config/model-registry-schema.md](references/config/model-registry-schema.md)
- [references/style-presets.md](references/style-presets.md)
- [references/weryai-platform.md](references/weryai-platform.md)
