# doubao-asr

> Agent Skill for transcribing audio files via ByteDance Volcengine **Seed-ASR 2.0** (豆包录音文件识别模型2.0)

Best-in-class Chinese speech recognition — Mandarin, Cantonese, Sichuan dialect, and 13+ languages. With speaker diarization, SRT subtitle export, and three recognition tiers (standard / express / offpeak), up to 5 hours / 512MB per file.

中文语音识别准确率业界领先——支持普通话、粤语、四川话等方言及 13+ 种语言。自带说话人分离、SRT 字幕导出、三档识别版本（标准/极速/闲时），单文件最长 5 小时 / 512MB。

## Why this skill?

Setting up Volcengine's Doubao Audio File Recognition 2.0 (豆包录音文件识别模型2.0, recorded audio → text) from scratch involves **4 environment variables across 3 different console pages** (Speech console, IAM, TOS). Without guidance, this typically takes 1-2 hours of doc-hunting and trial-and-error.

This skill provides **step-by-step bilingual setup instructions** (中英双语) baked into `SKILL.md`, so your AI agent can walk you through the entire process in ~10 minutes.

从零配置火山引擎豆包录音文件识别模型2.0（录音转文字）涉及 **3 个不同控制台页面的 4 个环境变量**。没有引导的话通常需要 1-2 小时翻文档踩坑。本 skill 在 `SKILL.md` 中内置了**中英双语分步引导**，AI agent 可以在约 10 分钟内带你完成全部配置。

## Install

### Claude Code

```bash
claude /install-skill https://github.com/vahnxu/doubao-asr
```

Or manually copy to `~/.claude/skills/doubao-asr/`.

### OpenClaw / ClawHub

Available on [ClawHub](https://clawhub.com) as `doubao-asr`.

### Manual

```bash
git clone https://github.com/vahnxu/doubao-asr.git
cd doubao-asr
pip install -r requirements.txt   # pins requests to a reviewed version
python3 scripts/transcribe.py /path/to/audio.m4a
```

## Quick start

```bash
# Basic transcription
python3 scripts/transcribe.py /path/to/audio.m4a

# Save to file
python3 scripts/transcribe.py /path/to/audio.m4a --out /tmp/transcript.txt

# JSON output
python3 scripts/transcribe.py /path/to/audio.m4a --json --out /tmp/result.json

# Direct URL (skip upload)
python3 scripts/transcribe.py https://example.com/audio.mp3

# Disable speaker diarization
python3 scripts/transcribe.py /path/to/audio.m4a --no-speakers

# Export SRT subtitles (from per-utterance timestamps) / 导出 SRT 字幕
python3 scripts/transcribe.py /path/to/audio.m4a --srt --out /tmp/subs.srt

# Express tier (极速版): fastest — short audio returns in seconds, single-shot, audio ≤ 2h
python3 scripts/transcribe.py /path/to/audio.m4a --tier express

# Offpeak tier (闲时版): cheapest — async queue, completes within 24h, fetch later with --query
python3 scripts/transcribe.py /path/to/audio.m4a --tier offpeak            # prints request_id
python3 scripts/transcribe.py --query <request_id> --tier offpeak          # fetch result when ready
```

## Sample output

With speaker diarization enabled (default), the transcript is grouped by speaker:

带说话人分离（默认开启）时，转写文本按说话人分组输出：

```
Speaker 1:
今天这期节目我们聊聊语音识别的落地场景。

Speaker 2:
好的，我先分享一下我们团队最近的实践。
把会议录音自动转成纪要之后，整理时间大概省了一半。

Speaker 1:
这个效果确实不错，展开讲讲？
```

## Credentials

See the detailed setup guide in [SKILL.md](./SKILL.md#credentials-setup) — with step-by-step instructions for each environment variable.

| Variable | Required | Description |
|---|---|---|
| `VOLCENGINE_API_KEY` | Yes | ASR API key (UUID) from Speech console |
| `VOLCENGINE_ACCESS_KEY_ID` | Yes | IAM Access Key ID (starts with `AKLT`) |
| `VOLCENGINE_SECRET_ACCESS_KEY` | Yes | IAM Secret Access Key |
| `VOLCENGINE_TOS_BUCKET` | Yes | TOS bucket name |
| `VOLCENGINE_TOS_REGION` | Yes | TOS region code, must match bucket region. Overseas: e.g. `cn-hongkong`, `ap-southeast-1`; China: `cn-beijing` |

## Supported formats

WAV, MP3, MP4, M4A, OGG, FLAC — up to 5 hours, 512MB max.

## Troubleshooting / 常见问题

**Error**: `45000006 [Invalid audio URI] audio download failed` ([issue #1](https://github.com/vahnxu/doubao-asr/issues/1))
**Cause**: The ASR service cannot download the audio. The script submits a presigned GET URL, which is only valid if the signing IAM sub-user itself has READ permission on the object — a bucket policy that grants write but not read (or one with IP restrictions) lets the upload succeed while the ASR-side download fails. / ASR 服务下载不到音频。脚本提交的是预签名 GET URL，其有效性取决于签名的 IAM 子用户自身是否有该对象的读权限——桶策略只授了写没授读（或带 IP 限制条件）时，上传能成功但 ASR 侧下载失败。
**Solution**: Fix the bucket policy: grant the sub-user **read + write** via the "Folder Read/Write" template (SKILL.md Step 3), with no IP-restriction conditions. Setting the object ACL to public read also works as a quick diagnostic, but it exposes your audio to the whole internet — do not leave it on. / 修桶策略：按 SKILL.md 第三步用「文件夹读写」模板给子用户授**读+写**权限，且不带 IP 限制条件。把对象 ACL 设为公网读也能通（可作快速诊断），但会把音频暴露给全网——不要长期保留。

More troubleshooting entries (403 upload errors, slow cross-border upload, wrong console API key, etc.) in [SKILL.md § Troubleshooting](./SKILL.md#troubleshooting--常见问题).

更多常见问题（上传 403、跨境上传慢、API Key 来源错误等）见 [SKILL.md § Troubleshooting](./SKILL.md#troubleshooting--常见问题)。

## License

Apache-2.0
