---
name: castreader
description: >
  Read any web page aloud with natural AI voices. Extract article text from any URL
  and convert it to audio (MP3). Use when the user wants to:
  listen to a webpage, read an article aloud, convert URL to audio,
  text-to-speech for a link, read this page to me, listen to this article.
version: 2.1.0
metadata:
  openclaw:
    emoji: "🔊"
    requires:
      anyBins: ["node"]
    os: ["darwin", "linux", "win32"]
    homepage: https://castreader.ai/openclaw
---

# CastReader — Read Any Web Page Aloud

## Setup (once per session)

```
cd <skill-directory> && npm install --silent 2>/dev/null
```

## How to find target (chatId)

User messages look like: `[Telegram username id:8716240840 ...]`
The number after `id:` is the target. You MUST use this number in every `message` tool call.
Example: target is `"8716240840"`.

## When user sends a URL, follow these steps:

### Step 1: Extract article

```
node scripts/read-url.js "<url>" 0
```

Returns: `{ title, language, totalParagraphs, totalCharacters, paragraphs[] }`

### Step 2: Show info + ask user to choose

Reply with this text:

```
📖 {title}
🌐 {language} · 📝 {totalParagraphs} paragraphs · 📊 {totalCharacters} chars

📋 Summary:
{write 2-3 sentence summary from paragraphs}

Reply a number to choose:
1️⃣ Listen to full article (~{totalCharacters} chars, ~{Math.ceil(totalCharacters / 200)} sec to generate)
2️⃣ Listen to summary only (~{summary_char_count} chars, ~{Math.ceil(summary_char_count / 200)} sec to generate)
```

**STOP. Wait for user to reply 1 or 2.**

### Step 3a: User chose 1 (full article)

Reply: `🎙️ Generating full audio (~{totalCharacters} chars, ~{Math.ceil(totalCharacters / 200)} seconds)...`

```
node scripts/read-url.js "<url>" all
```

Then send the audio file using the `message` tool:
```json
{"action":"send", "target":"<chatId>", "channel":"telegram", "filePath":"<audioFile>", "caption":"🔊 {title}"}
```

Reply: `✅ Done!`

### Step 3b: User chose 2 (summary only)

Reply: `🎙️ Generating summary audio...`

Save the SAME summary text you showed in Step 2 to a file and generate:
```
echo "<summary text>" > /tmp/castreader-summary.txt
node scripts/generate-text.js /tmp/castreader-summary.txt <language>
```

Then send the audio file using the `message` tool:
```json
{"action":"send", "target":"<chatId>", "channel":"telegram", "filePath":"/tmp/castreader-summary.mp3", "caption":"📋 Summary: {title}"}
```

Reply: `✅ Done!`

## Rules

- ALWAYS extract first (index=0), show info, wait for user choice. Never skip.
- ALWAYS send audio files using the `message` tool with `target` (numeric chatId) and `channel` ("telegram"). Never just print the file path.
- Do NOT use built-in TTS tools. ONLY use `read-url.js` and `generate-text.js`.
- Do NOT use web_fetch. ONLY use `read-url.js`.
