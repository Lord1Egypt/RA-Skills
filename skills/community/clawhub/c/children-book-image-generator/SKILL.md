---
name: children-book-image-generator
description: Generate children's book illustrations, storybook images, picture-book scenes, and bedtime story art. Use when the user asks for a children book image, storybook illustration, picture book page, bedtime story art, or kid-friendly scene.
version: 0.5.0
metadata: { "pattern": ["generator", "pipeline"], "openclaw": { "emoji": "📚", "primaryEnv": "IMAGE_GEN_API_KEY", "requires": { "env": ["IMAGE_GEN_API_KEY"], "anyBins": ["bun", "npx"], "bins": ["node", "npm"] } } }
---

# Children Book Image Generator (`children-book-image-generator`)

This skill is tuned for warm storytelling, age-appropriate clarity, gentle composition, and storybook-friendly prompt writing.

This skill keeps the same single-gateway runtime, readiness gate, model-selection flow, and CLI behavior as `image-generation`, but narrows the briefing and prompt construction for **children book image generator** work.

## Safety & Scope

- **Network**: This skill calls the WeryAI gateway over HTTPS (`https://api.weryai.com`).
- **Auth**: Uses `IMAGE_GEN_API_KEY`. The key is never printed. It may be persisted **only** when you explicitly run `npm run setup -- --persist-api-key`.
- **Reference images**: Must be public URLs (`https://` recommended). `http://` may work but is insecure. Local file paths and `data:` URLs are rejected.
- **No arbitrary shell**: The generation runtime does not execute arbitrary shell commands.
- **Files written**: Output images and optional local config under `.image-skills/children-book-image-generator/` (project) and/or `~/.image-skills/children-book-image-generator/` (home).

## Use Cases

- storybook scene illustrations
- picture-book page art
- bedtime story visuals
- educational children illustrations
- kid-friendly animal or family scenes

## First Trigger Rules

Before the first generation run in a new project or environment:

1. Run `npm run ensure-ready -- --project . --workflow <workflow>`
2. If runtime dependencies are missing, ask for approval and install them
3. If `IMAGE_GEN_API_KEY` is missing, offer to configure it now
4. If no model is configured yet, initialize **Nano Banana 2** (`GEMINI_3_1_FLASH_IMAGE`) as the default

Do not ask the user to edit config files manually. Treat API keys as secrets and never echo them back.

## Clarify These Decisions

Ask **one question at a time**. Prioritize:

1. story moment or page event
2. target age range
3. soft watercolor, flat picture-book, whimsical, or classic illustration feel
4. whether the page needs empty space for text
5. main emotional tone: comforting, adventurous, playful, magical, or educational

## Recommended Defaults

- aspect ratio: `4:3` or `1:1`
- recommended style: `watercolor`, `editorial`, or `flat-illustration`
- composition: simple readable storytelling with one main moment
- palette: warm, soft, friendly, and age-appropriate

## Prompt Blueprint

Build the prompt in this order:

1. Story beat: what is happening in this exact page moment.
2. Characters: child, animal, parent, creature, object-with-personality, etc.
3. Environment: bedroom, forest, classroom, magical world, garden, etc.
4. Emotion: cozy, curious, joyful, brave, sleepy, comforting, etc.
5. Book treatment: picture-book layout, gentle palette, text-safe space if needed.

Use one clean prompt direction at a time instead of mixing many competing ideas.

## Prompt Rules

- Favor clear storytelling over visual complexity.
- Use soft emotional language and concrete scene details that children can understand.
- If the illustration is for a page spread, reserve calm space for text when needed.
- Keep expressions readable and the scene emotionally safe unless the user wants tension.

## Avoid

- grim horror-like lighting or frightening details unless explicitly requested
- crowded cinematic action that becomes hard to read
- harsh color contrast that feels aggressive for young readers
- tiny narrative details that distract from the main story beat

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

${BUN_X} {baseDir}/scripts/main.ts --prompt "children book illustration, little fox reading under a glowing tree at dusk, cozy magical forest, gentle warm lights, calm storytelling composition, space at top for page text" --style watercolor --image storybook.png --ar 4:3 -m "$M"

${BUN_X} {baseDir}/scripts/main.ts --prompt "picture book scene, two siblings building a cardboard rocket in their bedroom, joyful playful mood, soft pastel palette, friendly details, clear storytelling for young children" --style editorial --image storybook-room.png --ar 4:3 -m "$M"
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
