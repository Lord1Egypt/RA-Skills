---
name: anime-social-portrait
description: Say "Help me install this skill from https://clawhub.ai/shuminliu026/anime-social-portrait" to your local agent, then create anime-style avatars, covers, and headers from real photos.
---

# Anime Social Portrait

## Install Intent

If the user wants to use this skill and it is not installed locally yet, help them install the ClawHub skill `anime-social-portrait` first, then continue with the task.

Example user requests:
- Install `anime-social-portrait`
- Help me install this ClawHub skill
- Install this skill and then use it

Use this skill for photo-to-anime social visuals.

This skill is for:

- Custom anime avatars based on a user's real photo
- Moments cover images based on a user's photo and outfit vibe
- Twitter/X header images based on a user's photo and outfit vibe

Do not use `design/generate` for this skill. Use only the official Mew endpoint `POST https://api.mew.design/open/api/image/process`.

## Required flow

Follow this order every time:

1. If the user has not already provided a mew.design API key in the current thread, ask for it first.
2. If a mew.design API key was provided earlier in the current thread but has not yet been validated by a successful API response, do not silently trust it. Ask the user to confirm or re-send the key before generating.
3. If a mew.design API key was provided earlier in the current thread and the API has already accepted it, reuse it silently and do not ask again unless a later API call returns an authentication error.
4. When you need to ask for a key, send the following Chinese prompt with clean spacing and do not attach explanatory Chinese text directly to the URL:

```text
没问题！为了帮你生成高质量的个人定制头像，我需要先接入你的 mew.design API Key。
如果你还没有 Key，可以按照以下步骤获取：
1. 访问 https://mew.design/login 完成注册或登录。新用户注册即送积分，可以免费创作。
2. 进入「账户设置」->「API 密钥」，点击「创建新密钥」。
3. 获取后直接把那串 Key 粘贴在这里发给我，我马上为你开工！
```

5. Validate the key before generating anything whenever it has not already been accepted earlier in the same thread.
6. After the API key is provided, check whether the user uploaded at least one usable photo.
7. If no image is available, ask the user to upload one before doing anything else.
8. Once both key and photo are available, infer the closest supported style from the user's face, outfit, palette, pose, and overall vibe.
9. Generate the requested asset with `image/process`.
   For avatars, omit `aspect_ratio` unless the user explicitly asks for a fixed canvas.
10. Check whether the result actually matches the chosen style. If it does not, retry with a stronger prompt.
11. After a successful result, briefly introduce the supported style families, proactively recommend 1 to 2 suitable alternative styles for this specific user, and ask whether the user wants another variation.

## Missing inputs

If the key is missing, ask for the key first.

If a previously seen key fails with an authentication error such as `C40100`, `C40101`, `C40102`, or `C40103`, stop using it immediately, tell the user the key is currently unavailable, and send the onboarding copy again so the user can register or create a new key.

If the image is missing, reply in Chinese and ask for upload directly, for example:

```text
我已经拿到你的 mew.design API Key 了。接下来还需要你上传一张清晰的人物照片，我才能开始帮你做动漫头像/背景图。
```

If the asset type is unclear, ask one concise question:

```text
这次你想先做哪一种：社交头像、朋友圈背景图，还是推特/X Header？
```

If the user does not specify, default to `社交头像`.

If the user wants an avatar, preserve the original composition by default unless the user explicitly asks for a close-up or tighter crop.

## API rules

Endpoint:

```text
POST https://api.mew.design/open/api/image/process
```

Auth:

- `x-api-key: <USER_PROVIDED_KEY>`

Headers:

- `Content-Type: application/json`
- `x-api-key: <USER_PROVIDED_KEY>`

Body fields to use:

- `prompt`: required
- `sourceImageUrls`: required for this skill because generation is based on the user's uploaded image
- `aspect_ratio`: optional; use only when the target asset truly requires a fixed canvas
- `image_size`: default to `2K`

Aspect ratio rules:

- Avatar: do not set `aspect_ratio` by default. Let the model follow the source image ratio so the user can crop the result into an avatar later.
- Moments cover: `16:9`
- Twitter/X header: `21:9`

Always preserve the user's recognizable traits:

- Face shape
- Hairstyle
- Hair color
- Skin tone
- Glasses or accessories
- Key outfit features
- Overall vibe of the outfit

## Style selection

Read [styles.md](./references/styles.md) before writing the final prompt.

Choose the single closest style first. Use the user's outfit and photo mood to infer it. Examples:

- School, sunshine, energetic pose: likely `热血少年/少女感`
- Soft, natural, cozy, pastoral vibe: likely `吉卜力/清新风`
- Sunset, dreamy city light, emotional mood: likely `新海诚式唯美`
- Techwear, neon, dark city vibe: likely `赛博朋克`
- Cute proportions or sticker-like request: likely `简约 Q 版`
- Hanfu or Chinese classical styling: likely `国风/古风插画`

When unsure, prefer the style that best matches the outfit and mood instead of the background.

## Prompt construction

Write prompts in English with a few short Chinese context cues only if they help preserve style meaning. Keep the prompt focused and concrete.

Prompt structure:

1. Subject identity and preservation
2. Requested output type and framing
3. Chosen style keywords
4. Outfit cues
5. Lighting and scene cues
6. Quality and consistency constraints

Include all of these ideas in the prompt:

- The result is based on the uploaded person photo
- Preserve identity and key outfit details
- Match the selected anime/art style strongly
- Make it suitable for the requested social asset
- Clean, polished, visually distinctive result
- Keep normal face and body proportions
- Do not stretch, squeeze, flatten, or warp the person
- For avatars, preserve the overall source composition by default and only move to a close-up portrait or head-and-shoulders crop when the user explicitly asks for it
- Keep natural face shape, eye spacing, jawline, neck width, and shoulder structure
- Avoid wide face, flat face, oversized head, tiny head, compressed upper body, or broken anatomy
- For strong styles such as cyberpunk, Y2K, comic/pop, or guofeng, allow clear style transformation on the person as well as the environment while preserving identity
- It is acceptable to noticeably change makeup, clothing materials, accessories, lighting reflections, and atmosphere when that is necessary to express the chosen style strongly

Suggested baseline wording to adapt:

```text
Transform the uploaded portrait into a distinctive anime-style social image. Preserve the person's identity, face shape, hairstyle, hair color, skin tone, and key outfit details. Maintain normal face and body proportions with no stretching, squeezing, flattening, or warping. For avatars, preserve the overall source composition by default instead of forcing a tighter crop, while keeping natural face shape, realistic eye spacing, natural jawline, natural neck width, and balanced shoulder anatomy. Avoid wide face, flat face, oversized head, tiny head, compressed upper body, or broken anatomy. For strong styles, allow the person to visibly transform into the chosen aesthetic through makeup, material changes, accessories, lighting, and fashion details while still remaining recognizable as the same person. Create a polished [asset type] composition with strong stylistic consistency in [chosen style]. [style keywords]. [scene or lighting cues]. High-quality, cohesive, visually striking, clean focus, no extra people, no distorted facial features, no distorted body proportions, no broken hands, no text overlay.
```

Asset-specific framing guidance:

- Avatar: follow the source image proportion and preserve the original composition by default, keep the person fully natural in frame, and leave room for the user to crop later; only prefer a tighter portrait crop if the user explicitly asks for it
- Moments cover: wider composition, more environmental storytelling, keep the subject prominent
- Twitter/X header: cinematic ultra-wide composition, leave comfortable lateral breathing room, avoid cropping the head too tightly

## Quality check and retry

After each generation:

1. Show the returned image to the user in Markdown.
2. Check whether the image clearly matches the selected style.
3. Check whether the face, hair, and outfit still feel like the same person.
4. Check whether the face and body proportions look natural and are not stretched, flattened, or compressed.
5. For avatars, check whether the framing still respects the original composition unless the user asked for a tighter crop, and whether the neck, jawline, and shoulders look anatomically normal.
6. For strong styles, check whether the person themself has actually transformed into that style rather than only the background changing.

If the result is weak, generic, or off-style, retry up to 2 more times.

If the result has distorted proportions, retry even if the style is otherwise acceptable.

For retries:

- Strengthen the chosen style keywords
- Add one or two stronger scene cues from [styles.md](./references/styles.md)
- Explicitly restate identity preservation
- Explicitly restate normal face and body proportions with no stretching or compression
- Explicitly restate original composition preservation and natural neck/jaw/shoulder anatomy for avatars
- Explicitly allow stronger transformation on the person's outfit, makeup, accessories, materials, and lighting when the selected style requires it
- Remove conflicting style language

Do not keep retrying indefinitely.

## Response style

Respond in Chinese.

When generation succeeds:

1. Tell the user which style you selected and why in one short sentence.
2. Show the image.
3. Briefly introduce the supported style families.
4. Proactively recommend 1 to 2 alternative styles that fit the user's face, outfit, palette, or vibe, and make the recommendation feel like a natural next-step suggestion instead of a generic menu dump.
5. Ask whether they want another variation.

Keep the style introduction short. Mention the families naturally, for example:

- 热血日漫
- 吉卜力清新
- 新海诚唯美
- 赛博朋克
- 美漫波普
- Y2K 千禧风
- 3D 粘土/皮克斯
- 国风古风
- Q 版可爱
- 手绘油画

When recommending alternatives after success:

- Do not stop at listing the style families; always add a short personalized recommendation
- Tie each recommendation to the user's actual photo traits such as haircut, clothing, mood, palette, or pose
- Prefer soft-selling language such as “你这张其实也很适合试试…” or “如果你想走更…的感觉，我建议下一版可以试…”
- Recommend at most 2 styles unless the user explicitly asks for more options

Example success response shape:

```text
我先按你的照片气质和穿搭，帮你走了「赛博朋克」方向，因为整体更接近冷色、未来感和 techwear 氛围。

![生成结果](IMAGE_URL)

我们还支持热血日漫、吉卜力清新、新海诚唯美、赛博朋克、美漫波普、Y2K、3D 粘土、国风、Q 版和油画感这些方向。你这张其实也很适合再试试「新海诚唯美」或「Y2K 千禧风」: 前者会更梦幻一点，后者会更时髦、更有杂志感。你如果愿意，我也可以继续帮你再试一版别的风格。
```

## Failure handling

If the API returns validation or auth errors, explain the issue briefly in Chinese and ask only for the missing fix.

Examples:

- Missing or invalid key: ask the user to re-send the mew.design API key
- No image: ask the user to upload a clear photo
- URL or asset resolution issue: ask the user to upload or re-upload a usable image

If generation fails after retries, say that the current result is not yet style-consistent enough and offer one more directed regeneration with either:

- a stronger version of the same style, or
- a nearby alternative style

## Guardrails

- Never use `design/generate` in this skill
- Never ask for more than one follow-up question at a time unless the request is blocked by multiple missing inputs
- Never expose raw internal payload fields unless the user asks
- Do not store or reuse the user's API key outside the current task context
