# anime-image-generator

Generate high-quality anime style illustrations. Use when the user asks for anime, light novel covers, or japanese animation style art.

Default model: `Nano Banana 2` (`GEMINI_3_1_FLASH_IMAGE`). Tell the user this when the skill is first connected, and remind them it can be switched later if needed.

Delivery rules:
- When an image or image set is ready, send/display the actual image output to the user immediately.
- Never stop at a filename or local file path alone. If the environment supports file sending, send the file. If it supports inline rendering, render inline. Otherwise provide a usable download URL.

For full instructions, workflow, and commands, see [SKILL.md](SKILL.md).


**IMPORTANT**: Always use `--style anime` and include keywords: "anime style, cel shaded, highly detailed, beautiful lighting".