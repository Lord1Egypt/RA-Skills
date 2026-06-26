---
name: bigmodel-web-search-fallback
description: Use Zhipu / BigModel web search as a non-invasive fallback when the built-in web_search route is unavailable, failing, or the user explicitly wants 智谱 / BigModel / GLM search. Supports both direct structured search results and chat-completions search-with-summary. Supports engine switching across search_std, search_pro, search_pro_sogou, and search_pro_quark.
---

# BigModel Web Search Fallback

Use this skill when you want Zhipu search **without modifying OpenClaw core**.

It provides a local wrapper script with two execution modes:

- `raw` — call Zhipu Web Search API directly and get structured results
- `chat` — call Zhipu chat completions with the built-in `web_search` tool and get a synthesized answer

## Requirements

Make sure the OpenClaw host has one of these environment variables set:

- `ZAI_API_KEY`
- `ZHIPUAI_API_KEY`
- `BIGMODEL_API_KEY`

If none is present, stop and report missing auth instead of retrying blindly.

## Engine selection

This skill supports four Zhipu search engines:

- `search_std` — default, lowest-cost/basic search
- `search_pro` — stronger general search quality
- `search_pro_sogou` — 搜狗-backed route
- `search_pro_quark` — 夸克-backed route

Default to `search_std` unless the user asks for:

- better search quality
- broader retrieval coverage
- a specific upstream engine
- result comparison across engines

When the user explicitly names an engine, honor it.

## Quick decision

- Use `raw` when you want structured results such as title/link/summary/media/date and you will write the final answer yourself.
- Use `chat` when you want GLM to search and summarize in one call.
- Use `search_std` first for routine lookups.
- Switch to `search_pro` when quality matters more than cost.
- Switch to `search_pro_sogou` or `search_pro_quark` when the user wants to test or compare engines.

## Commands

Run commands from the skill directory or use absolute paths.

### Raw structured search

```bash
python scripts/zhipu_web_search.py raw --query "OpenClaw 是什么" --engine search_std --count 5 --pretty
```

### Search + answer synthesis

```bash
python scripts/zhipu_web_search.py chat --query "请简要说明 OpenClaw 是什么，并给出搜索来源。" --engine search_std --count 5 --pretty
```

### Higher-quality search

```bash
python scripts/zhipu_web_search.py raw --query "今天的 AI 新闻" --engine search_pro --count 5 --pretty
```

### Explicit engine comparison

```bash
python scripts/zhipu_web_search.py raw --query "OpenClaw 是什么" --engine search_pro_sogou --count 5 --pretty
python scripts/zhipu_web_search.py raw --query "OpenClaw 是什么" --engine search_pro_quark --count 5 --pretty
```

## Workflow

1. Decide whether the task needs `raw` results or a `chat`-generated answer.
2. Pick the engine:
   - default `search_std`
   - `search_pro` for better quality
   - `search_pro_sogou` / `search_pro_quark` for explicit engine routing or comparison
3. Run the wrapper script.
4. If using `raw`, summarize the returned results yourself and cite the best links.
5. If using `chat`, still sanity-check the answer before sending it.
6. If the user asks how this relates to built-in `web_search`, explain that this is a non-invasive fallback and does not replace OpenClaw core tooling.

## Notes

- The script prints JSON to stdout for easy parsing.
- Supported flags include `--domain-filter`, `--recency`, `--content-size`, `--count`, and `--engine`.
- Read `references/api-notes.md` if you need API details, engine guidance, or more examples.
