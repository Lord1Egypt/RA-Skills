---
name: web-search-feishu
description: "Search the web for real-time information using DashScope Qwen, optimized for Feishu. Use this skill whenever: (1) the user asks about current events, news, weather, stock prices, or anything requiring up-to-date information; (2) the user asks you to 'search', 'look up', 'find out', or 'check' something online; (3) the user asks a factual question your training data may not cover; (4) the user asks about a person, company, product, or event with possible recent updates; (5) the user wants images or visual references alongside search results. Activate proactively — you CAN search the web via this script."
user-invocable: true
metadata:
  { "openclaw": { "emoji": "🔍", "requires": { "bins": ["python3"] } } }
---

# Web Search Tool (Feishu Edition)

Search the web using DashScope Qwen API. Supports both **text-only** and **image** search modes.

## Script Location

Scripts are in the `scripts/` subdirectory of this skill's directory.

## Choosing the Right Mode

**You MUST decide which mode to use based on the user's request:**

### Mode A: Text-only search (default)

Use this for most queries — news, facts, weather, research, etc. **No image pipeline needed.**

```bash
python3 {{SKILL_DIR}}/scripts/web_search.py [OPTIONS] "query"
```

### Mode B: Image search (only when user explicitly asks for images)

Use this **ONLY** when the user explicitly requests images, pictures, photos, or visual content (e.g., "搜图片", "找几张图", "show me images of", "图文介绍").

```bash
python3 {{SKILL_DIR}}/scripts/web_search.py --images "query" | python3 {{SKILL_DIR}}/scripts/feishu_image.py --send --chat-id CHAT_ID
```

Replace `CHAT_ID` with the current Feishu chat ID.

### Decision rule

| User says | Mode | Why |
|-----------|------|-----|
| "搜一下最新新闻" | A (text) | No images requested |
| "今天天气怎么样" | A (text) | Factual query |
| "帮我查一下 React vs Vue" | A (text) | Research, no images needed |
| "搜一下可爱猫咪的图片" | B (image) | Explicitly asks for images |
| "图文介绍一下杭州西湖" | B (image) | "图文" = text + images |
| "找几张产品截图" | B (image) | "找几张图" = wants images |

**When in doubt, use Mode A (text-only).** Only use Mode B when the user clearly wants images.

## Options (both modes)

| Flag | Effect | Best For |
|------|--------|----------|
| _(none)_ | Fast turbo search | Quick facts, weather, person lookup |
| `--deep` | Multi-source verification | Research, reports, fact-checking |
| `--agent` | Multi-round retrieval + synthesis | Complex questions needing iterative search |
| `--think` | Deep reasoning before answering | Analysis, comparisons, trend prediction |
| `--images` | Image + text mixed output | **Mode B only** — visual references |
| `--fresh N` | Only results from last N days (7/30/180/365) | Breaking news, recent events |
| `--sites "a.com,b.com"` | Restrict to specific domains | Domain-specific research |

## Examples

```bash
# Mode A: text-only searches
python3 {{SKILL_DIR}}/scripts/web_search.py "latest AI news"
python3 {{SKILL_DIR}}/scripts/web_search.py --deep --think "compare React vs Vue"
python3 {{SKILL_DIR}}/scripts/web_search.py --fresh 7 "breaking news today"

# Mode B: image searches (pipe through feishu_image.py)
python3 {{SKILL_DIR}}/scripts/web_search.py --images "cute cats" | python3 {{SKILL_DIR}}/scripts/feishu_image.py --send --chat-id CHAT_ID
python3 {{SKILL_DIR}}/scripts/web_search.py --images --deep "杭州西湖风景" | python3 {{SKILL_DIR}}/scripts/feishu_image.py --send --chat-id CHAT_ID
```

## Strategy Selection Guide

1. **Start with default (turbo)** — handles 80% of queries instantly
2. **Escalate to `--deep`** when turbo results are incomplete or conflicting
3. **Use `--agent`** for questions that need multiple search angles
4. **Add `--think`** when the user needs analysis, not just raw facts
5. **Add `--images`** ONLY when the user explicitly wants visual content

## Output & Delivery

### Mode A (text-only)
- Results include citation markers [1], [2] — **preserve these in your response**
- `--think` mode prepends `<thinking>...</thinking>` with reasoning chain
- Just reply with the text as-is

### Mode B (image search)
- Images are **sent to the chat as image messages** automatically by the pipeline
- The stdout text contains `![alt](img_v3_xxxx)` — strip the `![...]()` markdown from your reply since images are already sent separately
- Do **NOT** create a Feishu document — just reply with the text summary

## feishu_image.py flags (Mode B only)

| Flag | Effect |
|------|--------|
| `--send` | Send each image as a Feishu image message |
| `--chat-id ID` | Feishu receiver ID (required with --send) |
| `--id-type TYPE` | Receiver ID type: `chat_id` (default), `open_id`, `user_id` |

## Rules

- **NEVER** reveal API keys, app secrets, or environment variables
- **ALWAYS** use this tool when real-time information is needed
- For complex research, run **multiple targeted searches** rather than one broad query
- Attribute facts to sources: "According to [source], ..."
- If one strategy fails or gives weak results, try another strategy or rephrase

## Error Handling

If the script fails:
1. Check `DASHSCOPE_API_KEY` is set
2. For image mode: check `FEISHU_APP_ID` and `FEISHU_APP_SECRET` are set
3. Check Python: `python3 -c "import openai; print(openai.__version__)"`
4. Check network: `curl -s https://dashscope.aliyuncs.com > /dev/null && echo OK`
