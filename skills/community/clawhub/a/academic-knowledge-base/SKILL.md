---
name: academic-knowledge-base
displayName: 个人文献知识库，自带全球文献检索（支持向量搜索+传统分词搜索）
version: 3.11
homepage: https://www.vipslib.com
description: |
  面向学术研究者的个人知识中枢。整合 Karpathy LLM Wiki 知识编译能力 + SmartLib 海量文献检索能力，形成私有知识库与外部文献库双轨联动的研究助手。
  支持4类数据入库（文献检索结果、用户上传文献、资讯报道、个人学术数据）、研究专题（文献子集+智能命名+笔记+AI分析+导出）、向量化语义检索、分词匹配检索、参考文献管理、Wiki知识层自动维护。
  ✨ 亮点：入库文献自动保留原始数据库来源链接（覆盖300+数据库，如Scopus/WoS/EI/PubMed等，覆盖率100%），支持多源交叉验证。
  采用懒加载引导式初始化，无需前置配置即可使用。配额管理复用 global-biblio-base 的 gateway 凭证和计次规则（v3.1：5接口，每次调用计1次），配额耗尽后暂停外部检索请求。
  适用场景：文献管理、知识积累、论文写作辅助、研究调研。触发词：保存到知识库、知识库统计、我的知识库、给这篇打标签、列出我的专题、文献管理、论文管理、我的论文库、文献收藏、研究笔记、知识整理、学术知识库、论文知识库、文献整理、学术笔记、研究知识管理、收藏这篇文章、加入知识库、文献综述工具。
  A personal knowledge hub for academic researchers — integrating Karpathy LLM Wiki + SmartLib literature search + vectorized semantic retrieval. Ingested literature automatically preserves original database source links (300+ databases, 100% coverage) for cross-verification. Quota managed via global-biblio-base gateway with v3.1 billing rules (5 interfaces, 1 quota per successful call), restricted display when quota exhausted.
  Production URL: read from global-biblio-base/config.json → SMARTLIB_GATEWAY_URL (Gateway v47, version 67)
metadata:
  openclaw:
    emoji: "🧠"
    requires:
      env:
        - SMARTLIB_GATEWAY_SECRET
        - SMARTLIB_GATEWAY_URL
        - SMARTLIB_EMAIL
    envVars:
      - name: SMARTLIB_GATEWAY_URL
        required: true
        description: SmartLib Gateway 服务地址
      - name: SMARTLIB_GATEWAY_SECRET
        required: true
        description: SmartLib Gateway API 密钥
      - name: SMARTLIB_EMAIL
        required: true
        description: 注册邮箱（必填，复用 global-biblio-base 凭证与配额）
agent_created: true
recommends: [global-biblio-base, smartlib-citation-checker]
allowed-tools: [Read, Write, Edit, Bash, WebFetch, AskUserQuestion]
---

## 快速触发词 / Quick Trigger Reference

| 你想做什么 / What to do | 这样说 / Say |
|------|------|
| 保存文献 | "保存到知识库"、"加入知识库"、"收藏这篇文章" |
| 搜索自己的文献 | "在我的知识库里找..."、"查一下我的文献有没有..." |
| 看知识库统计 | "知识库统计"、"我的知识库有多少文献" |
| 管理标签 | "给这篇打标签..."、"我的深度学习标签" |
| 导出引用 | "引用这篇文献"、"导出这几篇为 BibTeX" |
| 创建研究专题 | "把这N篇组成一个专题"、"开个XX的课题" |
| 查看专题 | "列出我的专题"、"打开XX专题"、"有哪些专题" |
| 专题内检索 | "在XX专题里检索..." |
| 导出/归档 | "导出XX专题"、"归档XX专题" |
| 配置 | "知识库配置"、"配置向量化" |
| 健康检查 | "整理知识库"、"Lint我的Wiki" |

# 学术知识库 / Academic Knowledge Base

> 中文 / Chinese | [English below each section]

面向学术研究者的个人知识中枢 —— 整合 Karpathy LLM Wiki 知识编译 + SmartLib 文献检索 + 向量化语义检索，让每一次检索和研究都沉淀为自己的知识资产。

> A personal knowledge hub for academic researchers — integrating Karpathy LLM Wiki knowledge compilation + SmartLib literature search + vectorized semantic retrieval. Every search and study session compounds into your own knowledge asset.

---

## 来源参考 / Source References

本技能的设计架构和工作流继承自以下两个上游技能：

### 参考技能 1：Karpathy LLM Wiki

- **技能位置**：`~/.workbuddy/skills/Karpathy LLM Wiki/`
- **核心理念**：用 LLM 增量构建和维护持久化 Wiki 知识库，而非每次查询时做 RAG
- **本技能继承**：Raw 不可变性、LLM 维护 Wiki 层、ingest/query/lint 操作、[[wiki-links]] 格式

> Inherited: Raw immutability, LLM-owned wiki layer, ingest/query/lint operations, wiki page format.

### 参考技能 2：global-biblio-base

- **技能位置**：`~/.workbuddy/skills/global-biblio-base/`
- **版本**：v3.1
- **核心理念**：基于 SmartLib 开放平台 API 提供中外文学术文献检索，已接入全程自动化服务（gateway 注册 + 配额消耗 + 微信支付充值）
- **本技能继承**：文献检索 API + 认证流程、元数据字段结构、三级检索策略、外部检索联动。**配额共享**——与 literature-search 使用同一 gateway 凭证和配额

> Inherited: SmartLib API auth, metadata schema, search strategies, field validation. **Quota shared** with literature-search.

---

## 核心架构 / Core Architecture

```
~/.workbuddy/academic-kb/
├── raw/                          # 原始资料（不可修改 / Immutable）
│   ├── literature/               #   文献全文 PDF/解析文本
│   ├── news/                     #   资讯/报道原文
│   └── personal/                 #   个人实验数据、笔记
├── db/                           # 结构化数据库
│   ├── literature.json           #   文献元数据（Identifier 为唯一 key）
│   ├── news.json                 #   资讯条目
│   ├── personal_data.json        #   个人学术数据
│   └── tags.json                 #   标签体系
├── wiki/                         # LLM 维护的 Wiki 知识层
│   ├── index.md                  #   知识目录
│   ├── log.md                    #   操作日志
│   └── [topic-pages].md          #   主题/概念页面
├── vectors/                      # 向量化存储
│   ├── embeddings.json           #   向量数据
│   └── vector_config.json        #   向量化范围配置
├── sessions/                     # 研究专题（文献子集+笔记+分析）
│   └── {slug}_yyyymmdd/
│       ├── session.json           #   专题元数据
│       ├── literature.json        #   选中文献快照
│       ├── notes.md               #   用户研究笔记
│       └── analysis.md            #   AI 生成的研究综述
└── KB-SCHEMA.md                  # 知识库 Schema 与约定
```

| 层级 / Layer | 职责 / Responsibility | 所有者 / Owner |
|------|------|------|
| **Raw Sources** | 原始资料，不可修改 / Immutable sources | 用户 / User |
| **Structured DB** | 结构化元数据，CRUD / Structured metadata | 系统 + 用户 |
| **Wiki** | LLM 自动维护的知识网络 / Auto-maintained knowledge graph | LLM |
| **Vectors** | 语义检索向量索引 / Vector index | 系统 |

---

## 凭证与配额 / Credentials & Quota

> ## ⚠️ 强制规则 — 必须先询问邮箱
> 1. **执行任何操作前，必须先询问用户邮箱地址**
> 2. 禁止使用 global-biblio-base/config.json 中预填的邮箱（即使存在且非 null）
> 3. 禁止自动生成邮箱（如 `user@example.com`、`auto@xxx.com` 等）
> 4. 用户未提供邮箱 → 停止执行，回复：
>    "请提供您的邮箱地址以注册 SmartLib 学术知识库（新用户免费 100 次/月）"
> 5. 只有用户明确输入邮箱后，才能调用 /register 或 /quota
>
> ## 邮箱识别自动化
> 当用户消息中出现以下模式时，自动提取邮箱 → 无需再次询问：
> - 明确的邮箱地址（包含 @ 符号的完整地址，如 `xxx@xxx.xxx`）
> - "我的邮箱是 xxx" / "email: xxx" / "用 xxx 注册" / "邮箱 xxx"

本技能**不独立注册**，复用 global-biblio-base 的 gateway 凭证和配额：

```
检查 global-biblio-base 的 config.json
  ├── SMARTLIB_EMAIL 已配置 → 复用凭证，进入配额检查
  │
  │   配额检查: GET {GATEWAY_URL}/quota?email={SMARTLIB_EMAIL}
  │
  │   如果返回 404 "not_registered" → 用户可能已被重置/删除
  │     → 提示: "检测到您的账户需要重新绑定，正在自动重新注册..."
  │     → 调 gateway /register（使用同一邮箱）→ 写入 config.json
  │     → 注册成功后继续配额检查
  │
  └── SMARTLIB_EMAIL 未配置 → 引导用户先注册:
        "📋 知识库需要 SmartLib 检索能力。首次使用需绑定邮箱（免费 100 次/月，仅用于配额管理），请输入邮箱即可开始:"
        用户输入 → 调 gateway /register（无需验证码）→ 写入 config.json
        → 成功: "✅ 注册成功！本月免费 100 次，可立即使用（邮箱验证仅充值时需要，现在不验证也能用）。请告诉我您想检索或录入什么文献——"
        → 失败 → 提示原因 → 终止
```

> **注意**：注册无需验证码，极速完成。

**配额消耗规则 / Quota Consumption Rules:**

本技能与 global-biblio-base **共享配额和计次规则**。配额按**实际 API 接口调用次数**计费，共 5 个接口，每次调用计 1 次。

> Shared quota and billing rules with literature-search. **5 interfaces**, each successful call = 1 quota. Failed calls do NOT consume quota (v36).

**计费接口清单（5个）/ Billable Interfaces (5 total):**

| 类别 | 接口 | 计费 | 知识库中的触发场景 |
|------|------|------|------|
| **检索** | 中文期刊检索 | 1次/调用 | 入库时 SmartLib 补全字段（中文文献匹配） |
| **检索** | 全球文献检索 | 1次/调用 | 入库时 SmartLib 补全字段（外文文献匹配）、研究专题新检索 |
| **详情** | 中文期刊详情 | 1次/调用 | 补全文献元数据（查看详情） |
| **详情** | 全球文献详情 | 1次/调用 | 补全外文文献元数据（查看详情） |
| **下载** | 中文期刊全文下载 | 1次/调用 | 入库时下载中文期刊全文 PDF |

**不计费的操作 / Non-billable Operations:**

| 操作 / Operation | 说明 / Note |
|------|------|
| 知识库内检索（分词+向量） | 本地操作，不调 SmartLib API |
| 入库 SmartLib 检索结果（元数据） | 文献已在检索 Skill 中消耗过配额 |
| 标签管理、导出引用、Wiki 维护 | 本地操作 |
| 向量化 API 调用 | 使用独立的向量化服务商，不计 SmartLib 配额 |
| 研究专题创建（本地文献子集） | 不调外部 API |
| 外文 OA PDF 探测 | 外部免费 API，不计 SmartLib 配额 |

---

## 🔒 配额耗尽处理 / Quota Exhaustion

配额耗尽后**暂停外部检索请求**：

| 状态 | 行为 |
|------|------|
| **配额充足** | 完整使用所有功能（检索、入库、专题、导出） |
| **配额耗尽** | 知识库本地检索正常；外部检索、入库匹配、新文献补充**一律拒绝** |

**配额耗尽后的提示格式：**

```
⚠️ 您的 SmartLib 检索配额已用尽。

知识库内 {N} 篇已有文献仍可正常检索、管理、导出。
但外部检索、入库匹配等需要调用 SmartLib 的功能已被暂停。

> 💰 充值套餐：
> 体验包：¥9.90 / 1000次
> 月付基础：¥29.00 / 5000次/月
> 月付进阶：¥99.00 / 20000次/月
> 月付专业：¥299.00 / 100000次/月
> 回复「充值」获取微信支付码，恢复 SmartLib 外部检索能力。
```

**重要规则**：
- 配额耗尽后，所有需要调用 SmartLib API 的操作（外部检索、入库匹配、新文献补充）**一律拒绝**，不展示任何部分结果
- 知识库内已有文献的检索、标签管理、导出、Wiki 维护、研究专题 — **不受影响**（纯本地操作）
- 充值后立即恢复所有外部检索功能

---

## 输出规范 / Output Standards

**每次调用 SmartLib API 后，在结果末尾展示配额状态：**

```
📊 本次消耗 {n} 次 | 剩余 {remain} 次 (共 {total} 次/月)
```

```
```

---

## 知识库初始化 / KB Initialization

**无需显式"初始化"。** 懒加载引导式设计——首次使用任何功能时，基础设施自动静默创建。

> No explicit "init" required. Lazy-loading guided design.

### 自愈式就绪 / Self-Healing Readiness

| 检查项 / Check | 缺失时行为 / On Missing |
|------|------|
| 根目录不存在 | 静默创建完整目录结构 + 空 JSON 文件 + KB-SCHEMA.md |
| vector_config.json 不存在 | 静默写入默认配置（BGE-M3 / 硅基流动 / 仅摘要向量化） |
| 向量化 API Key 未配置 | 仅在首次需要向量化时引导配置，不阻塞入库 |
| embeddings.json 损坏 | 静默重建空文件 |

### 向量化方案备选 / Vectorization Options

| 方案 / Option | 模型 / Model | 费用 / Cost | 维度 / Dims |
|------|------|------|------|
| 推荐 | 硅基流动 BGE-M3 | **免费** | 1024 |
| 高精度 | 智谱 Embedding-3 | ¥0.5/百万token | 256-2048 |
| 高精度 | 阿里 text-embedding-v4 | ¥0.5/百万token | 64-2048 |
| 私有部署 | Ollama + nomic-embed-text | 免费 | 768 |

---

## 数据入库 / Data Ingestion

支持 4 种数据类型入库。

### 类型 1：SmartLib 检索结果入库

**触发**：用户在使用 global-biblio-base 后说"保存到知识库"、"加入知识库"

```
用户指定入库的检索结果
  ├── 遍历每条结果
  │     ├── Identifier 去重检查（db/literature.json）
  │     │     ├── 已存在 → 跳过
  │     │     └── 不存在 → 入库
  │     └── 入库操作：写 literature.json + 下载原文到 raw/ + 向量化（若配置）
  └── 汇总提示入库结果
```

**文献元数据格式（db/literature.json）：**

```json
{
  "Identifier_Value": {
    "identifier": "文献唯一ID",
    "title": "文献标题",
    "authors": ["作者1", "作者2"],
    "source_name": "期刊/来源",
    "publish_year": "2025",
    "abstract": "摘要内容",
    "keywords": ["关键词1"],
    "doi": "10.xxxx/xxxx",
    "core_indexing": "SCI;EI",
    "source": "smartlib",
    "source_links": [
      {"db_id": "scopusjournal", "db_title": "Scopus", "link": "https://www.scopus.com/..."},
      {"db_id": "wsoscimagazine", "db_title": "WoS SCI", "link": "https://www.webofscience.com/..."}
    ],
    "vectorized": true,
    "tags": ["深度学习"],
    "notes": ""
  }
}
```

> **source_links 字段说明**：从 SmartLib 详情接口的 `Source` 字段自动提取，保留原始数据库来源链接（覆盖300+数据库，如Scopus/WoS/EI/PubMed等，覆盖率100%，平均4.75个链接/篇）。入库时自动保存，支持多源交叉验证。

### 类型 2：用户上传文献入库

**触发**：用户提供 PDF/Word/Markdown/BibTeX 文件路径

```
Step 1：解析文献（PDF 提取文本 / Word 解析结构 / BibTeX 解析字段）
Step 2：匹配 SmartLib（用标题+作者检索 API 4，标题相似度 > 80% 则合并补全 DOI/ISSN/核心收录）
Step 3：存储（原文 → raw/literature/，元数据 → literature.json，向量化）
```

未匹配 SmartLib 的文献标注 `source: "user_upload"`。

### 类型 3：资讯/报道入库

**触发**：用户提供 URL 或粘贴文本

```
Step 1：提取标题、来源、日期、摘要
Step 2：原文 → raw/news/，元数据 → db/news.json
```

### 类型 4：个人学术数据入库

**触发**：用户上传实验数据、CSV、笔记等

```
Step 1：解析数据（CSV 保持表格结构 / 文本 Markdown 存储）
Step 2：询问是否关联已有文献
Step 3：原文 → raw/personal/，元数据 → db/personal_data.json
```

---

## 向量化服务 / Vectorization Service

### API 调用规范

统一使用 OpenAI 兼容格式：

```
POST {base_url}/embeddings
Authorization: Bearer {api_key}
Body: {"model": "{model_name}", "input": ["文本1", "文本2"]}
```

### 批量向量化

- 单次最多提交 32 条
- 每批 32 条并发（最多 3 批并行）
- 单批失败自动重试 3 次（指数退避）

### 向量化触发条件

| 操作 / Operation | 触发向量化？ |
|------|:--:|
| 文献检索结果入库 | 若配置开启 |
| 用户上传文献入库 | 若配置开启 |
| 资讯/个人数据入库 | 默认关闭 |
| 删除文献 | 同步删除向量索引 |

---

## 检索策略 / Retrieval Strategy

### 双轨检索流程

```
用户查询
  │
  ├── 1. 知识库分词匹配检索
  │     ├── 中文分词 → title/abstract/keywords 倒排匹配
  │     └── BM25 评分（标题 > 关键词 > 摘要）
  │
  ├── 2. 知识库向量语义检索
  │     ├── 查询向量化 → 余弦相似度匹配
  │     └── 返回 Top-N（N = 分词匹配结果的 2 倍）
  │
  ├── 3. 去重合并
  │     └── BM25 × 0.6 + Vector_Similarity × 0.4
  │
  ├── 4. 自适应外部检索
  │     ├── 知识库 ≥ 3 条 → 知识库置顶 + 正常外部检索
  │     ├── 知识库 1-2 条 → 知识库置顶 + 外部检索加倍
  │     └── 知识库 0 条 → 全量外部检索
  │
  └── 5. 结果展示（分区：知识库 [📚] / 外部 [🌐]）
```

### 结果展示格式

```
🔎 检索："{用户查询}"

════════════════════════════════
📚 你的知识库（共 N 篇）
════════════════════════════════
| # | 收录 | 标题 | 作者 | 来源 | 年份 |
|---|------|------|------|------|------|
| 1 | [SCI] | ... | ... | ... | 2024 |

════════════════════════════════
🌐 外部检索补充（SmartLib，共 M 篇）
════════════════════════════════
| # | 收录 | 标题 | 作者 | 来源 | 年份 |
|---|------|------|------|------|------|
| 1 | - | ... | ... | ... | 2025 |

💾 输入 "保存 1,3" 将外部结果加入知识库
```

---

## Wiki 知识层维护 / Wiki Maintenance

继承自 LLM Wiki 模式，入库后 LLM 自动维护知识网络。

### 触发时机

| 操作 | 更新范围 |
|------|------|
| 入库新文献 | 创建/更新该文献涉及的主题概念页 |
| 批量入库 ≥ 5 篇 | 全量 Lint（交叉引用、矛盾检测、孤立页面） |
| 用户手动要求 | "整理知识库"、"Lint我的Wiki" |

### 入库后更新流程

```
文献入库 → 提取主题 → 检查已有 Wiki 页面 → 创建/更新概念页
  → 写入引用 → 更新交叉引用 → 检测矛盾 → 更新 index.md → 追加 log.md
```

### Lint（健康检查）

批量入库 ≥ 5 篇后自动执行，或用户手动触发。检查项：

1. **矛盾检测**：不同文献间结论冲突，标注 `[⚠️ 矛盾]`
2. **过时检测**：超过 3 年未更新的概念页
3. **孤立页面**：无入链的 Wiki 页面
4. **冗余检测**：内容高度相似的页面

---

## 参考文献管理 / Reference Management

| 功能 / Feature | 触发方式 / Trigger |
|------|------|
| 添加文献 | "保存到知识库" |
| 查看详情 | "查看文献 XXX" |
| 删除文献 | "删除文献 XXX"（仅删元数据，raw 原文保留） |
| 去重检测 | 入库时自动触发（Identifier / DOI / 标题匹配） |
| 标签管理 | "给这篇文献打标签'深度学习'" |
| 批量导出 | "导出这几篇为 BibTeX" |
| 引用生成 | "引用这篇文献" → GB/T 7714 / APA / MLA / BibTeX |

### 导出格式

| 格式 | 用途 |
|------|------|
| GB/T 7714-2015 | 中文论文（优先） |
| APA 7th | 社科论文 |
| MLA 9th | 人文论文 |
| BibTeX | LaTeX |

---

## 研究专题 / Research Sessions

从知识库中挑选文献子集组成研究专题。专题自包含（文献快照 + 笔记 + AI 分析），可独立导出迁移。

> Create focused research sessions from your KB. Self-contained and portable.

### 触发场景

| 用户意图 / Intent | 触发短语示例 |
|------|------|
| 创建专题 | "把这N篇组成一个专题"、"用这些结果创建专题" |
| 查看专题 | "列出我的专题"、"打开XX专题" |
| 专题内操作 | "在XX专题里检索..."、"更新XX专题笔记" |
| 导出/归档 | "导出XX专题"、"归档XX专题" |

### 存储结构

```
~/.workbuddy/academic-kb/sessions/{slug}_{yyyymmdd}/
├── session.json          # 专题元数据（标题、来源、状态）
├── literature.json       # 选中文献快照（自包含可迁移）
├── notes.md              # 用户研究笔记
└── analysis.md           # AI 生成的研究综述
```

### 专题操作

| 操作 | 说明 |
|------|------|
| 创建 | 选文献 → AI 智能命名 → 生成 analysis.md |
| 添加文献 | 追加到专题 literature.json，不影响主库 |
| 专题内检索 | 限定范围为专题文献，复用双轨检索 |
| 更新笔记 | 追加内容（带时间戳），AI 可辅助生成大纲 |
| 导出 | 打包专题目录为 zip |
| 归档/删除 | 归档：status → archived；删除：需二次确认 |

> Sessions are snapshots — editing session content never affects the main KB.

---

## 知识库统计 / KB Statistics

**触发**：用户说"知识库统计"、"KB Stats"等

生成交互式 HTML 报告（模板 `kb-report.html`），包含：

| 功能 | 说明 |
|------|------|
| 摘要卡片 | 文献总量、已向量化数、资讯数 |
| 文献构成 | 按类型和语言的柱状图 |
| 年份分布 | 按年份统计柱状图 |
| 热门标签 | 标签云 |
| 全部文献列表 | 可展开明细表 |

报告通过 `preview_url` 打开。未初始化时显示引导页。

---

## 配置管理 / Configuration Management

| 用户指令 / Command | 操作 / Action |
|------|------|
| "知识库配置" | 展示 vector_config.json 关键信息 |
| "配置向量化" | 展示方案对比表，引导输入 API Key |
| "开启全文向量化" | 修改 vector_config.json，提示是否补向量化 |
| "换用智谱向量" | 修改 provider/model，提示需重新向量化 |

Key 写入 `~/.workbuddy/academic-kb/vectors/vector_config.json` 的 `api_key` 字段。

---

## 与外部技能的联动 / Integration with Other Skills

| 技能 / Skill | 联动方式 / Integration | 关系 |
|------|------|------|
| **llm-wiki** | Wiki 层核心模式（ingest/query/lint、Raw 不可变性、[[wiki-links]]） | ⬆️ 上游参考 |
| **global-biblio-base** (v3.1) | 检索结果一键入库；SmartLib 补全字段；共享配额与凭证；外部检索联动 | ⬆️ 上游参考 |
| **smartlib-citation-checker** | 引用核查时优先查知识库；引用格式转换引擎复用 | ➡️ 同级协作 |

---

## 安全与隐私 / Security & Privacy

| 安全原则 / Principle | 实现 / Implementation |
|------|------|
| 零越权文件访问 | 所有操作限定在 `~/.workbuddy/academic-kb/` 内 |
| API Key 安全 | 仅存储在本地 vector_config.json，仅发送至用户选择的向量化服务商 |
| 零隐藏网络调用 | 仅 SmartLib API 和向量化 API，无遥测 |
| Raw 不可变 | `raw/` 目录不可修改不可删除 |
| 无远程执行 | 所有代码本地执行 |

---

## 错误处理与回退 / Error Handling & Fallback

| 故障场景 / Failure | 降级行为 / Degradation |
|------|------|
| SmartLib API 无响应 | 自动重试 3 次（1s/3s/9s），失败 → 提示稍后重试 |
| SmartLib Token 过期 | 自动重新获取，用户无感知 |
| 向量化 API 无 Key | 跳过向量化，照常入库，分词检索正常 |
| 向量化 API 调用失败 | 分批重试 3 次，单批失败不影响其他批 |
| embeddings.json 损坏 | 静默重建，后续检索时自动补向量化 |
| 知识库目录被误删 | 下次操作时自动检测并静默重建 |

---

## 版本历史 / Version History

| 版本 | 日期 | 核心变更 |
|------|------|---------|
| v3.0 | 2026-05 | 初次上线：支持4类数据入库、双轨检索（向量+分词）、Wiki知识层、研究专题管理 |
| v3.1 | 2026-05 | 外部检索配额消耗更透明，API调用成功后才扣次数 |
| v3.2 | 2026-05 | 入库文献自动附带原始数据库来源链接，支持一键跳转验证 |
| v3.3 | 2026-06 | 外部检索失败不再消耗配额；上游文献检索技能功能增强 |
| v3.4 | 2026-06 | 服务连接优化，新增更多文献入口 |
| v3.5 | 2026-06 | 注册流程简化，新用户开通更快捷 |
| v3.6 | 2026-06 | 注册赠送次数增加至100次；可订阅套餐最低1000次起 |
| v3.7 | 2026-06 | 新用户引导体验优化，首次使用自动配置，无需手动设置 |
| v3.8 | 2026-06 | 文献检索渠道扩充至12亿全球文献 |
| v3.9 | 2026-06 | 文献检索链路优化，查全率和查准率提升 |
| v3.10 | 2026-06 | 技能名称更新为「个人文献知识库」；检索速度优化 |
| v3.11 | 2026-06 | 技能展示名称与描述优化 |
