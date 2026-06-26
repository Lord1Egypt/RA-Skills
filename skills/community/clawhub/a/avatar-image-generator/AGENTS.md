# avatar-image-generator

Generate avatars, profile pictures, PFPs, social media headshots, gaming avatars, and portrait icons. Use when the user asks for an avatar, profile picture, pfp, portrait icon, or personal brand headshot.

Default model: `Nano Banana 2` (`GEMINI_3_1_FLASH_IMAGE`). Tell the user this when the skill is first connected, and remind them it can be switched later if needed.

Default aspect ratio: `1:1`.

Prompt priorities:
- Clarify these decisions one at a time: who or what the avatar represents, realistic, illustrated, anime, or stylized look, mood or personality: friendly, confident, mysterious, playful, etc., background preference: plain color, gradient, glow, or environmental hint, crop preference: face only, bust portrait, or shoulder-up.
- Bias toward: Optimize for instant recognition at thumbnail size.
- Avoid: busy environments behind the face

Delivery rules:
- When an image or image set is ready, send/display the actual image output to the user immediately.
- Never stop at a filename or local file path alone. If the environment supports file sending, send the file. If it supports inline rendering, render inline. Otherwise provide a usable download URL.

For full instructions, workflow, and commands, see [SKILL.md](SKILL.md).
