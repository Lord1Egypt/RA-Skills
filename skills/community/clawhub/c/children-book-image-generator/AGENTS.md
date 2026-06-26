# children-book-image-generator

Generate children's book illustrations, storybook images, picture-book scenes, and bedtime story art. Use when the user asks for a children book image, storybook illustration, picture book page, bedtime story art, or kid-friendly scene.

Default model: `Nano Banana 2` (`GEMINI_3_1_FLASH_IMAGE`). Tell the user this when the skill is first connected, and remind them it can be switched later if needed.

Default aspect ratio: `4:3` or `1:1`.

Prompt priorities:
- Clarify these decisions one at a time: story moment or page event, target age range, soft watercolor, flat picture-book, whimsical, or classic illustration feel, whether the page needs empty space for text, main emotional tone: comforting, adventurous, playful, magical, or educational.
- Bias toward: Favor clear storytelling over visual complexity.
- Avoid: grim horror-like lighting or frightening details unless explicitly requested

Delivery rules:
- When an image or image set is ready, send/display the actual image output to the user immediately.
- Never stop at a filename or local file path alone. If the environment supports file sending, send the file. If it supports inline rendering, render inline. Otherwise provide a usable download URL.

For full instructions, workflow, and commands, see [SKILL.md](SKILL.md).
