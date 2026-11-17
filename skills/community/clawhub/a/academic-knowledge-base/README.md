# Academic Knowledge Base (学术知识库) v3.7

> Your research compounds. Not just searches — a personal knowledge hub that grows with every query.

**SkillHub 安装名：** `academic-knowledge-base`
**作者：** @J-levee (张亚东 / Zhang Yadong)
**依赖技能：** global-biblio-base (必需), smartlib-citation-checker (推荐)

---

## 这是什么？ / What is this?

一个**面向学术研究者的个人知识中枢**。让每一次文献检索和研究自动沉淀到私有知识库，形成持续积累的研究资产。

> A personal knowledge hub for academic researchers. Every search and study session compounds into your private knowledge base.

### 一句话说清 / One-liner

> 你说"查 RAG 最新进展" → AI 先搜你的知识库 → 再搜外部补充 → 一键入库。以后你再问，知识库优先回答。

---

## 核心功能 / Core Features

### 4 类数据自动入库

| 数据类型 | 触发方式 | 入库行为 |
|------|------|------|
| SmartLib 检索结果 | "保存到知识库" | 元数据写入 + 摘要自动向量化 + Wiki 概念页更新 |
| 用户上传文献 (PDF/Word/BibTeX) | 提供文件路径 | 解析 → SmartLib 匹配补全字段 → 入库 |
| 资讯/报道 | "保存这篇资讯" | 原文存档 + 元数据标引入库 |
| 个人学术数据 | "记录这些实验数据" | CSV/Excel/笔记入库，可关联到文献 |

### 双轨智能检索

- **BM25 分词匹配**：标题/关键词/摘要倒排索引
- **向量语义检索**：BGE-M3（免费，1024维，中文优化）
- **加权合并**：知识库结果 [📚] 置顶，命中不足时自动扩展外部 SmartLib 检索

### LLM 自动维护 Wiki 知识层

继承自 Karpathy LLM Wiki 模式 — 每次入库 AI 自动创建/更新主题概念页、建立文献交叉引用。

### 研究专题 (Research Sessions)

文献子集 → 智能命名 → 笔记 + AI 分析 → 一键导出 zip 快照。

### 交互式统计报告

说"知识库统计" → 自动生成 HTML 报告：摘要卡片 + 语言饼图 + 年份柱状图 + 标签云。

---

## 💰 变现说明 / Monetization

本技能与 `global-biblio-base` **共享凭证和配额**。首次使用自动检测并复用凭证，共享 100 次/月免费额度。

| 状态 | 展示规则 |
|------|---------|
| 配额充足 | 知识库检索完整展示所有结果 |
| 配额耗尽 | Gateway 返回 429，外部检索、入库匹配等需要调用 SmartLib 的功能**一律拒绝**；知识库本地检索、标签管理、导出等纯本地操作正常 |

每次入库一条文献 = 消耗 1 次配额。回复「充值」获取微信支付码。

---

## 快速开始 / Quick Start

### 1. 安装

在 WorkBuddy 中，SkillHub 搜索 `academic-knowledge-base` → 一键安装。必须同时安装 `global-biblio-base`。

### 2. 第一次使用

**直接开始就行。** 本技能采用懒加载设计：

```
你："帮我查 RAG 技术的文献"
→ AI 自动创建知识库目录 → 用 SmartLib 检索 → 展示结果
你："保存全部"
→ 自动入库 + 去重 + 标签提取 + Wiki 更新 → 完成
```

### 3. (可选) 开启语义检索

首次批量入库时 AI 会提示配置向量化。推荐免费 BGE-M3（硅基流动），获取 Key → https://cloud.siliconflow.cn/account/ak。不配置也不影响核心功能。

### 4. 你的第一句话

| 你想... | 这样说 |
|------|------|
| 搜文献 | "帮我查 Transformer 在药物发现中的应用" |
| 保存 | "把这 5 篇保存到知识库" |
| 看自己的库 | "我的知识库有什么" / "知识库统计" |
| 创建专题 | "把这 N 篇组成一个专题" |

---

## FAQ

**Q: 这个和 global-biblio-base 有什么区别？**
A: 后者是"搜索引擎"（每次调用外部 API），本技能是"私人图书馆"（搜过就存下来，越积越多）。

**Q: 向量化要钱吗？**
A: 默认方案（硅基流动 BGE-M3）完全免费。

**Q: 我的数据安全吗？**
A: 全部存储在本地 `~/.workbuddy/academic-kb/`，不上传任何服务器。

---

> Inspired by [Karpathy LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) and powered by [SmartLib API](https://www.vipslib.com/).
