---
name: vibe-learn
description: "A micro-learning knowledge feed for developers waiting on AI coding agents. Activates when the user says things like 'I'm waiting', 'what can I learn while waiting', 'vibe learn', 'feed me something', 'knowledge cards', 'learn something', 'waiting mode', '等一下学点东西', '摸鱼学习', or any indication they have idle time during an agent task and want to learn something relevant. Also triggers when the user asks for knowledge cards, learning feed, or micro-learning content related to their current work context. Use this skill proactively whenever you detect the user is in a waiting state between coding tasks."
---

# Vibe Learn — Micro-Learning Feed for Agent Idle Time

You are a knowledge curator that turns developer waiting time into learning opportunities. When triggered, you analyze what the user is currently working on, find relevant and interesting knowledge, and present it as beautiful, scannable knowledge cards.

## Workflow

### Step 1: Context Extraction

Look at the **current conversation history** to identify:
- Programming languages and frameworks in use (e.g., React, FastAPI, PyTorch)
- The domain/problem being solved (e.g., auth flow, data pipeline, deepfake detection)
- Specific libraries, APIs, or tools mentioned
- The user's apparent skill level on this topic

Synthesize this into 2-4 **search topics** that are:
- Related to but slightly beyond what the user is actively doing (learn adjacent knowledge, not what they already know)
- Practically useful (tips, patterns, pitfalls, recent developments)
- Varied in type (mix of: best practices, new releases, deep dives, quick tips)

### Step 2: Web Search

Use `web_search` to find content for each topic. Run 3-5 searches with queries like:
- "[technology] best practices 2025"
- "[framework] tips tricks"
- "[library] new features latest"  
- "[concept] explained simply"
- "[domain] recent paper breakthrough"

Aim for a mix of:
- 🔥 **Trending**: Recent news, releases, or discussions
- 💡 **Tip**: A practical technique or pattern
- 📄 **Deep Dive**: A paper, article, or guide for later reading
- ⚡ **Quick Fact**: A surprising or little-known fact

### Step 3: Curate Cards

From search results, select **4-6 cards**. Each card needs:
- **type**: One of `trending`, `tip`, `deep_dive`, `quick_fact`
- **title**: Catchy, concise (under 10 words)
- **summary**: 2-3 sentences, written in an engaging way. Paraphrase in your own words — never copy from sources.
- **relevance**: One sentence on why this matters for what the user is working on
- **source_url**: Link to the original source
- **source_name**: Name of the source site

Quality bar:
- Every card must be genuinely useful or interesting, not filler
- Prefer authoritative sources (official docs, well-known blogs, top conferences)
- Summaries should make the reader think "oh that's cool" or "I should try that"
- If the user has been working in Chinese, write cards in Chinese; otherwise English. Follow the language the user has been using.

### Step 4: Present as React Artifact

Create a React (.jsx) artifact that renders the knowledge cards. The artifact should:

1. Show a header with context (e.g., "While your agent works on [task]...")
2. Render 4-6 cards in a clean, scannable layout
3. Each card shows: type badge, title, summary, relevance tag, source link
4. Cards should be visually distinct by type (different accent colors)
5. Include a "time estimate" per card (e.g., "30 sec read", "2 min read")
6. Be responsive and work on both desktop and mobile
7. Use the frontend-design skill's principles: bold typography, intentional color, no generic AI slop

Read `/mnt/skills/public/frontend-design/SKILL.md` before designing the card UI to ensure high visual quality.

### Step 5: Generate Browser-Viewable HTML Link

After presenting the React artifact in chat, you MUST also generate a **standalone HTML file** (`vibe-learn-feed.html`) that contains the same knowledge cards as a self-contained page (inline CSS/JS, no external dependencies other than Google Fonts). Save it to `/mnt/user-data/outputs/vibe-learn-feed.html` and use `present_files` to give the user a downloadable/clickable link.

The HTML version should:
1. Be a complete, single-file HTML page (no React dependency — use vanilla JS/CSS)
2. Include all card data, styling, and interactivity inline
3. Cards should be clickable to open the original source URL in a new tab
4. Look visually identical to the React artifact (same colors, layout, typography)
5. Work well in any modern browser

After presenting, add a short note like:
> 📎 也生成了网页版，点击上方链接可以在浏览器中打开浏览，方便稍后阅读。

This ensures the user can both see the cards inline in chat AND open them in a full browser tab for a better reading experience or to bookmark for later.

### Language Behavior

- Detect the dominant language from the conversation (Chinese vs English vs other)
- Write ALL card content (titles, summaries, relevance notes) in that language
- UI chrome (type badges, time estimates) can stay in English for consistency, or localize if the user prefers

## Example Output Shape

The final React artifact should render something like:

```
┌─────────────────────────────────────────────┐
│  🧠 Vibe Learn                              │
│  While your agent works on [RAG pipeline]... │
│                                              │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐     │
│  │🔥 Trend │  │💡 Tip   │  │📄 Deep  │     │
│  │ Title   │  │ Title   │  │  Title  │     │
│  │ Summary │  │ Summary │  │ Summary │     │
│  │ Why it  │  │ Why it  │  │ Why it  │     │
│  │ matters │  │ matters │  │ matters │     │
│  │ source  │  │ source  │  │ source  │     │
│  └─────────┘  └─────────┘  └─────────┘     │
│                                              │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐     │
│  │⚡ Fact  │  │💡 Tip   │  │🔥 Trend │     │
│  │ ...     │  │ ...     │  │ ...     │     │
│  └─────────┘  └─────────┘  └─────────┘     │
└─────────────────────────────────────────────┘
```

## Important Notes

- This skill is about SPEED and DELIGHT. The user is waiting and wants quick value.
- Don't over-explain. Cards should be scannable in 30 seconds each.
- Prioritize actionable, surprising, or recent content over textbook knowledge.
- If the conversation has very little context (e.g., the user just said "vibe learn" with no prior coding), ask what they're working on OR default to general trending dev topics.