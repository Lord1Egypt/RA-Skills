**English** | [中文](README-zh.md)

# chat-visualizer-ymind

An AI agent skill for OpenClaw, Claude Code, and Codex. Visualize any AI chat conversation into a structured thinking map — extract the reasoning behind decisions, surface friction points, and trace how ideas evolved.

**Philosophy:** Chat is linear. Thinking isn't. AI conversations are dense with insight — but insights scatter across lengthy threads. You forget key breakthroughs, repeat conversations unknowingly, miss the connections. This skill externalizes your thinking: every conversation becomes a navigable graph of what you actually figured out.

## What it does

Share a conversation URL → get an interactive force graph with:
- **Reasoning nodes** — facts, frictions, sparks, and actions extracted from the conversation
- **Thinking shift detection** — where did the conversation turn?
- **Action items** — extracted, prioritized, and grouped by friction context
- **D3.js visualization** — dark-mode interactive graph, shareable as a single HTML file

![Titanic and the Utilitarian Filter](assets/graph-demo.png)

## Quick Start

1. Install the skill (see [Install](#install))
2. Share a conversation URL with your agent:
   ```
   Visualize this: https://chatgpt.com/share/xxx
   ```
3. The agent fetches the conversation, extracts the thinking graph, and renders an HTML file
4. Open `graph.html` — explore nodes, trace action paths, export insights

**Auto-fetch** (share link → agent fetches automatically): ChatGPT, Gemini, Claude, DeepSeek, Doubao.

**Paste** (no share link? Ctrl+A → copy → paste to your agent): works with any AI tool — no URL needed.

Want auto-fetch support for another provider? [Open an issue](https://github.com/yslenjoy/chat-visualizer-ymind/issues).

## Install

### ClawHub

```bash
npx clawhub@latest install chat-visualizer-ymind
```

### Manual Install

#### OpenClaw

```bash
git clone https://github.com/yslenjoy/chat-visualizer-ymind.git ~/.openclaw/skills/chat-visualizer-ymind
```

#### Claude Code

```bash
git clone https://github.com/yslenjoy/chat-visualizer-ymind.git ~/.claude/skills/chat-visualizer-ymind
```

#### Codex

```bash
git clone https://github.com/yslenjoy/chat-visualizer-ymind.git ~/.codex/skills/chat-visualizer-ymind
```

## Output

Results are saved to `~/ymind-ws/` by default (override with `YMIND_DIR`). Each run is a self-contained folder — your personal thinking map library.

```
~/ymind-ws/
  index.html                    ← visual timeline of all sessions
  index.json                    ← machine-readable session registry
  20260319-143021_chatgpt/
    raw_chat.json               ← fetched conversation
    graph.json                  ← extracted thinking graph
    graph.html                  ← D3.js visualization (split view with chat panel if raw_chat.json exists)
    graph.png                   ← screenshot
    meta.json                   ← provider, url, title, created_at
```

## Privacy

- **No cookies stored** — fetching uses requests + Playwright in a fresh context; no session data is cached between runs
- **Everything stays local** — all output is saved to your machine only, nothing is uploaded
- **No external services for data** — all conversation data stays local; the rendered HTML loads fonts and visualization libraries (D3.js, html2canvas) from CDN and requires an internet connection to display correctly
- Conversation URLs are only used to fetch the public share page you provide

## Pipeline

```
Input
  ├─ Share URL   → scripts/run.sh fetch → fetch-chat.py → raw_chat.json
  └─ Paste text  → tell your agent the conversation directly (no fetch needed)
        │
  [LLM] SKILL.md → analyze → graph.json
        │
  scripts/run.sh render → render-html.py → graph.html + graph.png
        │
  (auto) rebuild index.html + index.json  ← your full session library
```

## Dependencies

Requires Python 3.10+.

**Minimal** (paste mode):  — no install needed.

**Full** (auto-fetch URLs + screenshot):
```bash
pip install requests playwright && playwright install chromium
```

## License

MIT
