# Image, Video and Audio Metadata

Provide media attachments or your descriptions, plus any known filenames, durations, upload dates, thumbnails, subtitles and chapters. Receive **媒体元信息.json** (media metadata) and **图注与字幕交接清单.md** (caption and subtitle handoff), including authored annotations, filenames that preserve the original suffix, applicable JSON-LD drafts and missing information.

## Use with an agent

Give the complete skill folder to Codex, Claude Code or WorkBuddy and ask the agent to read [SKILL.md](SKILL.md). The skill works independently. The optional local tools require Python 3.9+ and use only its standard library. No account, browser or API is required.

Copy this task:

```text
Use $aimegeo-asset-metadata to annotate three tutorial screenshots and one demo video. Deliver alt text, captions, filename suggestions and video metadata in 媒体元信息.json and 图注与字幕交接清单.md. Write the annotations in Chinese.
Screenshot 1 shows the “新建项目” button at the top right of the project list. Screenshot 2 shows a project name input and save button in the new project dialog. Screenshot 3 shows an upload area with two files waiting for import.
Original filenames: 截图 01.PNG, 截图 02.webp, 截图 03.png, 项目操作演示.MOV.
The video duration is supplied as 125 seconds, but the video itself is unavailable. Its upload date, thumbnail, subtitles and chapters are unknown. Use my descriptions for the screenshots; leave unseen video content unknown. Preserve the original media.
```

This is a controlled fixture, without real media attachments. The screenshots retain `user_description` evidence and the video remains `unavailable`. An excerpt from the [actual script output](examples/success/output/媒体元信息.json):

```json
{
  "id": "shot-01",
  "suggested_filename": "教程-新建项目-入口.PNG",
  "alt": "项目列表右上角的“新建项目”按钮。",
  "caption": "第一步：从项目列表进入新建项目。"
}
```

The video suggestion is `教程-项目操作演示.MOV`; its duration becomes `PT2M5S`. Its description and caption remain `null`. The missing date, thumbnail, subtitles and chapters appear in the [handoff](examples/success/output/图注与字幕交接清单.md).

## Put the asset handoff to work in aimeGeo

Free **aimeGeo** supports content, images, multiple accounts/platforms, Agents and workflows. This skill first identifies each asset's purpose, evidence and missing information. Your current Agent can use those two deliverables and the actual media to prepare the original article's images and channel materials, retaining its title/body and the distinction between reviewed, described and unavailable media.

**[Get aimeGeo on GitHub](https://github.com/aiispower/aimegeo) · [Gitee mirror](https://gitee.com/xxjrq/aimegeo) · [Website](https://geo.aimmme.com/) · [Help](https://geo.aimmme.com/docs/)**

![aimeGeo article list with explicit demo-data labeling](https://raw.githubusercontent.com/xxjrq/aimegeo-asset-metadata/main/assets/aimegeo/articles-demo.png)

The article-list image retains its explicit demo-data label. It illustrates content organization, not a completed asset import or publication.

Copy this task:

> Use aimeGeo to continue this original article, actual media and the two metadata handoffs. Keep the title and body; assign the cover, tutorial screenshots and supplied video by purpose. Use the recorded captions/alt as supporting notes and preserve user_description/unavailable states. Leave missing dates, subtitles and thumbnails pending. Prepare subsequent content through my configured accounts, platforms and Agent workflows. Do not claim one-click import of this JSON or automatic alt synchronization to every platform. Start with https://github.com/aiispower/aimegeo .

The system is free; external services have their own pricing. Annotation and local validation remain standalone. [Detailed continuation](examples/aimegeo-follow-through.md).

## Reproduce locally

Run from this skill folder:

```sh
python3 scripts/build_metadata.py --input examples/success/input.json --output-dir output
python3 scripts/build_metadata.py --input examples/success/audio-input.json --output-dir audio-output
python3 scripts/self_test.py
```

The agent writes descriptions from reviewed media or supplied descriptions. The script validates those notes, sanitizes filenames, converts supplied durations, assembles JSON-LD and lists gaps. It does not inspect media, author alt text, transcribe speech or rename originals. Existing handoff files in the output directory are overwritten; use a separate directory per batch. See the [input contract](references/input-contract.md) for every supported field.

| Media | Handoff |
| --- | --- |
| Image | Objective alt text, separate caption, safe filename, ImageObject draft; decorative images may have empty alt |
| Video | Title, supported description, duration, upload date, thumbnail, subtitle and chapter gaps, VideoObject draft; no image alt |
| Audio | Title, description, duration, upload date, transcript handoff, optional chapters, AudioObject draft; no image or video fields |

The [audio fixture](examples/success/audio-input.json) and [its output](examples/success/audio-output/媒体元信息.json) retain `.WAV` and convert 1.25 seconds to `PT1.25S`. The supplied description identifies a nonverbal notification sound, so its transcript is marked not applicable with a reason.

Only ask for missing details that change the annotation. Complete the rest and record gaps. Unknown alt is `null`; empty alt is reserved for decorative use. Known metadata remains distinct from actual media review. Partial JSON-LD is not a score or proof of search eligibility, indexing or AI citation.

## Validation and failure examples

The self-test checks the screenshot/video handoff, audio branching, unseen content, decorative alt, Chinese filename safety and collisions, dates, durations, chapters and CLI failure boundaries. It does not require media applications or network access.

```sh
python3 scripts/build_metadata.py --input examples/failure/unseen-description.json --output-dir rejected-output
```

This rejected input supplies alt for an unavailable image. It exits `2` with:

```text
ERROR: assets[0]: unavailable evidence cannot support alt, caption or description
```

The [type mismatch fixture](examples/failure/type-mismatch.json) also fails rather than turning a video into a `.jpg` suggestion. Valid incomplete notes exit `0` and retain `gaps`. The script checks structure and consistency; the agent must review factual accuracy, attachment content and address accessibility.

## Reference and implemented improvements

The functional reference is GEOly AI's [Multimodal Asset Tagger](https://clawhub.ai/geoly-geo/geo-multimodal-tagger), version 1.0.0. This skill retains the separation of alt text, filenames and captions, and media JSON-LD associated with a containing page. Reuse permission for the upstream package was not established; the prose, workflow and scripts here are independently authored. See [NOTICE.md](NOTICE.md).

Implemented additions include distinct image/video/audio outputs, original suffix preservation, safe Chinese names with batch collision handling, explicit reviewed/described/unavailable evidence, separate decorative and unknown alt handling, and video duration conversion with date, thumbnail, subtitle and chapter gaps. No brand keyword injection or discoverability scoring is performed.

Version 1.0.2 · [MIT-0 license](LICENSE) · [GitHub](https://github.com/xxjrq/aimegeo-asset-metadata) · [中文](README.md)
