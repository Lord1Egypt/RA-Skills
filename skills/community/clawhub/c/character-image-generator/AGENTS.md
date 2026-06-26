# character-image-generator

Generate character design images, original character art, OC portraits, character sheets, and hero concept art. Use when the user asks for a character design, OC, character portrait, fantasy character, anime character, or original persona image.

Default model: `Nano Banana 2` (`GEMINI_3_1_FLASH_IMAGE`). Tell the user this when the skill is first connected, and remind them it can be switched later if needed.

Default aspect ratio: `3:4` or `4:5`.

Prompt priorities:
- Clarify these decisions one at a time: character role or archetype, age range, gender expression, and body language, setting: fantasy, modern, sci-fi, historical, etc., signature outfit, props, and color identity, portrait, half-body, full-body, or sheet layout.
- Bias toward: Always define silhouette, costume anchors, and one memorable visual hook.
- Avoid: too many unrelated props

Delivery rules:
- When an image or image set is ready, send/display the actual image output to the user immediately.
- Never stop at a filename or local file path alone. If the environment supports file sending, send the file. If it supports inline rendering, render inline. Otherwise provide a usable download URL.

For full instructions, workflow, and commands, see [SKILL.md](SKILL.md).
