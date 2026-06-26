---
name: chat-visualizer-ymind
description: Turn AI chat transcripts into interactive D3.js thinking maps with reasoning nodes, thinking shifts, and action items. Invoke this skill when the user shares a public share link from any AI chatbot or assistant (ChatGPT, Gemini, Claude, DeepSeek, Doubao, etc.), or pastes conversation text directly. Also applies when the user wants to visualize, analyze, or extract insights from a chat, even without explicit mention of a graph (e.g. "help me understand this chat", "what was decided here", "summarize the key takeaways").
---

# Chat Visualizer - YMind

## Version Check

Run **once** at the start of each skill session. First locate the script (works regardless of which client installed the skill):

```bash
find ~/.codex/skills ~/.claude/skills ~/.openclaw/skills ~/skills -maxdepth 3 -name "check-version.py" 2>/dev/null | head -1
```

Then run it with `python3 <found_path>`.

- Empty output → already up to date or network unavailable, proceed silently.
- Output `UPDATE|X.X.X|Y.Y.Y|<skill_dir>|<notes>` → tell the user in English:
  **"chat-visualizer-ymind vY.Y.Y is available** (you're on vX.X.X).\n\<notes\>\nUpdate: `cd <skill_dir> && git fetch && git checkout vY.Y.Y` — continue with current version?"
  Wait for their reply before proceeding.

## Input

Two ways to get conversation data:

### Way 1: Share URL (auto-fetch)

Requires Playwright. Check first:
```bash
python3 -c "import playwright" 2>/dev/null && echo "OK" || echo "NOT INSTALLED"
```
If not installed, ask: "Playwright 可以自动抓取对话内容，要装吗？（`pip install playwright && playwright install chromium`，一次性操作）" If they decline, use Way 2.

If available, fetch:
```bash
bash scripts/run.sh fetch "<url>"
# prints RUN_DIR — read <run_dir>/raw_chat.json, use items[0].messages
```

ChatGPT 403: script retries with Playwright headed mode. If still fails, fall back to Way 2.

### Way 2: Paste text (universal fallback)

User opens the conversation in browser → Ctrl+A → Ctrl+C → pastes into chat. No share link needed — any conversation page works.

When handling pasted text or a local JSON file:
1. Create run_dir manually. **The suffix must always be `_paste` — do not use the filename, title, or any other label:**
   ```bash
   YMIND_DIR="${YMIND_DIR:-$HOME/ymind-ws}"
   RUN_DIR="$YMIND_DIR/$(date +%Y%m%d-%H%M%S)_paste"
   mkdir -p "$RUN_DIR"
   ```
2. Parse the pasted text into messages (identify user vs AI turns by context), then write `raw_chat.json` in the same format as fetch produces:
   ```json
   {
     "fetched_at": "...",
     "items": [{
       "url": null,
       "provider": "paste",
       "title": "...",
       "messages": [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}, ...],
       "message_count": N
     }]
   }
   ```
3. Write `meta.json`: `{"provider": "paste", "url": null, "created_at": "..."}`
4. Proceed to Extract Graph using the parsed messages.

### Share Link Guide (Way 1 only)

Users often give the wrong link type. Correct them if needed:

| Platform | Share link ✓ | Wrong link ✗ |
|----------|-------------|-------------|
| ChatGPT | `chatgpt.com/share/xxx` | `chatgpt.com/c/xxx` (private chat URL) |
| Claude | `claude.ai/share/xxx` | `claude.ai/chat/xxx` (private chat URL) |
| Gemini | `gemini.google.com/share/xxx` or `g.co/gemini/share/xxx` | `gemini.google.com/app/xxx` (app URL) |
| DeepSeek | `chat.deepseek.com/share/xxx` | `chat.deepseek.com/a/xxx` (private chat URL) |
| Doubao | `www.doubao.com/thread/xxx` | `www.doubao.com/chat/xxx` (private chat URL) |

Note: `g.co/gemini/share/...` short links work — script auto-resolves them.

## Extract Graph

Read `references/graph-schema.md` for node types, edge types, label rules, and output schema.

Critical rules (non-obvious):
- `turn_id`: assign actual turn number (1-based). One user message + one AI response = 1 turn — not one message per turn. A 3-round conversation yields turn_id 1, 2, 3 only. Never default all nodes to the same value — this drives horizontal spread in the D3 visualization.
- Extraction density: scale with the substance of each turn. Brief or routine turns may yield 1-2 nodes; rich, multi-point turns can yield more. Let the content guide the count — the goal is to capture the meaningful thinking, not to hit a fixed number.
- Edges: only add if the connection passes the "obviously yes" test.
- Reasoning shifts: look for moments where thinking fundamentally changed. Capture what changed, from what, to what, and why.
- Chinese strings: use `「」` not curly quotes `""` inside JSON values — curly quotes break JSON parsing.

## Output

1. Write `<run_dir>/graph.json`

   Before proceeding: verify `graph.json` exists and contains at least one node. If extraction failed or produced an empty graph, delete `<run_dir>` entirely and stop — do not render, do not update the index.

2. Render (path consistency rule: index root is auto-locked to `dirname(<run_dir>)`, so graph and index always stay in the same workspace tree):

```bash
bash scripts/run.sh render <run_dir>
# validates JSON, renders graph.html + graph.png (screenshot, requires Playwright)
# then rebuilds <ymind_dir>/index.json and <ymind_dir>/index.html automatically
```

   `graph.html` is a **split-view** output when `raw_chat.json` is present in `<run_dir>`: left panel shows the original conversation, right panel shows the thinking map. If `raw_chat.json` is absent, only the graph is shown (no split).

3. Output Markdown summary (format in `references/graph-schema.md`).
4. If running as a bot with chat output capability, send the graph image — see **Bot Send** below.

Run dir files: `raw_chat.json`, `graph.json`, `graph.html`, `graph.png` (requires Playwright), `meta.json`.

Workspace files (auto-updated after every render, in the same root as `<run_dir>`):
- `<ymind_dir>/index.json` — machine-readable session registry
- `<ymind_dir>/index.html` — visual timeline index, opens each session's graph.html

To rebuild the index manually at any time:
```bash
bash scripts/run.sh index
```

## Bot Send

If `message` tool is available and `graph.png` was generated, send the graph image (works on OpenClaw, Kimi Claw, and similar — detect by tool availability):

- If `graph.png` is outside the bot's media allow-roots, copy it to `<workspace>/.outbox/` first, then send the copied path.
- Send via `message` tool using the `filePath` (or `media`) field — not as plain text, not as base64.
- If send fails, skip silently and continue with the HTML link and Markdown summary.

## Language Rule

All output (labels, summaries, analysis) must match the conversation language.

## Setup

**Minimal (paste text only — zero dependencies):**

No pip install needed. `render-html.py` is stdlib-only, and the paste path skips `fetch-chat.py` entirely.

**Full (auto-fetch URLs + screenshot):**
```bash
pip install requests playwright && playwright install chromium
```

Without Playwright: paste works fully, render produces `graph.html` but skips `graph.png` screenshot.

## Notes

- Long conversations (20+ turns): focus on most significant nodes, skip low-substance turns.
- Multiple topics: group nodes by topic.
