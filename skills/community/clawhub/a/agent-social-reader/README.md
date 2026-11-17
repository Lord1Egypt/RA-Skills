# 👁️ Agent-Social-Reader

<p align="center">
 <strong>Ask your agent to read a specific social link → AI summarizes → Save that item to Notion / Obsidian / ima when you request it<br/> No social login. No cookies. Lower account risk.<br/><br/>
Reads content from X, Instagram, YouTube, Xiaohongshu, and more — with optional per-item archiving to your personal knowledge base</strong>
</p>
<p align="center">
 <a href="#-quick-overview">Quick Overview</a> ·
 <a href="#-what-it-does">What It Does</a> ·
 <a href="#-supported-platforms">Supported Platforms</a> ·
 <a href="#-quick-start">Quick Start</a> ·
 <a href="docs/README_cn.md">中文</a>
</p>


---

## 🎯 Quick Overview

As a knowledge worker, product manager, or heavy AI agent user, the moment you drop an X (Twitter), Reddit, WeChat article, or Xiaohongshu link into your AI, you hit walls: login barriers, anti-scraping blocks, IP bans, or HTML garbage. On top of that, you're stuck maintaining a separate tool for every single platform.

**The problem this Skill solves:**

❌ Before:

```
You: drop a Twitter/Reddit/Xiaohongshu link into your agent
Agent: "I can't access that" / returns garbled HTML
You: resort to manual copy-paste, screenshots, or give up
```

✅ Now:

```
You: ask your agent to read a specific social media link
Agent: reads it → summarizes it
You: optionally say "save this to Notion / Obsidian / ima"
→ content neatly filed in your knowledge base
```

**Core value**:
- ✅ **Complete loop**: Read → Summarize → Archive — end-to-end in one workflow
- ✅ **Broad coverage**: 20+ global social platforms (TikTok, Instagram, X, YouTube, Reddit, Douyin, Xiaohongshu, Bilibili...)
- ✅ **Lower account risk**: No need to log in to personal social accounts, no cookie required — reduces risk of suspension from cookie-based access
- ✅ **Flexible cost**: Free tools first; optional paid enhancements from $2.90/month

> 💡 **Design philosophy**: Use free tools wherever possible; reach for the most cost-effective paid option only when free tools won't do. You decide which tier to use.

> ❤️ **Special thanks to** [Agent-Reach](https://github.com/Panniantong/Agent-Reach) by [@Panniantong](https://github.com/Panniantong). Agent-Reach proved that getting an AI agent to read web content was achievable — this project is a personal iteration on the same idea, with a tighter focus on social content reading and knowledge base archiving.

---

## ✨ What It Does

After installing this Skill, your agent gains the following capabilities (no code required):

| Content Source | Tool | Cost |
| :--- | :--- | :--- |
| General web pages | Jina Reader (r.jina.ai) | ✅ Free, no API key required |
| Public X/Twitter posts | FxTwitter API | ✅ Free, no API key or cookie required |
| YouTube (with subtitles) | youtube-transcript-api | ✅ Free, no API key required |
| Weibo | Jina Reader (r.jina.ai) | ✅ Free, bypasses login wall |
| WeChat public accounts | Camoufox | ✅ Free, headless browser handles JS rendering<br/>(falls back to AgentLens or prompts you to paste text if it fails) |
| **20+ global social platforms** | AgentLens API | 🎁 20 free requests per month<br>💵 Then $2.90/month (200 requests) |
| Video summarization (TikTok, YouTube and other videos without subtitles) | Whisper transcription + LLM | ✅ Free locally (requires setup)<br>💵 OpenAI API $0.006/minute |
| RSS feeds | Python feedparser | ✅ Free |
| Full-web semantic search | Agent runtime built-in search | ✅ Free (provided your current runtime supports it) |
| Save to Notion upon request | Agent writes after confirmation | ✅ Free (your Notion Token) |
| Save to Obsidian upon request | Agent writes after confirmation | ✅ Free (local path) |
| Save to ima upon request | Agent writes after confirmation | ✅ Free (ima OpenAPI, accessible from WeChat/Feishu/WeCom) |

---

## 🌐 Supported Platforms

Via **AgentLens API**, the following social media platforms are accessible and verified (if you spot errors or discover additional platforms, please let us know):

| Global Platforms | Chinese Platforms |
| :--------------- | :---------------- |
| TikTok | Douyin |
| Instagram | Xiaohongshu |
| YouTube | Bilibili |
| X (Twitter) | Weibo |
| Facebook | Kuaishou |
| Threads | Xigua Video |
| Reddit | Zhihu (columns) |
| LinkedIn | WeChat Official Account (articles) |
| Twitch (clips) | WeChat Channels |
| Pinterest | |
| Bluesky | |
| Snapchat | |
| Kick (clips) | |
| Lemon8 | |

* **AgentLens reads**: main text content + images/video files (original media links)
* **AgentLens does not read**: comments, timelines, X Lists, private account content, or reply/conversation threads on X and Reddit

---

## 🚀 Quick Start

### Step 1: Install the Skill (10 seconds)

Copy and paste this into whichever AI agent you're using (Claude Code, Cursor, Codex, OpenClaw, Hermes Agent, WorkBuddy, etc.):

```
Install the Agent-Social-Reader Skill: https://github.com/hermiod99-vibe/Agent-Social-Reader
```

That's it. Your agent handles everything else.

---

### Step 2: Start using it immediately (free right away)

After installation, these features work at no cost:

- "Show me what's on this tweet"
- "Summarize this WeChat article"
- "What does this webpage say?"
- "Subscribe to this RSS feed"

---

### Step 3: Optional enhancements (as needed)

#### 🔓 Unlock 20+ social platform reading (TikTok, Reddit, Instagram, Douyin, Xiaohongshu, Bilibili, etc.; X/Twitter single public posts, Weibo posts, WeChat Official Account articles use the free tool path first)

The first time you ask your agent to read from these platforms, it will prompt:

> "This platform requires an AgentLens API key to read. It unlocks 20+ major social platforms. Get your free API key in 10 seconds at https://agentlensapi.io/pricing — 20 requests/month free; paid plans from $2.90/month (200 requests), see pricing page. Once you paste it here, I'll handle the rest."

Full pricing: [agentlensapi.io/pricing](https://agentlensapi.io/pricing)

---

#### 🎥 Unlock video summarization (TikTok, YouTube, and other videos without subtitles)

Two options:

**Option A: Completely free (requires setup)**

Install Whisper locally:

```bash
pip install faster-whisper
# macOS: brew install ffmpeg | Ubuntu: sudo apt install ffmpeg
```

Once installed, tell your agent:

> "I've installed local Whisper, running in CPU mode."

If your current agent supports preference memory and you confirm, your agent can remember your preference. Going forward, when it encounters a video without subtitles, it automatically follows: download → extract audio → transcribe locally → summarize.

> ⚠️ **Hardware notes**: Small models (tiny/base) run on any regular computer; large models (large-v3) are recommended with a GPU. On first use, the model downloads automatically (75MB–3GB).

**Option B: Paid & convenient (recommended for most users)**

Get a Whisper API Key from the [OpenAI platform](https://platform.openai.com/api-keys) and tell your agent:

> "Here's my OpenAI API Key: [YOUR_KEY]"

If your current agent supports preference memory and you confirm, your agent can remember your preference. Going forward, it automatically calls the API for any subtitle-free video.

> 💡 **Low cost**: ~$0.006/minute. A 1-minute TikTok costs ~$0.006; a 10-minute YouTube video costs ~$0.06.

---

#### 📁 Connect your knowledge base (Notion / Obsidian / ima)

The first time you say "save to Notion", "save to Obsidian", or "save to ima", your agent walks you through a one-time setup:

- **Notion**: requires an Integration Token and a Database ID or Page ID; use platform secret storage or environment variables when possible, and use local plaintext config only if you approve it
  💡 The default save script assumes your Notion database has a Title property named **Name** and a URL property named **Source**. If your database uses different property names or you want to save to a single page instead of a database, let your agent know during the first save.
- **Obsidian**: requires your local vault path
- **ima**: requires Client ID + API Key (scan QR code at ima.qq.com/agent-interface); ima is Tencent's knowledge base product, accessible from WeChat, Feishu, and WeCom

**ima — three access scenarios:**

| Scenario | Description |
|:---------|:-----------|
| Running inside ima directly | Zero config; use built-in ima skills |
| Running in WorkBuddy | One-time setup: Client ID + API Key |
| Running in another Agent (OpenClaw / Claude Code etc.) | One-time setup: Client ID + API Key + Knowledge Base ID |

For social links (Douyin/Xiaohongshu/X etc.), Markdown upload is recommended — content persists even if the original link goes dead. For regular web pages, URL import works fine.

Once configured in the same runtime environment, setup is typically one-time only.

---

### Step 4: Use natural, explicit requests

After setup, just ask for the specific action you want:

- "Show me what this tweet says"
- "Summarize this Xiaohongshu post"
- "Save this to Notion"
- "Save this to ima"

After the first successful public social-media read, the agent may ask whether Agent-Social-Reader should be remembered as the preferred workflow for public social-media links in that runtime. This is scoped to social post/video reading and summarization; it does not apply to unrelated files, private content, general browsing, or saving.

Saving happens only when you ask to save the current item.

## 👍🏻 My Daily Workflow

```
I share a link → Agent reads → Agent summarizes → I say "save to Notion" → it's in Notion
```

Content saved to Notion/Obsidian/ima includes:

- Original link
- Full text
- AI summary

Easy to search and review later.

---

## 💰 Pricing (Fully Transparent)

Per Skill marketplace guidelines, paid services require transparent pricing disclosure:

### Completely free features

- ✅ General web pages (r.jina.ai)
- ✅ Single public X/Twitter posts (FxTwitter API)
- ✅ YouTube videos with subtitles (youtube-transcript-api)
- ✅ Weibo (r.jina.ai)
- ✅ WeChat public accounts (Camoufox)
- ✅ RSS feeds (feedparser)
- ✅ Full-web search (Agent runtime built-in search)
- ✅ Notion/Obsidian/ima archiving
- ✅ Local Whisper video transcription (requires your own installation)

### Optional paid features

#### 📱 AgentLens API (20+ social platform reading)

| Plan | Requests/month | Price |
| :--- | :--- | :--- |
| Free | 20 | $0 |
| Basic | 200 | $2.90/month |
| Ultra | 500 | $5.90/month |
| Mega | 1,000 | $9.90/month |

Full pricing: [agentlensapi.io/pricing](https://agentlensapi.io/pricing)

Why AgentLens (from my own experience):

- One API key for 20+ platforms (vs one tool per platform)
- No cookie required (vs risking account suspension)
- No proxy required (vs maintaining your own IP pool)
- Stable maintenance (vs tracking platform rule changes yourself)

For me, $2.90/month (200 requests, enough for a month) is excellent value for the peace of mind it brings.

---

#### 🎥 OpenAI Whisper API (video transcription)

- **Price**: ~$0.006/minute
- **Examples**:
  - 1-minute TikTok: $0.006
  - 10-minute YouTube: $0.06
  - 30-minute podcast: $0.18

Full pricing: [OpenAI Pricing — Whisper](https://platform.openai.com/docs/pricing)

> 💡 If your machine has sufficient resources and you don't mind the setup, you can install Whisper locally (`pip install faster-whisper`) for zero cost.

---

## 💡 Design Philosophy

**Focus on completing the "read → summarize → archive" loop.**

Within this loop:

### Read layer (free-first)

| Content source | Tool | Cost |
| :--- | :--- | :--- |
| General web pages | Jina Reader | ✅ Free |
| Public X/Twitter posts | FxTwitter API | ✅ Free |
| YouTube subtitles | youtube-transcript-api | ✅ Free |
| Weibo | r.jina.ai | ✅ Free |
| WeChat public accounts | Camoufox | ✅ Free |
| RSS feeds | feedparser | ✅ Free |
| 20+ social platforms | AgentLens API | 💵 Optional |

🔐 **Core advantage**: No social account login / no cookie used.
The underlying layer never requires you to log into any personal social account, enter a password, or provide a cookie — so platforms cannot trace activity back to your personal account, reducing the risk of suspension from using personal account cookies.

---

### Summarize layer (LLM calls)

| Content type | Method |
| :--- | :--- |
| Text, images | LLM summarizes directly |
| YouTube with subtitles | Subtitle text → LLM summarizes |
| Videos without subtitles | Audio transcription (✅ free locally, or 💵 optional paid API) → LLM summarizes |

---

### Archive layer (completely free)

Notion, Obsidian, and ima are all free. Tell your agent "save this to Notion", "save this to Obsidian", or "save this to ima" for the current item. The agent walks you through one-time destination setup when needed, then confirms the target before writing.

Archived content includes:

- Original link
- Full text
- AI summary

ima is Tencent's knowledge base product: once configured, your archive is accessible across WeChat, Feishu, and WeCom. For social links, Markdown upload is recommended — content is saved directly and doesn't depend on the original link remaining accessible.

---

## 🔒 Security & Privacy

- **Account safety (no login required)**: Many solutions require browser extensions or cookie exports to fetch content. This Skill never asks you to log into any personal social account or provide a cookie, which reduces the risk of suspension from cookie-based access.
- **Credential handling**: Prefer your agent platform's secret storage or environment variables for API keys and tokens. Local plaintext config (`~/.agent-social-reader/config.json`) is used only if you explicitly approve that tradeoff.
- **Service boundaries**: The agent calls only the service needed for the current request. AgentLens receives a URL only when AgentLens is needed for reading; OpenAI receives audio only if you choose OpenAI Whisper transcription; Notion or ima receive archive content only when you ask to save the current item. Obsidian writes to your local vault path.
- **Per-item save boundary**: Each archive write requires an explicit current request or confirmation of the destination.
- **Scoped reading preference**: If you ask the agent to remember Agent-Social-Reader as the preferred workflow, that preference is limited to public social-media link reading/summarization in the current runtime. It does not enable saving or unrelated browsing.

---

## 🛠️ Tech Stack

<details>
<summary>👀 Click to expand tech stack</summary>

**Free open-source tools and parsers:**
- [Jina Reader](https://jina.ai/reader) — general web page content extraction
- [FxTwitter API](https://github.com/FixTweet/FxTwitter) — public X/Twitter post parsing
- [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) — YouTube subtitle extraction
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — video download fallback (used when curl fails to extract video for transcription)
- [Jina Reader](https://r.jina.ai) — Weibo content extraction
- [Camoufox](https://github.com/daijro/camoufox) — WeChat public account dynamic rendering and reading
- Agent runtime built-in search — full-web semantic search (no extra dependencies)
- Python `feedparser` — RSS feed parsing

**Third-party optional APIs (user chooses as needed):**
- [AgentLens API](https://agentlensapi.io) — unified entry for 20+ social media platform public content
- [OpenAI Whisper API](https://platform.openai.com/docs/guides/speech-to-text) — cloud audio/video high-precision transcription

**Local processing (completely free):**
- [faster-whisper](https://github.com/SYSTRAN/faster-whisper) — locally running Whisper speech-to-text engine

</details>

---

## 🙏 Final Words

This is the first time I've published a Skill publicly.

If something doesn't work, open an issue and I'll fix it right away.

If I find a new tool or solution, I'll add it right away.

If you want a platform added, submit a PR.

If this Skill helps streamline your agent's social media reading and archiving workflow, please give it a ⭐ **Star**!

---

**MIT License**
