---
name: audio-to-wechat-article
description: Turn meeting audio or a transcript plus optional images into a publish-ready WeChat Official Account article. Use when the user wants to go from 录音/文字稿/会议内容/配图/二维码 to 标题、小标题、正文、公众号 markdown 稿，并 optionally push to WeChat draft box. Also use when the user provides audio + screenshots/images and wants a reusable end-to-end workflow rather than one-off writing.
---

# Audio to WeChat Article

Use this skill to convert raw spoken or written material into a structured WeChat article workflow.

Default outcome:
- transcript or cleaned source text
- article brief
- article JSON
- WeChat-ready markdown
- optional image placement plan
- optional QR code CTA block
- optional WeChat draft publishing

## Supported inputs

- audio file (`.m4a`, `.mp3`, `.ogg`, `.wav`, `.mp4`, `.mov`)
- transcript text
- meeting minutes / notes
- optional screenshots or supporting images
- optional QR code image for final article or poster

## V5.1 end-to-end workflow

### Route A: audio → transcript → article → WeChat draft
1. Transcribe audio into text
2. Build article brief from transcript
3. Decide article mode
4. Draft article JSON
5. Add screenshots / QR placement notes
6. Compose WeChat markdown
7. Optionally publish to WeChat draft box

### Route B: text / notes → article → WeChat draft
1. Clean notes into source text
2. Build article brief
3. Draft article JSON
4. Add screenshots / QR placement notes
5. Compose WeChat markdown
6. Optionally publish to WeChat draft box

## Core workflow rules

1. **Normalize the source**
   - If the user provides audio, transcribe it first.
   - If the user provides text, clean it into readable source notes.
   - Do not fabricate unclear sections; mark uncertain parts.

2. **Build an article brief**
   Use the bundled brief script for a deterministic first pass.

3. **Choose article mode**
   - **Insight article**: 观点 / 认知 / 判断
   - **Case article**: 复盘 / how we did it
   - **Practical article**: 教程 / 流程 / 方法
   - **Boss-facing article**: 管理 / 商业化 / 落地

4. **Write the article JSON**
   Always produce:
   - title
   - summary
   - body
   - optional cover direction
   - optional QR CTA sentence

5. **Handle images and QR code**
   - Place screenshots only where they support understanding.
   - Place QR code near the end by default.
   - Add one CTA sentence above the QR code.

6. **Prepare WeChat-ready markdown**
   Save markdown with frontmatter:
   - title
   - author
   - summary
   - coverImage (if available)

7. **Optional publish step**
   If the user asks to publish, hand off the final markdown to `baoyu-post-to-wechat`.

## Writing rules

- Prefer short, strong paragraphs.
- Cut repetitive spoken filler aggressively.
- Keep spoken authenticity, but remove rambling.
- Use subheads to create clear reading rhythm.
- For WeChat, prioritize readability over literal transcript fidelity.
- Keep one article centered on one core message.

## Image handling

When the user provides images:
- do not dump images randomly into the article
- decide whether each image is for:
  - proof / screenshot evidence
  - emotional pacing
  - explanatory diagram
  - QR code CTA
- place images only where they improve comprehension or conversion

When the user provides a QR code:
- default placement is near the end
- add one sentence CTA above it
- avoid placing QR code too early unless explicitly requested

## Recommended output structure

### 1. 核心观点
- 一句话说清这篇到底讲什么

### 2. 文章标题候选
- 标题 1
- 标题 2
- 标题 3

### 3. 正文大纲
- 开头钩子
- 3-5 个主体部分
- 收尾

### 4. 公众号成稿
Provide full markdown-ready article.

### 5. 配图建议
- cover direction
- inline image placement notes
- QR placement note (if applicable)

## Bundled scripts

- `scripts/build_article_brief.py`: convert transcript/minutes text into a compact article brief JSON
- `scripts/draft_article_json.py`: turn source text into a simple article JSON draft
- `scripts/compose_wechat_markdown.py`: convert article JSON + metadata into WeChat-ready markdown
- `scripts/audio_to_article_pipeline.py`: end-to-end wrapper from source text/audio metadata to markdown handoff plan

## References

- Read `references/workflow.md` for the full end-to-end process from audio/text to WeChat article.
- Read `references/style-guide.md` for how to turn spoken content into tighter公众号文章表达.
- Read `references/publish-handoff.md` for how this skill should hand off to the WeChat publishing workflow.
- Read `references/transcription-handoff.md` for how to integrate with meeting-minutes-whisper.
