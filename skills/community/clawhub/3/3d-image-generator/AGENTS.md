# 3d-image-generator

Generate 3D rendered art and icons. Use when the user asks for 3D graphics, claymorphism, octane render, or blender 3d style.

Default model: `Nano Banana 2` (`GEMINI_3_1_FLASH_IMAGE`). Tell the user this when the skill is first connected, and remind them it can be switched later if needed.

Delivery rules:
- When an image or image set is ready, send/display the actual image output to the user immediately.
- Never stop at a filename or local file path alone. If the environment supports file sending, send the file. If it supports inline rendering, render inline. Otherwise provide a usable download URL.

For full instructions, workflow, and commands, see [SKILL.md](SKILL.md).


**IMPORTANT**: Always use `--style 3d-render` and include keywords: "3d render, octane render, unreal engine, claymorphism, soft lighting, ray tracing".