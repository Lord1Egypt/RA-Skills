---
name: bilibili-course-notes
description: "B站网课转笔记 / Bilibili lecture & course notes. 用户要把一节 B 站网课、讲座、公开课（BV 号、b23.tv 短链或分享文字）整理成学习笔记，或要把一整套分P 课程逐 P 做成笔记时使用。输出 Markdown：8 分钟以上的视频带「带时间的章节大纲」，要点附原话和时间，逐字稿每行带 [mm:ss]；分P 课程每 P 一个文件，开始前先报每 P 时长和要花的积分。不登录 B 站、不要 Cookie、不下载视频。没有 Key 可免费看一条摘要；完整笔记需要 LinkDigest API Key（注册送 10 积分）。"
version: 1.0.0
homepage: https://linkdigest.dev/zh/bilibili-shipin-biji?ref=skill-bilibili-course-notes
metadata: {"openclaw":{"requires":{"anyBins":["python3"]},"primaryEnv":"LINKDIGEST_API_KEY","envVars":[{"name":"LINKDIGEST_API_KEY","required":false,"description":"LinkDigest API Key（ld_live_ 开头），在 https://linkdigest.dev/signin?ref=skill-bilibili-course-notes&next=/app/keys 创建；不设也能免费看一条摘要"}],"homepage":"https://linkdigest.dev/zh/bilibili-shipin-biji?ref=skill-bilibili-course-notes"}}
required_environment_variables:
  - name: LINKDIGEST_API_KEY
    prompt: "LinkDigest API key (starts with ld_live_)"
    help: "https://linkdigest.dev/signin?ref=skill-bilibili-course-notes&next=/app/keys"
    required_for: "full notes and multi-part courses; without it the script shows one free summary"
---

# B站网课 → 学习笔记（大纲 · 要点 · 逐字稿 · 分P）

A lecture on Bilibili is an hour of speech and slides. Agents cannot fetch it (Bilibili answers server requests with HTTP 412), and a raw transcript is not notes. This skill turns one lecture — or a whole multi-part course — into Markdown notes a student can study from.

## Decide first

| The user wants | Run |
| --- | --- |
| Notes for one lecture | `python3 {baseDir}/scripts/bili2notes.py "<link>" -o note.md` |
| Only what was said, cheapest | add `--depth script` |
| Slide / board text too | add `--depth full --on-screen` (dearer: frames are read) |
| Parts 1–10 of a 分P course | `python3 {baseDir}/scripts/bili2notes.py "<link>" --parts 1-10 --out-dir notes/` |
| Every part | `--parts all` (the script lists each part's length and the credit total and asks before starting; `--yes` skips the question) |
| Re-render notes from a saved API reply, offline | `--from-json reply.json` |

The link can be a full `bilibili.com/video/BV…` address, a `?p=N` part link, a `b23.tv` short link, a bare BV id, or the whole share text copied from the app.

## What a note contains

1. Header: title, uploader, date, length, and for a 分P video "第 N P / 共 M P".
2. **大纲** (videos of 8 minutes and longer read since 2026-11-10): sections with start–end times, a title and one to three lines each. Section times are taken from the transcript's own timestamps and checked in code, so every time can be found in the video.
3. **要点**: the key points, each followed by the quoted line and time it came from when one was found.
4. **逐字稿**: every line with `[mm:ss]`.

Real output: [`examples/bilibili/sample-note.md`](https://github.com/jcaiagent7143-ui/linkdigest-mcp/blob/main/examples/bilibili/sample-note.md) — 跟李沐学AI《Transformer论文逐段精读》(87 min): 17 outline sections, 15 key points, 527 transcript lines.

## Tell the user

- Speech recognition misspells names and terms (in that lecture "attention" once came out as "tension"); check them against the video.
- A long lecture's last outline section can be coarse; split it by the transcript if it covers much more than its title.
- Exit codes: 3 key refused · 4 not enough credits (the message names what the balance can read instead) · 5 the video cannot be read (deleted, private, members-only) · 7 timed out (rerun; the job is not charged twice).

## Cost and limits

Billed per started minute of video and cheaper the less is read: a 10-minute video is 5 credits speech-only (`--depth script`), an 87-minute lecture is 45 credits transcript-first (the default). Transcript-first reads up to 60 minutes per video on the free plan and 2 hours on paid plans. A video anyone has already read at that depth is free. Links that cannot be read are not charged.

## Privacy

Only the link is sent to linkdigest.dev. No Bilibili account, cookie or login is used; the video is read through the player Bilibili publishes for other sites and deleted after reading. https://linkdigest.dev/privacy · support@linkdigest.dev
