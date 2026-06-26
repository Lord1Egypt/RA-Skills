---
name: gbrain-multi-agent-search
description: "Search and manage a local gbrain personal knowledge base (full-text search, semantic search, knowledge graph). Use when searching personal notes, emails, documents, diary entries, or any knowledge stored in gbrain. Triggers: search brain, query brain, find in brain, brain search, gbrain, knowledge base search, personal knowledge, 知识库搜索, 脑库查询, 记忆搜索, 搜索知识库, 查询脑库."
---

# Gbrain Multi-Agent Search

Local knowledge base with full-text search, semantic search, and knowledge graph. Requires [gbrain](https://github.com/nicepkg/gbrain) installed and a brain repo initialized.

## Prerequisites

- gbrain CLI installed (`bun install` in gbrain repo)
- A brain repo with synced markdown content
- Embedding API configured (OpenAI-compatible endpoint)

## Configuration / 配置

Set these variables or replace inline:

| Variable | Description | 示例 |
|----------|-------------|------|
| `GBRAIN_DIR` | Path to gbrain source repo | `~/gbrain` |
| `BRAIN_DIR` | Path to brain content repo | `~/brain` |
| `OPENAI_API_KEY` | Embedding API key | `sk-...` |
| `OPENAI_BASE_URL` | Embedding API base URL | `https://api.openai.com/v1` |

### One-liner setup (add to TOOLS.md)

```bash
export GBRAIN_DIR=~/gbrain
export BRAIN_DIR=~/brain
export OPENAI_API_KEY=your-key-here
export OPENAI_BASE_URL=https://api.openai.com/v1
alias gb="cd $GBRAIN_DIR && bun run src/cli.ts"
```

## Search / 搜索

### Keyword search (fast, exact match) / 关键词搜索

```bash
cd $GBRAIN_DIR && bun run src/cli.ts search "<query>" [--limit N]
```

Best for: exact names, terms, file references.
适合：精确的人名、术语、文件名搜索。

### Semantic search (hybrid, understands meaning) / 语义搜索

```bash
cd $GBRAIN_DIR && bun run src/cli.ts query "<question>" [--limit N]
```

Best for: natural language questions, fuzzy concepts, cross-topic queries.
适合：自然语言提问、模糊概念、跨主题查询。

Examples / 示例:
```
query "When did I join company X"        / "什么时候加入的公司X"
query "Heart rate trends in 2024"         / "2024年心率趋势"
query "Email about project approval"      / "项目审批相关的邮件"
```

### List pages / 列出页面

```bash
cd $GBRAIN_DIR && bun run src/cli.ts list [--type source|person|concept|company|project|deal|media|civic] [--tag T] [-n N]
```

### Read a page / 读取页面

```bash
cd $GBRAIN_DIR && bun run src/cli.ts get "<slug>" [--fuzzy]
```

Use `--fuzzy` for approximate slug matching.
使用 `--fuzzy` 进行模糊匹配。

## Knowledge Graph / 知识图谱

### Create link / 创建关联

```bash
cd $GBRAIN_DIR && bun run src/cli.ts link "<from>" "<to>" [--link-type TYPE] [--context "description"]
```

### Traverse graph / 遍历图谱

```bash
cd $GBRAIN_DIR && bun run src/cli.ts graph "<slug>" [--depth N]
```

### Common link types / 常用关联类型

`works_at`, `invested_in`, `related_to`, `wrote`, `attended`, `located_in`, `managed`, `friend_of`, `reported_to`, `parent_of`, `spouse_of`

## Data Management / 数据管理

### Import & embed / 导入与嵌入

```bash
# Sync markdown files from repo to brain
cd $GBRAIN_DIR && bun run src/cli.ts sync --repo $BRAIN_DIR --no-pull --no-embed --full

# Generate embeddings for new/changed content
cd $GBRAIN_DIR && OPENAI_API_KEY=... OPENAI_BASE_URL=... bun run src/cli.ts embed --stale
```

### Statistics / 统计信息

```bash
cd $GBRAIN_DIR && bun run src/cli.ts stats
```

### Health check / 健康检查

```bash
cd $GBRAIN_DIR && bun run src/cli.ts doctor
```

## Workflow / 工作流程

### Adding new content / 添加新内容

1. Add markdown files to `$BRAIN_DIR/sources/<category>/`
2. `git add && git commit`
3. Run `sync --full --no-pull --no-embed`
4. Run `embed --stale`

### Typical search pattern / 典型搜索模式

1. Start with `search` for exact matches
2. If no results or need deeper understanding, use `query`
3. Use `get <slug>` to read full page content
4. Use `graph <slug>` to explore related pages

## Tips / 提示

- `search` is faster, `query` is smarter — use `search` first / `search` 更快，`query` 更智能
- Add `--limit 5` for concise results / 加 `--limit 5` 获取简洁结果
- Use `--fuzzy` when unsure of exact slug / 不确定 slug 时用 `--fuzzy`
- For embedding issues with large files (>64 chunks), split into smaller files / 大文件嵌入失败时，拆分为小文件
- Run `stats` periodically to check brain health / 定期运行 `stats` 检查知识库状态
