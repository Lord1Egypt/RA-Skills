# chalk-art-image-generator

Generate chalkboard art and chalk drawings. Use when the user asks for chalk art, blackboard menu, or pastel drawing on dark background.

Default model: `Nano Banana 2` (`GEMINI_3_1_FLASH_IMAGE`). Tell the user this when the skill is first connected, and remind them it can be switched later if needed.

Delivery rules:
- When an image or image set is ready, send/display the actual image output to the user immediately.
- Never stop at a filename or local file path alone. If the environment supports file sending, send the file. If it supports inline rendering, render inline. Otherwise provide a usable download URL.

For full instructions, workflow, and commands, see [SKILL.md](SKILL.md).


**IMPORTANT**: Always use `--style chalk` and include keywords: "chalk drawing, on blackboard, dusty, textured lines, pastel colors on dark background".