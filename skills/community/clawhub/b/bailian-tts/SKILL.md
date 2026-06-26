---
name: bailian-tts
description: Generate speech audio with 阿里云百炼 TTS via the `bailian-cli` npm package. Use when users ask to convert text to voice, choose voices/languages, batch-generate narration, or troubleshoot 百炼 TTS setup (npm install, API key, region, output format/path).
---

# Bailian TTS

Use this skill to produce speech audio from text with `@hackerpl/bailian-cli`.

## Quick Workflow

1. Check CLI availability.
2. Check `BAILIAN_API_KEY`.
3. If key is missing, guide user to prepare one in 阿里云百炼.
4. Run `bailian tts` with requested voice/language/style.
5. Return output path (or base64 when requested). Default audio output directory: `~/.openclaw/media/audio`.

## 1) Check and install CLI

Run:

```bash
npm ls -g --depth=0 @hackerpl/bailian-cli
```

If missing, install:

```bash
npm i -g @hackerpl/bailian-cli
```

## 2) Check API key

Run:

```bash
[ -n "$BAILIAN_API_KEY" ] && echo SET || echo MISSING
```

If missing, ask user to create and configure key from the 阿里云百炼官方入口（控制台/平台）：

- https://bailian.console.aliyun.com/

Then set it:

```bash
export BAILIAN_API_KEY="sk-xxxx"
# optional
export BAILIAN_REGION="beijing"   # or singapore
```

## 3) Generate speech (bailian-cli)

Basic (default to OpenClaw media folder):

```bash
mkdir -p ~/.openclaw/media/audio
bailian tts -t "你好，欢迎使用百炼 TTS 服务" -o url -d ~/.openclaw/media/audio
```

Specify voice/language:

```bash
mkdir -p ~/.openclaw/media/audio
bailian tts -t "Hello world" -v "Ethan" -l "English" -o url -d ~/.openclaw/media/audio
```

With style instruction:

```bash
mkdir -p ~/.openclaw/media/audio
bailian tts -t "春眠不觉晓" -v "Serena" -i "用温柔缓慢的语调朗读" -o url -d ~/.openclaw/media/audio
```

Return base64 instead of file:

```bash
bailian tts -t "测试" -o data
```

Custom output directory:

```bash
bailian tts -t "你好世界" -d "./audio"
```

## 4) Voices and languages

- For live lookup:

```bash
bailian tts --list-voices
```

- Full built-in table: read `references/voices-and-languages.md`.

## 5) Operational notes

- Keep text length within CLI limit (600 chars per request).
- Default output directory: `~/.openclaw/media/audio` (create with `mkdir -p ~/.openclaw/media/audio`).
- Prefer `-o url` for file delivery, `-o data` for programmatic pipelines.
- Respect user privacy: do not upload sensitive text externally without explicit confirmation.
- If generation fails, check in order: API key → region → network → voice/language spelling.
- When producing many clips, keep a consistent voice and instruction style for tonal continuity.
