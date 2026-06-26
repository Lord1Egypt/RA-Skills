[English](README.md) | [中文](README.zh-CN.md) | [日本語](README.ja.md)

# ChatGPT Memory Extraction 🧠✨

An [OpenClaw](https://github.com/openclaw/openclaw) skill that turns your years of ChatGPT conversations into a **structured, searchable personal memory archive**.

## Why I made this

I chatted with ChatGPT for over three years — 500+ conversations, 60,000+ messages. Papers I read, things I learned, decisions I made, the happy and hard moments, the people I met along the way — all of it was locked inside massive JSON files I couldn't actually look through 😢

So I built this little tool. It takes your ChatGPT export data and walks you through organizing it into a timeline-based memory archive, pulling out people, learning journeys, and key life events along the way.

And the archive isn't just for looking back — you can feed it to your OpenClaw agent or any other AI assistant so that **it truly knows you from day one**. No more spending ages re-introducing yourself every time you start with a new AI 😅

## What it does

- 📦 **Auto-extract**: A Python script converts the JSON into readable text files, sorted by year and quarter
- 📖 **Deep reading**: Guides the AI to read each conversation thoroughly (not just skim the title), producing structured quarterly timelines
- 👥 **People profiles**: Extracts every person mentioned and builds them a profile
- 🎯 **Topic threads**: Academic growth, emotional moments, life changes, skills learned — organized by theme

## An honest note

Here's the thing — AI agents **really do tend to cut corners** when processing lots of text 😅 I learned this the hard way, many times over. So this skill comes with built-in quality rules targeting common AI laziness patterns (like summarizing after only reading the first few messages, writing "XX messages about various topics" as if that means anything, or claiming "files updated" when nothing actually changed…).

Even with these rules, **I'd still recommend checking the AI's output yourself**. Review each quarter when it's done, and ask it to redo anything that looks shallow. The best results come from working together with the AI, not just handing it off and walking away~

## How to use

### 1. Install

```bash
# Via ClawHub
npx clawhub install chatgpt-memory-extraction

# Or manually from GitHub
git clone https://github.com/cyresearch/chatgpt-memory-extraction.git ~/.openclaw/workspace/skills/chatgpt-memory-extraction
```

### 2. Export your ChatGPT data

Go to [ChatGPT](https://chat.openai.com) → Settings → Data controls → Export data → Confirm

> ⏳ The export might take **a few hours or even a day or two** — longer if you have a lot of data. OpenAI will email you when it's ready~

### 3. Start organizing!

Tell your OpenClaw agent:

> "I exported my ChatGPT data — help me turn it into a memory archive."

It'll walk you through: extract → read quarter by quarter → write timelines → you review → extract people and topics 🌱

## What the output looks like

```
memory/
├── timeline/{year}/Q{1-4}.md   # Quarterly timelines (the core files~)
├── people/{category}/*.md       # People profiles
├── topics/*.md                  # Topic-based records
├── meta/extraction-log.md       # Progress tracking
└── raw/{year}_Q{n}/             # Raw conversation texts (for verification)
```

## What you'll need

- [OpenClaw](https://github.com/openclaw/openclaw)
- Python 3.8+
- Your ChatGPT data export (the `.zip` from OpenAI)

## License

MIT — see [LICENSE](LICENSE)
