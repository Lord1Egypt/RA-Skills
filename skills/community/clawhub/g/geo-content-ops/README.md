# OpenClaw GEO Content Ops

> Languages: [简体中文](README.md) | [English](docs/readme/README_en.md) | [日本語](docs/readme/README_ja.md) | [Español](docs/readme/README_es.md) | [Русский](docs/readme/README_ru.md) | [Português (BR)](docs/readme/README_pt_BR.md)

> OpenClaw GEO Content Ops 是一个面向 GEO（生成式引擎优化）的轻量级 Skill 与内容运营模型。它把可信知识源、topic clusters、内容任务、AI Search 写作、SEO/GEO 工作流 receipts、发布目标、LLM 友好 artifacts 和可见度 analytics 串成一条可审计的内容资产链路。

[![Skill](https://img.shields.io/badge/OpenClaw-Skill-0F766E)](#快速开始)
[![GEO](https://img.shields.io/badge/GEO-Content%20Ops-blue)](#你可以用它做什么)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

OpenClaw GEO Content Ops 以 [MIT License](LICENSE) 开源发布。你可以自由使用、复制、修改和分发本项目，包括商业使用；请保留版权声明和许可证文本。

---

## 你可以用它做什么

| 层级 | 说明 |
| --- | --- |
| 知识源目录 | 管理品牌文档、产品事实、receipts、URL、客户问题、竞品记录和 wiki 页面 |
| Topic clusters | 沉淀问题、关键词、实体、对比角度和 FAQ 地图 |
| 内容任务 | 把读者、核心问题、source evidence、发布范围和成功信号串成任务 brief |
| 写作协同 | 与 AI Search writer 分工，保证单篇内容 answer-first、可引用、可抽取 |
| SEO/GEO 工作流 | 与 Hunter/Tony/Peter daily workflow、发布门禁和 receipts 分工 |
| 发布目标 | 支持 ClawLite blog、WordPress REST、静态 GEO site、X posts、Feishu docs 和后续 provider |
| GEO artifacts | 管理 `llms.txt`、sitemap、TXT map、Schema、Open Graph、canonical URL 和证据块 |
| Receipts | 保存生成、审核、发布、部署、live QA、patrol、analytics 的 durable evidence |
| 可见度分析 | 追踪 AI crawler hits、indexing、sitemap coverage、AI citation checks、top content 和 rescue tasks |

---

## 为什么需要它

很多 SEO/GEO 系统把三件事混在一起：找资料、写内容、证明发布。结果就是“多写文章”，但没有可信来源、没有发布证据，也没有反馈回流。

OpenClaw GEO Content Ops 把三层分开：

1. **内容运营层**：决定 sources、topics、tasks、targets、artifacts、receipts 和 analytics。
2. **每日执行层**：由 `openclaw-seo-geo-workflow` 执行 Hunter/Tony/Peter 生产、发布、QA 和 patrol。
3. **单篇写作层**：由 `ai-search-visibility-content-writing` 保证内容清晰、可抽取、可引用。

这个 repo 是运营层，不替代写作 skill，也不替代发布 workflow。

---

## 运行结构

```text
knowledge_sources
    ↓
topic_clusters
    ↓
content_tasks
    ↓
AI-search content writing
    ↓
SEO/GEO workflow receipts
    ↓
publication_targets
    ↓
GEO artifacts
    ↓
visibility analytics
    ↓
source/wiki promotion
```

---

## 系统架构

| 组件 | 作用 | 示例 |
| --- | --- | --- |
| `knowledge_sources` | 证据与来源索引 | `catalogs/sources.jsonl` |
| `clawlite-brain/wiki` | 长期项目知识层 | topic/entity/synthesis pages |
| `synthadoc/wiki` | 可读的生成式导航与 topic 页面 | brand hub、keyword map、Hunter pages |
| `topic_clusters` | 内容战略层 | keywords、questions、comparison pages |
| `content_tasks` | 执行 brief 层 | reader、query、answer、source IDs |
| `openclaw-seo-geo-workflow` | 每日交付控制器 | Hunter/Tony/Peter receipts |
| `ai-search-visibility-content-writing` | 单篇写作层 | answer-first body、metadata、schema hints |
| `publication_targets` | 分发层 | ClawLite blog、WordPress、static site、X |
| `geo_artifacts` | LLM/search 可读输出 | `llms.txt`、sitemap、Schema、TXT map |
| `visibility_signals` | 监控层 | crawler logs、indexing、AI citations |

---

## 与现有 Skill 如何协同

| Skill | 负责 | 不负责 |
| --- | --- | --- |
| `openclaw-geo-content-ops` | sources、topics、tasks、targets、artifacts、receipts、analytics | 单篇正文写作或无证据的 live publish claim |
| `openclaw-seo-geo-workflow` | Hunter/Tony/Peter daily execution、publish gates、receipts、patrol | 长期 source catalog governance |
| `ai-search-visibility-content-writing` | 单篇内容质量、直接答案、实体清晰、可引用结构 | 选题发现、部署、analytics |
| `claw-wiki` | 从 canonical source 生成可读 wiki 页面 | 原始来源注册和发布状态判断 |

推荐顺序：

1. 用 `openclaw-geo-content-ops` 选择 sources、clusters、tasks、targets 和 success signals。
2. 用 `openclaw-seo-geo-workflow` 跑或审查 daily production 与 publish evidence。
3. 用 `ai-search-visibility-content-writing` 写或改单篇内容。
4. 再用 `openclaw-geo-content-ops` 把 validated findings 回流到 source catalog、wiki、rescue tasks 和 analytics。

---

## 快速开始

### 安装为 Codex Skill

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/X-RayLuan/openclaw-geo-content-ops.git ~/.codex/skills/openclaw-geo-content-ops
```

### 安装为 OpenClaw Workspace Skill

```bash
mkdir -p ~/.openclaw/workspace/skills
git clone https://github.com/X-RayLuan/openclaw-geo-content-ops.git ~/.openclaw/workspace/skills/openclaw-geo-content-ops
```

### 使用方式

```text
Use openclaw-geo-content-ops to design this week's GEO content operating plan.
```

```text
Use openclaw-geo-content-ops to audit whether today's SEO/GEO workflow promoted the right findings back into sources and wiki.
```

---

## Source Catalog

Source catalog 是 JSONL 证据索引。每一行是一个 source：

```json
{
  "id": "clawlite-positioning",
  "type": "brand_doc",
  "title": "ClawLite Positioning",
  "path": "references/clawlite-brand/positioning.md",
  "trustLevel": "owned",
  "capturedAt": "2026-05-24T00:00:00+08:00",
  "summary": "Canonical positioning source for ClawLite.",
  "entities": ["ClawLite", "OpenClaw"],
  "usableFor": ["brand-positioning", "comparison-pages"]
}
```

参考：`examples/sources.example.jsonl`

---

## Task Brief

每个 GEO content task 都应该把 source evidence 和 publish target 连起来：

```json
{
  "taskId": "geo-2026-05-24-openclaw-routing-cost-control",
  "status": "planned",
  "targetReader": "AI team operator",
  "coreQuery": "How can teams control OpenClaw routing cost without losing reliability?",
  "primaryAnswer": "Use a verified routing policy, receipts, and rollback gates instead of manual model switching.",
  "requiredSources": ["clawlite-positioning", "clawlite-topic-clusters"],
  "entities": ["OpenClaw", "ClawLite"],
  "topicCluster": "routing-cost-control",
  "publishScope": ["clawlite_blog", "x_post"],
  "geoArtifacts": ["schema", "sitemap", "llms_txt"],
  "successSignals": ["live_url", "index_check", "ai_crawler_log"]
}
```

参考：`examples/task.example.json`

---

## Receipt Contract

没有 evidence，就不要声明生产发布、索引、AI crawler visits、排名或 AI citation。

```json
{
  "date": "2026-05-24",
  "taskId": "geo-2026-05-24-openclaw-routing-cost-control",
  "stage": "publish",
  "target": "clawlite_blog",
  "status": "PASS",
  "evidence": {
    "localPath": "delivery/seo-geo/2026-05-24/manifest.json",
    "liveUrl": "https://clawlite.ai/blog/openclaw-routing-cost-control",
    "checkedAt": "2026-05-24T10:00:00+08:00"
  },
  "warnings": [],
  "nextActions": []
}
```

参考：`examples/receipt.example.json`

---

## GEO Artifact Checklist

公开 web target 应检查：

- canonical URL 和稳定 slug
- title 和 meta description
- Open Graph / Twitter metadata
- Article、FAQ、HowTo 或 Organization Schema
- sitemap inclusion
- `llms.txt` 或 AI-readable site map inclusion
- TXT map 或 Markdown hub index
- 相关 cluster 页面的 internal links
- 需要 grounding 的 source/evidence block
- evergreen 页面更新时间

---

## 从 GEOFlow 借鉴了什么

这个 repo 参考了 GEOFlow 的架构思想，但没有引入它的 Laravel CMS stack。

借鉴点：

- generation 之前先建设 source/material library
- task queue state machine
- local publish 与 remote distribution 分离
- target-site Agent / WordPress provider abstraction
- `llms.txt`、sitemap、TXT map、Schema 输出
- access-log 和 AI-crawler analytics

---

## 仓库结构

```text
.
├── SKILL.md
├── README.md
├── LICENSE
├── agents/
│   └── openai.yaml
├── docs/readme/
│   ├── README_en.md
│   ├── README_ja.md
│   ├── README_es.md
│   ├── README_ru.md
│   └── README_pt_BR.md
├── examples/
│   ├── receipt.example.json
│   ├── sources.example.jsonl
│   └── task.example.json
└── references/
    ├── geoflow-patterns.md
    └── openclaw-integration.md
```

---

## 推荐运营节奏

Daily:

1. 先读 workflow receipts，再判断状态。
2. 只把 validated findings 推进 source catalog 或 topic clusters。
3. 对 publish、live QA、patrol 失败项创建 rescue tasks。

Weekly:

1. Review source catalog quality。
2. 把重复问题合并进 topic clusters。
3. 刷新 wiki pages。
4. 检查 visibility analytics。
5. 决定哪些强内容要派生 X posts 或 internal links。
