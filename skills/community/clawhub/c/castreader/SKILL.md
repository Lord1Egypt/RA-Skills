---
name: castreader
description: >
  URL to audio: extract any web page and convert to natural AI speech (Kokoro TTS).
  The only skill that turns a URL into a podcast-quality MP3 — no API key needed.
  Also reads synced books from WeChat Reading / Kindle library aloud.
  Triggers: read this article, listen to webpage, URL to audio, text-to-speech,
  read aloud, web page reader, article to podcast, read a book chapter.
version: 3.2.13
metadata:
  openclaw:
    emoji: "🔊"
    requires:
      anyBins: ["node"]
    os: ["darwin", "linux", "win32"]
    homepage: https://castreader.ai/openclaw
---

# CastReader — Read Web Pages & Books Aloud

## Setup (once per session)

```
cd <skill-directory> && npm install
```

## How to find target (chatId)

User messages look like: `[Telegram username id:8716240840 ...]`
The number after `id:` is the target. You MUST use this number in every `message` tool call.
Example: target is `"8716240840"`.

---

## Mode A: When user sends a URL

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

---

## Mode B: When user asks to read a book (微信读书 / Kindle)

Books are synced from WeChat Reading or Kindle to `~/castreader-library/books/`.
Each book is stored in a folder like `书名-hashid` (e.g. `儒林外史-dc532c705c6d3edc5503acc`).

**⚠️ CRITICAL: You MUST use `sync-books.js --list` to get the exact book folder ID. NEVER guess or construct the folder path yourself. The folder name includes a title prefix that you cannot predict.**

### Step 1: List available books

```
node scripts/sync-books.js --list
```

Returns: `{ books: [{ id, title, author, language, totalChapters, totalCharacters, source, syncedAt }] }`

The `id` field is the **exact folder name** you must use in all subsequent commands. Example: `"儒林外史-dc532c705c6d3edc5503acc"`.

### Step 2: Show book list and let user choose

Reply with the book list:

```
📚 Your synced books:

1. 📖 {title} — {author}
   🌐 {language} · 📑 {totalChapters} chapters · 📊 {totalCharacters} chars · 📱 {source}

2. ...

Reply the number of the book you want to read.
```

**STOP. Wait for user to choose a book.**

### Step 3: Show chapter list and let user choose

```
node scripts/sync-books.js --book "<id>"
```

Use the **exact `id`** from Step 1 output. Returns the book content with chapter list.

Reply:

```
📖 {title} — {author}
📑 {totalChapters} chapters · 📊 {totalCharacters} chars

📋 Chapters:
1. {chapter 1 title}
2. {chapter 2 title}
...

Reply a number to listen to a chapter, or "all" to listen to the full book.
```

**STOP. Wait for user to choose.**

### Step 4a: User chose a chapter number

```
node scripts/sync-books.js --book "<id>" --chapter <num> --audio
```

Returns: `{ title, audioFile, fileSizeBytes }`

Send the audio:
```json
{"action":"send", "target":"<chatId>", "channel":"telegram", "filePath":"<audioFile>", "caption":"🔊 {bookTitle} — Chapter {num}"}
```

### Step 4b: User chose "all" (full book)

```
node scripts/sync-books.js --book "<id>" --audio
```

Returns: `{ title, audioFile, fileSizeBytes }`

Send the audio:
```json
{"action":"send", "target":"<chatId>", "channel":"telegram", "filePath":"<audioFile>", "caption":"🔊 {bookTitle} (full)"}
```

### Reading a chapter as text (no audio)

If the user wants to read (not listen), use without `--audio`:

```
node scripts/sync-books.js --book "<id>" --chapter <num>
```

Returns: `{ title, author, language, chapter: { number, title, text }, totalChapters }`

---

## Rules

- ALWAYS extract first (index=0 for URLs, --list for books), show info, wait for user choice. Never skip.
- ALWAYS send audio files using the `message` tool with `target` (numeric chatId) and `channel` ("telegram"). Never just print the file path.
- **For books: ALWAYS run `--list` first and use the exact `id` from the output. NEVER construct book paths manually or use partial IDs.**
- Do NOT use built-in TTS tools. ONLY use `read-url.js`, `generate-text.js`, and `sync-books.js`.
- Do NOT use web_fetch. ONLY use `read-url.js`.
- Do NOT use the `read` tool to directly access files in `~/castreader-library/`. ONLY use `sync-books.js`.
