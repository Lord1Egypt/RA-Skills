---
name: character-image-generator
description: Generate character design images, original character art, OC portraits, character sheets, and hero concept art. Use when the user asks for a character design, OC, character portrait, fantasy character, anime character, or original persona image.
version: 0.5.0
metadata: { "pattern": ["generator", "pipeline"], "openclaw": { "emoji": "🧙", "primaryEnv": "IMAGE_GEN_API_KEY", "requires": { "env": ["IMAGE_GEN_API_KEY"], "anyBins": ["bun", "npx"], "bins": ["node", "npm"] } } }
---

# Character Image Generator (`character-image-generator`)

This skill is optimized for character identity, silhouette clarity, costume logic, and reusable character prompt structure.

This skill keeps the same single-gateway runtime, readiness gate, model-selection flow, and CLI behavior as `image-generation`, but narrows the briefing and prompt construction for **character image generator** work.

## Safety & Scope

- **Network**: This skill calls the WeryAI gateway over HTTPS (`https://api.weryai.com`).
- **Auth**: Uses `IMAGE_GEN_API_KEY`. The key is never printed. It may be persisted **only** when you explicitly run `npm run setup -- --persist-api-key`.
- **Reference images**: Must be public URLs (`https://` recommended). `http://` may work but is insecure. Local file paths and `data:` URLs are rejected.
- **No arbitrary shell**: The generation runtime does not execute arbitrary shell commands.
- **Files written**: Output images and optional local config under `.image-skills/character-image-generator/` (project) and/or `~/.image-skills/character-image-generator/` (home).

## Use Cases

- original character portraits
- fantasy or sci-fi hero concepts
- character sheets and reference images
- mascot or spokesperson characters
- narrative cast exploration

## First Trigger Rules

Before the first generation run in a new project or environment:

1. Run `npm run ensure-ready -- --project . --workflow <workflow>`
2. If runtime dependencies are missing, ask for approval and install them
3. If `IMAGE_GEN_API_KEY` is missing, offer to configure it now
4. If no model is configured yet, initialize **Nano Banana 2** (`GEMINI_3_1_FLASH_IMAGE`) as the default

Do not ask the user to edit config files manually. Treat API keys as secrets and never echo them back.

## Clarify These Decisions

Ask **one question at a time**. Prioritize:

1. character role or archetype
2. age range, gender expression, and body language
3. setting: fantasy, modern, sci-fi, historical, etc.
4. signature outfit, props, and color identity
5. portrait, half-body, full-body, or sheet layout

## Recommended Defaults

- aspect ratio: `3:4` or `4:5`
- recommended style: `anime`, `editorial`, `manga`, or `photoreal`
- composition: one primary character, readable silhouette
- background: simple enough that outfit and pose stay dominant

## Prompt Blueprint

Build the prompt in this order:

1. Identity: role, archetype, age range, personality, faction, or profession.
2. Look: face, hair, body language, posture, expression.
3. Outfit + props: signature materials, colors, weapon/tool, emblem, etc.
4. Presentation: portrait, full body, turnaround, or concept sheet.
5. World feel: fantasy, cyberpunk, school life, mythology, noir, etc.

Use one clean prompt direction at a time instead of mixing many competing ideas.

## Prompt Rules

- Always define silhouette, costume anchors, and one memorable visual hook.
- If the user wants a reusable character, keep accessories and palette consistent across variants.
- Use a sheet-style prompt for reference art; use a scene-style prompt for story art.
- When underspecified, prefer strong archetypes over generic 'cool character' wording.

## Avoid

- too many unrelated props
- multiple equal-priority characters unless the user asks for a duo/group
- unclear costume materials or indistinct silhouette
- overly busy background scenes for reference-style art

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

${BUN_X} {baseDir}/scripts/main.ts --prompt "original fantasy character, young female archivist mage, emerald robe with gold embroidery, floating paper charms, calm intelligent expression, full-body concept art, clean parchment backdrop" --style editorial --image character.png --ar 3:4 -m "$M"

${BUN_X} {baseDir}/scripts/main.ts --prompt "anime character sheet for a cyberpunk courier boy, silver undercut hair, orange visor, black utility jacket, messenger drone companion, front pose with detail callouts feel, highly consistent design" --style anime --image character-sheet.png --ar 4:5 -m "$M"
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
