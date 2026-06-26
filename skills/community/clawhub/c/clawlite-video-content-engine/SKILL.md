---
name: clawlite-video-content-engine
description: |
  中文：将 YouTube 视频转化为 ClawLite 营销资产的内容引擎，覆盖摘要、短视频脚本、X thread 与博客输出，支持知识型内容复用与渠道化分发。
  日本語：YouTube動画をClawLite向け教育・マーケ配信資産へ再構成。要約、短尺動画、Xスレッド、ブログ出力まで一貫して最適化。
  한국어：YouTube 영상을 ClawLite 마케팅 자산으로 재가공하는 콘텐츠 엔진. 요약, 숏폼, X 스레드, 블로그 산출물을 일괄 생성해 채널 확장을 지원.
  Español：Convierte videos de YouTube en activos de marketing para ClawLite: resumen, guion short-form, hilos de X y posts de blog para reutilización escalable del contenido.

---

# ClawLite Video Content Engine

Use this skill to convert third-party educational videos into **ClawLite-compatible educational marketing content**.

Core principle:
- do **not** treat source videos as raw material for plagiarism or blind reposting
- treat source videos as **learning inputs** that become:
  - beginner summaries
  - practical takeaways
  - explainer shorts
  - X threads
  - LinkedIn/Facebook posts
  - short blog summaries
  - soft ClawLite bridge content

## Outcome

Turn one source video into a **content pack**:
- 1 source summary
- 1 beginner translation
- 1 short-form video script
- 1 X thread
- 1 LinkedIn/Facebook post
- 1 short blog summary
- 1 CTA bridge to ClawLite

## Output location rule

Write outputs to a stable folder so the workflow is reusable and auditable.

Recommended structure:

```text
video-content/
  <videoId>/
    raw-transcript.md
    notebooklm-summary.md
    jk-marketing-asset.md
    source-note.md
    short-video-script.md
    x-thread.md
    linkedin-post.md
    blog-summary.md
    metadata.json
```

At minimum, write:
- `notebooklm-summary.md`
- `jk-marketing-asset.md`
- `source-note.md`
- `short-video-script.md`
- `x-thread.md`
- `blog-summary.md`
- `metadata.json`

## Workflow

### Normalization rule
NotebookLM output is not the final downstream input.
It must be normalized into a **JK / marketing-assets layer** before Elon, Tony, or Jenny consume it.

Use this chain:
- YouTube / transcript source
- raw extraction layer (for example `yt-dlp`)
- NotebookLM understanding layer
- JK marketing asset layer
- Elon / Tony / Jenny execution outputs

### 1. Capture the source video context
Record:
- title
- creator
- URL
- publish date if useful
- duration
- main topic
- likely beginner pain point

If NotebookLM is available, use it for transcript + summary extraction.
If NotebookLM is unavailable, create the structure manually from transcript/notes.

When using NotebookLM UI automation:
- use a screenshot-first workflow
- verify the exact input field before typing
- avoid generic textarea selectors
- confirm source creation before moving to content generation

Read `references/notebooklm-automation-guide.md` before automating NotebookLM.

### 2. Build a source note
Create a structured source note with:
- what the video is about
- 3 key takeaways
- strongest quote or idea
- why it matters for beginners
- where setup friction appears
- how ClawLite naturally bridges the gap

Read `references/source-note-template.md` when building the note.

### 3. Normalize into JK marketing assets
Convert the source + NotebookLM understanding into a reusable asset note for downstream lanes.

The JK asset should include:
- source context
- pain point
- beginner misunderstanding
- 3 key takeaways
- strongest idea / quote
- angle candidates
- hook candidates
- ClawLite bridge
- Elon social angle
- Tony blog angle
- Jenny lifecycle angle
- source / proof lines

This asset layer should become the **shared substrate** for downstream content generation.

Read `references/jk-marketing-asset-template.md` when building this layer.

### 4. Translate the source into ClawLite angles
Do **not** simply restate the creator video.
Create one or more of these angles:
- beginner translation
- practical summary
- “what matters most” summary
- “3 takeaways” summary
- “too long, didn’t watch” summary
- setup-friction reframing

Read `references/angle-framework.md` when choosing the angle.

### 5. Create the short-video script
Write a 30–90 second short video script with:
- hook
- 2–3 insights
- beginner framing
- soft ClawLite bridge
- CTA

Prefer:
- educational tone
- real user pain
- concise and clear subtitles
- no hard sell in the first half

Read `references/short-video-template.md` when writing the script.

### 6. Expand into a multi-channel content pack
Derive from the same source note and JK marketing asset:
- X thread
- LinkedIn/Facebook post
- short blog summary
- optional newsletter blurb

Read `references/content-pack-template.md` for the output structure.

### 7. Promote inbox assets into formal marketing-assets
Do not leave all value trapped in a one-off source folder.
After building the JK asset, normalize reusable pieces into the shared marketing-assets layer.

Typical destinations:
- pain points → `02-pain-points/`
- hooks → `01-hooks/`
- angles → `06-angles/`
- proof/source lines → `03-proof-points/`
- CTA lines → `07-cta/`

Rule:
- inbox/source asset = working note
- marketing-assets = durable shared substrate

At minimum, extract from the JK asset:
- reusable pain lines
- reusable hooks
- reusable angle lines
- source-backed proof lines

Read `references/asset-promotion-guide.md` before promoting shared assets.

### 8. Keep the content compliant
Always:
- attribute the source creator/video
- add original explanation and framing
- avoid copying long transcript passages
- avoid heavy reuse of original video/audio
- keep the result in commentary/education territory, not mirror-reposting

Read `references/compliance-and-positioning.md` before finalizing publishable outputs.

## ClawLite bridge rules

Use soft bridges such as:
- “The concept is powerful. The usual blocker is setup friction.”
- “If you want to try this without the setup pain, start with ClawLite.”
- “This is the idea. ClawLite makes the first step easier.”

Avoid:
- overclaiming
- hijacking the creator’s work into a hard product ad
- turning every summary into aggressive CTA spam

## Recommended output order

1. source note
2. beginner translation
3. short-video script
4. X thread
5. LinkedIn/Facebook post
6. short blog summary
7. ClawLite CTA bridge

## Example use case

If given a source video like `https://www.youtube.com/watch?v=fd4k16REDOU`, produce:
- a summary note
- 3 key beginner takeaways
- a 45-second short script
- a ClawLite bridge angle
- a thread/post/blog content pack

## NotebookLM automation layer

Use NotebookLM as the **ingestion layer**, not the final content layer.
Its job is to help extract:
- transcript understanding
- summaries
- section structure
- notes and source context

Your real output should still be a ClawLite content pack.

When automating NotebookLM:
- screenshot before every action
- verify the modal/input target before typing
- avoid the sidebar search textarea
- re-dispatch input/change events when UI state does not update
- verify that the source was actually added before continuing

Read `references/notebooklm-automation-guide.md` before doing any NotebookLM UI automation.

## Read next when needed
- `references/source-note-template.md`
- `references/jk-marketing-asset-template.md`
- `references/angle-framework.md`
- `references/short-video-template.md`
- `references/content-pack-template.md`
- `references/asset-promotion-guide.md`
- `references/compliance-and-positioning.md`
- `references/notebooklm-automation-guide.md`
