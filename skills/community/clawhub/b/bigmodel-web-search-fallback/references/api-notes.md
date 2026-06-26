# Zhipu Web Search Notes

## Authentication

Set one of these environment variables on the OpenClaw host:

- `ZAI_API_KEY`
- `ZHIPUAI_API_KEY`
- `BIGMODEL_API_KEY`

The bundled script checks them in that order.

## Supported engines

- `search_std` — default, cheapest/basic search
- `search_pro` — stronger quality, better default upgrade path
- `search_pro_sogou` — 搜狗-backed route
- `search_pro_quark` — 夸克-backed route

## Two execution modes

### 1. Raw search

Use Zhipu's dedicated Web Search API.

Endpoint:

- `POST https://open.bigmodel.cn/api/paas/v4/web_search`

Good for:

- Getting structured search results
- Returning title/link/summary/media/date directly
- Lightweight lookups where the assistant should synthesize the final answer itself
- Comparing different engines side by side

### 2. Chat search

Use chat completions with the `web_search` tool.

Endpoint:

- `POST https://open.bigmodel.cn/api/paas/v4/chat/completions`

Good for:

- Search + answer synthesis in one call
- Letting GLM produce a short answer with sources
- Testing whether different engines affect answer quality

## Recommended defaults

- Default engine: `search_std`
- Default count: `5`
- Default content size: `medium`
- Upgrade to `search_pro` when result quality matters more than cost
- Use `search_pro_sogou` / `search_pro_quark` only when the user explicitly wants those routes or wants comparison tests

## Script examples

### Raw search

```bash
python scripts/zhipu_web_search.py raw --query "OpenClaw 是什么" --engine search_std --count 5 --pretty
```

### Chat search

```bash
python scripts/zhipu_web_search.py chat --query "请简要说明 OpenClaw 是什么，并给出搜索来源。" --engine search_std --count 5 --pretty
```

### Compare engines

```bash
python scripts/zhipu_web_search.py raw --query "OpenClaw 是什么" --engine search_std --count 5 --pretty
python scripts/zhipu_web_search.py raw --query "OpenClaw 是什么" --engine search_pro --count 5 --pretty
python scripts/zhipu_web_search.py raw --query "OpenClaw 是什么" --engine search_pro_sogou --count 5 --pretty
python scripts/zhipu_web_search.py raw --query "OpenClaw 是什么" --engine search_pro_quark --count 5 --pretty
```

### Chat search with custom summarization prompt

```bash
python scripts/zhipu_web_search.py chat \
  --query "总结今天的 AI 新闻" \
  --engine search_std \
  --count 5 \
  --prompt "请基于网络搜索结果给出 3 条要点，并在句末标注来源。"
```
