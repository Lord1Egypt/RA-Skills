---
name: auto-deep-research
description: 深度研究技能。用于深入调查、验证信息、研究主题。当用户需要调研概念、对比工具、追踪事件、分析趋势时使用。通过拆分问题、多次搜索、多源验证，输出结构化报告。确保每个结论有多个独立来源，不确定点要标注。
---

# Auto Deep Research

自动深度研究技能。

## 核心逻辑

```
loop (1 轮 = 并行 search 所有待处理子问题):
  1. 动态拆解子问题（初始 3 个，可临时追加）
  2. 并行 search 所有待处理子问题
  3. 串行 read_page + 提炼，写入 memo（防爆）
  4. 合并去重
  5. 评估：弹药够不够？有没有决定性新概念影响最初结论不清晰需要继续研究？

退出条件：
  - 所有子问题已完成 AND 弹药够 OR
  - 达到 max_iterations（默认 5 轮）
```

### 当前支持模式

**简单模式（默认）**：
- 初始子问题数量 = 3
- max_iterations = 5
- 追加子问题需"决定性影响"或针对原始问题还有明显盲点
- 强制合并去重


### 动态拆解
- 初始生成 3 个子问题（默认）
- **Update 阶段可以临时追加新子问题**：如果子问题 1 的结果揭示了一个全新的关键概念，如果与原始问题高度相关，则加入任务队列
- 子问题用标记状态：`[待处理]` / `[处理中]` / `[已完成]`

## 输出目录

每次研究创建一个独立文件夹 `output/{研究主题slug}/`：

```
output/
└── {topic-slug}/
    ├── state.json      # 执行状态（轮数、子问题进度）
    ├── memo.json       # 结构化研究笔记（JSON，方便 agent 读取判断）
    ├── sources.json    # 所有来源 URL 和摘要
    └── report.md       # 最终报告
```

**文件夹命名规则**：用主题关键词 + 短时间戳，如 `react-server-components_20240331`

### state.json

```json
{
  "iteration": 1,
  "max_iterations": 5,
  "original_query": "用户问题",
  "subproblems": [
    {"id": 1, "title": "子问题1", "status": "completed", "sources": 2},
    {"id": 2, "title": "子问题2", "status": "processing", "sources": 1},
    {"id": 3, "title": "子问题3", "status": "pending", "sources": 0}
  ],
  "has_new_concepts": false,
  "enough_evidence": false
}
```

### memo.json

```json
{
  "subproblems": [
    {
      "id": 1,
      "title": "子问题标题",
      "findings": [
        {"source": "URL", "priority": "P1", "key_points": ["点1", "点2"], "conflict": null},
        {"source": "URL", "priority": "P4", "key_points": ["点1"], "conflict": "与来源A冲突"}
      ]
    }
  ],
  "new_concepts": ["概念A", "概念B"],
  "uncertain_points": ["争议点1"]
}
```

### sources.json

```json
{
  "sources": [
    {"url": "URL", "title": "标题", "priority": "P1", "added_at": "2024-01-01"}
  ]
}
```

## 工具

**推荐使用脚本**（见 `scripts/` 目录）：
- `search.sh <query> [max_results] [output_file]`
- `read_page.sh <url> [output_file]`

### 环境配置

在系统环境变量或 `.env` 文件中配置：

```bash
# 搜索 API（选一个）
export TAVILY_API_KEY="your-key-here"  # https://tavily.com 获取
# DuckDuckGo 免费，无需配置

# 页面读取 API
export JINA_API_KEY="your-key-here"  # https://jina.ai/reader 获取
```

### search(query)
联网搜索，返回带 URL 和高信息密度摘要的列表。

**脚本调用**：
```bash
./scripts/search.sh "React Server Components" 5
```

**手动调用**：
```bash
# Tavily（需要 API key）
curl "https://api.tavily.com/search" \
  -H "Authorization: Bearer $TAVILY_API_KEY" \
  -d '{"query": "query", "max_results": 5}'

# DuckDuckGo（免费，搜索网页内容）
curl "https://api.duckduckgo.com/?q=query&format=json"
# 如果curl失效，则用 Python duckduckgo-search 库或 SearXNG
```

**并行 search + 串行提炼**：
- 可以并行发起 search 获取多个 URL
- 读取网页并提炼时必须串行，避免上下文错乱

### read_page(url)
深度阅读目标页面，把 HTML 转成干净的 Markdown，剔除广告和导航栏。

**方式1: WebFetch（推荐，无需 API）**：
直接调用 Claude Code 的 WebFetch 工具读取页面

**方式2: 浏览器**：
用浏览器工具打开页面，复制内容

**方式3: Jina Reader（备用）**：
```bash
curl "https://r.jina.ai/readability/page?url=$URL"
```

## 两条铁律

1. **一个结论 ≥ 2 个来源**：不能只信一个来源
2. **必须标注不确定点**：不知道就是不知道

## Memo 格式

每次调用 read_page 后，必须强制提炼关键信息，写入 `memo.json`。

**同时保留 `memo.md`** 方便人类阅读（与 memo.json 内容同步）：

```markdown
## 子问题 1: [标题]

### 来源 A [P1-官方] ([URL])
- 关键点 1
- 关键点 2

### 来源 B [P4-GitHub] ([URL])
- 关键点 1
- ⚠️ 与来源 A 冲突：XXX ???
---
## 子问题 2: [标题]
...
```

### 标记规则
- `[P1-官方]` → 优先级 1，官方文档
- `[P4-GitHub]` → 优先级 4，GitHub
- `???` → 冲突待验证

详见 `references/source-trust.md`

**禁止**：
- 把长篇大论的网页全文直接塞进 memo
- 把 raw HTML 塞进 memo

**路径**：当前目录 `output/memo.json`（同时保留 memo.md 方便人工查看）

## 循环逻辑

### Eval（评估）
判断标准：
1. **弹药够不够**：所有子问题都有 ≥2 个独立来源确认？
2. **有没有新概念**：结果中出现了之前没覆盖的关键概念？

**没有新概念** → 退出
**即使有冲突也退出**（不阻塞），冲突标记为"不确定点"

详见 `references/conflict-detection.md`

### Plan（决策）
- 够了 → 退出循环，去写最终报告
- 不够 → 生成新 query，或者从搜索结果挑一个 URL 继续钻

### Act（执行）
- 调用 search 找新方向
- 或调用 read_page 钻进去看细节

### Update（更新 + 防爆）
1. **合并去重**：新信息写入 memo 时，必须与原有信息合并去重，不是无限往下拼接
2. **临时追加子问题**：当新概念对解答【用户初始核心问题】具有**决定性影响**，且当前 memo 无法解释它时，才允许追加
3. 提炼信息要精简：只保留关键点，禁止长篇大论

回到 Eval

## 最大轮数

**max_iterations = 5**（每次并行 search 一批子问题 = 1 轮，强制中断，防止烧钱）

**计数规则**：
- 1 轮 = 并行 search 所有 [待处理] 子问题
- 1 轮内不限 search 次数
- read_page 不计轮数

## 输出报告格式

**路径**：`output/{topic-slug}/report.md`

必须是 .md 文件：

```markdown
# 研究报告：[用户问题]

## 问题拆解
- 子问题 1: xxx
- 子问题 2: xxx
- 子问题 3: xxx

## 关键结论
### 结论 1
证据：
- [P1-官方] 来源 1: ...
- [P4-GitHub] 来源 2: ...

### 结论 2
...

## 不确定点
- 争议点 1：xxx（来源 A vs 来源 B）
- 未验证点：xxx

## 总结
[用 2-3 句话概括核心发现，一句话回答用户问题]

## 参考来源
1. [P1-官方] [标题] - [URL]
2. [P4-GitHub] [标题] - [URL]
```

## 触发方式

用户输入 `/auto-deep-research` 时触发。

## 完整执行流程

1. **初始化**：
   - 创建文件夹 `output/{topic-slug}/`
   - 初始化 `state.json`（轮数=0，子问题队列=3个待处理）
   - 创建空 `memo.json` 和 `sources.json`

2. **主循环**（最多 5 次 search）：
   - 每轮更新 `state.json` 中的 iteration++
   - 对每个子问题：search → read_page → 提炼写入 memo.json + sources.json
   - Eval：读取 state.json 判断是否继续

3. **退出**：
   - 生成 `output/{topic-slug}/report.md`
   - 保留 JSON 文件供后续 agent 读取

## 使用示例

**用户输入**：
```
/auto-deep-research 解释什么是 React Server Components
```

**执行流程**：
1. 拆成 3 个子问题（标记 [待处理]）
2. 第 1 轮：并行 search 所有待处理子问题
3. 串行 read_page + 提炼，写入 memo
4. Eval：没有决定性新概念？→ 退出
5. 达到 5 轮或所有子问题完成，输出报告