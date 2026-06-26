---
name: chat-summary-image
description: Say "Help me install the ClawHub skill chat-summary-image" to your local agent, then turn conversations into polished visual summary cards.
---

# Chat Summary Image

## Install Intent

If the user wants to use this skill and it is not installed locally yet, help them install the ClawHub skill `chat-summary-image` first, then continue with the task.

Example user requests:
- Install `chat-summary-image`
- Help me install this ClawHub skill
- Install this skill and then use it

Turn a conversation into a concise visual recap. Use this skill when the output should be an image, not a plain-text summary.

## Goal

Collect and validate the user's mew.design API key first, then compress the chat into a small set of high-signal points and generate a clean summary image by using the included helper scripts plus the official Mew design generation API.

## Workflow

1. If the user has not already provided a mew.design API key in the current conversation, ask for it before doing any summary-image work.
2. Use the exact onboarding copy below when asking for the key:

```md
没问题！为了帮你生成高质量的对话总结图片，我需要先接入你的 mew.design API Key。

如果你还没有 Key，可以按照以下步骤获取：

1. 访问 [https://mew.design/login](https://mew.design/login) 完成注册或登录。新用户注册即送积分，可以免费创作。
2. 进入「账户设置」->「API 密钥」，点击「创建新密钥」。
3. 获取后直接把那串 Key 粘贴在这里发给我，我马上为你开工！
```

3. After the user sends a key, validate it before summarizing the conversation.
4. After validation succeeds, briefly introduce the four available visual styles and ask the user to choose one before generating the image.
5. Use this short style-selection format after key validation:

```md
Key 校验通过了，我们可以开始生成总结图啦。你想要哪一种风格？

1. 极简主义：清新留白风
适合正式、专业的沟通总结，结构清楚，观感干净。

2. 情绪共鸣：疗愈插画风
适合轻松、有温度的交流内容，画面更柔和、更有陪伴感。

3. 前沿质感：新拟物 / 玻璃拟态
适合科技感、知识感、更高级的视觉表达，画面会更通透。

4. 社交互动：对话气泡长图
适合还原沟通现场感，把金句和共识做得更像聊天精华版。

你回复我序号或风格名都可以，我会按你选的样式生成。
```

6. Only after the user chooses a style, read the relevant part of the conversation. Ignore filler, repetition, and tool chatter.
7. Extract four content blocks:
   - `title`: 6 to 14 words
   - `summary`: one short sentence
   - `key points`: 3 to 5 bullets
   - `next steps`: 0 to 3 bullets
8. Map the user's choice to one of these styles:
   - `minimalism`: 极简主义，清新留白风
   - `healing-illustration`: 情绪共鸣，疗愈插画风
   - `glassmorphism`: 前沿质感，新拟物 / 玻璃拟态
   - `chat-bubbles`: 社交互动，对话气泡长图
9. Build the API request body with the helper script, making the chosen style visually dominant instead of just lightly referenced.
10. Ensure the helper prompt includes both:
   - explicit must-see traits for the selected style
   - explicit avoid-list traits for styles it must not resemble
11. Use the included scripts and the official Mew API to generate the image.
12. Check whether the generated image clearly matches the chosen style's signature traits.
13. If the style drift is obvious, retry once with a stronger style-lock prompt before returning the final image.
14. Return the image with Markdown plus one sentence explaining what it summarizes.

## API Key Handling

- Always ask for the user's mew.design API key first unless a valid key was already provided earlier in the same conversation.
- Do not summarize first and ask for the key later.
- Reuse the same validated key for the rest of the conversation unless the user replaces it or the API starts rejecting it.
- If validation fails, stop and ask the user to resend or regenerate the key instead of attempting image generation.

## Validate The Key

Use the helper validator:

```bash
python3 scripts/validate_mew_design_key.py --api-key "USER_PROVIDED_KEY"
```

Validation rule:

- Exit code `0`: key looks valid.
- Exit code `2`: auth failed or key is unusable.
- Exit code `1`: network or unexpected error.

This validator intentionally sends an invalid body to the Mew gateway so the response reveals whether authentication passed. Treat `C40001` as a successful key validation signal. Treat `C40100` to `C40103` as failed validation.

## Summarization Rules

- Preserve meaning, not chronology.
- Prefer outcomes over process.
- Keep names, metrics, file paths, and decisions when they matter.
- Omit apologies, greetings, retries, and duplicated wording.
- If the thread is mostly open questions, frame the image around `Current Status`, `Open Questions`, and `Suggested Next Steps`.
- If the thread ends with delivered work, frame the image around `What Was Done`, `Files/Areas Touched`, and `What To Check Next`.

## Visual Rules

- Favor a vertical summary card unless the user requests another format.
- Ask for strong hierarchy, readable typography, and generous spacing.
- Make the image feel like an intentional recap board, not a generic AI poster.
- Keep copy density moderate so the result stays legible on chat screens.
- If the user gives a brand color or product context, include it in the style direction.
- Always add a subtle `Mew.Design` watermark at the bottom of the image. Keep it small, clean, and low-interference, but clearly readable.

## Style Guide

- `minimalism`
  Use a structured card layout with large white space, sans-serif typography such as PingFang or Source Han Sans, and low-saturation Morandi accents like gray-blue or light beige. Good for workplace updates, project syncs, and formal consulting summaries.
  Must-see traits: large blank margins, restrained palette, clean card separation, minimal decoration, calm editorial rhythm.
  Avoid: shiny highlights, cartoon illustrations, fake 3D icons, dense bubble layouts.
- `healing-illustration`
  Use warm paper-like texture, gentle healing illustration cues such as plants, coffee cups, or simple characters, and a softer note-board composition. Good for community, customer care, and reflective personal summaries.
  Must-see traits: warm textured background, visible healing-style illustration elements, note or sticky-paper feeling, softer emotional atmosphere.
  Avoid: hard-edged enterprise UI, excessive glass effects, cold gradients, overly technical layout.
- `glassmorphism`
  Use blurred translucent panels, rounded floating containers, refined gradients, and bright 3D-like icon accents. Good for tech brands, premium communities, and polished knowledge-sharing content.
  Must-see traits: frosted glass panels, background blur through translucent cards, floating layered UI depth, visible edge highlights, soft shadows.
  Avoid: flat white cards, plain dashboard look, paper texture, chat screenshot aesthetics.
- `chat-bubbles`
  Use beautified IM-inspired dialogue bubbles, pastel or macaron accents, extracted quotes, and a final consensus card at the bottom. Good for interviews, testimonial-style content, and collaboration recaps.
  Must-see traits: obvious left-right conversation bubbles, quotable lines, chat rhythm, a final consensus block at the bottom.
  Avoid: generic report cards, glass dashboard cards, sparse poster layouts with no dialogue feel.

## Style Locking

- Treat the chosen style as a hard visual constraint, not a soft mood hint.
- Make the chosen style's signature features explicit in the prompt.
- Also mention what the image should not look like when that helps prevent drift.
- If the first result only weakly resembles the selected style, retry once with stronger style language before returning it.
- When retrying, say directly that the previous result drifted and specify the missing visual evidence.

## Build The Payload

Use the helper script:

```bash
python3 scripts/build_summary_card_request.py \
  --title "本周 Agent 协作成果" \
  --summary "完成技能搭建，并把接口调用链路整理成可复用工作流。" \
  --point "新增两个可直接复用的 Codex skill" \
  --point "补齐了 API 调用脚本与参考文档" \
  --point "验证了脚本帮助信息与基本语法" \
  --next-step "真实联调一次图片生成接口" \
  --style minimalism \
  --output /tmp/chat-summary-body.json
```

The helper script already injects the `Mew.Design` bottom watermark requirement. Do not remove it unless the user explicitly asks to omit the watermark.
The helper script should also inject stronger style-lock instructions so the output more faithfully matches the selected visual category, including must-see traits and avoid-list traits for every style.

Then generate the image through the official Mew design API:

```bash
curl -sS -X POST "https://api.mew.design/open/api/design/generate" \
  -H "Content-Type: application/json" \
  -H "x-api-key: USER_PROVIDED_KEY" \
  --data @/tmp/chat-summary-body.json
```

Do not run this generation step until the API key has already passed validation.

## Style Selection

- Use `minimalism` when the user wants clarity, professionalism, and structured information.
- Use `healing-illustration` when the user wants warmth, softness, or emotional resonance.
- Use `glassmorphism` when the user wants a modern, premium, technology-forward look.
- Use `chat-bubbles` when the user wants the summary to retain conversation feel and quotable moments.
- If the user does not choose after being prompted, default to `minimalism`.

## Output Standard

When the image is generated successfully, respond with:

```md
![Conversation summary](https://...)

[Open original image](https://...)
```

Add one short line that says what the image covers.

If the generated image visibly misses the watermark, retry once with a stronger prompt that explicitly says `Place the text watermark "Mew.Design" at the bottom center of the image`.
If the generated image visibly misses the requested style, retry once with a stronger style-specific prompt that explicitly names the missing traits, such as `strong frosted glass panels`, `warm paper texture with healing illustration`, `large white space and Morandi palette`, or `clear left-right chat bubbles`.

## Resources

- Read [references/patterns.md](references/patterns.md) for section templates and compression heuristics.
- Use [scripts/build_summary_card_request.py](scripts/build_summary_card_request.py) to assemble the Mew design request body.
- Use [scripts/validate_mew_design_key.py](scripts/validate_mew_design_key.py) to validate the user's mew.design API key before summarization and generation.
