---
name: ai-weekly
slug: ai-weekly
version: 4.1.0
displayName: AI Weekly Report
summary: 生成可搜索/筛选/暗色模式的 AI 行业新闻单文件网站（公开 RSS 取数，无付费 API 依赖）
tags: [ai, news, report, rss, weekly, 人工智能, 周报]
homepage: https://github.com/Elisabeth15501/ai-weekly
compatibility: Claude Code, OpenAI Codex, OpenCode, OpenClaw, Coze, WorkBuddy
description: >
  AI 行业新闻网站生成工具。生成一个可搜索、可筛选、支持暗色模式的 AI 新闻网站（单文件 HTML）。
  **直接说人话就能触发，不需要记命令**（例：「这周 AI 有什么大事」「给我看个 AI 简报」）。
  新闻默认全部来自公开 RSS 抓取（14 个精选源：国内 7 + 国外 7，国内源优先，无单点依赖）；**默认不调用任何付费/商业 API**。另提供一个**可选**的 NewsAPI 接入（`--news-api` + 自备 `NEWSAPI_KEY`，**默认关闭**），是否启用完全由用户决定。
  如需用 AI HOT 或其他「AI 行业知识类」外部 API 增强可信度，由用户自行获取数据并以
  --external-news-json 注入，是否启用完全由用户决定。每条新闻含原始来源链接。
  注意：AI HOT 的 legacy /api/public/* 已于 2026-10-31 停服（域名 301 到 aihot.news）；
  v1 参数形态不同（take→limit、since→window、新增 by），沿用 legacy 参数会静默返回 400 空结果。
  市场/融资图表数据由 WebSearch 获取后注入，未提供时明确标注「示例/估算」。
  触发词·生成（任意一句即可）：AI周报、AI行业周报、AI新闻、人工智能周报、AI行业动态、生成AI报告、
  AI新闻网站、AI新闻站、这周AI有什么大事、AI圈最近怎么样、给我看个AI简报、AI新闻汇总、
  做个AI周报、AI行业速览、我想看AI动态、weekly AI report、AI news digest。
  能力边界（重要）：本技能的默认行为**只是生成新闻内容**——抓取、生成 HTML、校验、展示。
  它**不会**部署、不会推送飞书、不会改动仓库任何设置（含 GitHub Pages 配置）、不会执行 git push。
  部署/推送/切 Pages 源/刷新排行榜等运维动作**不属于本技能的触发能力**，仅在用户明确点名要求时才执行，
  且不由本技能声明面触发。若用户只是要看 AI 新闻/周报/简报，直接生成内容即可，不要询问或执行任何运维动作。
  支持自动化：每周一上午 9 点自动生成最新版网站（仅生成，不含部署）。
metadata:
  author: Elisabeth15501
  version: "4.1.0"
  homepage: https://github.com/Elisabeth15501/ai-weekly
  tags: [ai, news, report, rss, weekly, leaderboard, market-data]
---

# AI Weekly Report Skill

> **Cross-platform Agent Skill** — Claude Code · OpenAI Codex · OpenCode · OpenClaw · Coze · WorkBuddy 通用。
> 跨平台 `SKILL.md`，遵循开放 Agent Skill 规范（Anthropic AgentSkills / OpenClaw / Coze 共用的 `SKILL.md` 标准）。
> 单一入口、单一真相源：本文件即为技能的全部说明，无需任何平台专属包装。

## 目录（快速跳转）

- [§0 限制总表（读前必看）](#0-限制总表读前必看)
- [快速开始](#快速开始一句话怎么用)
- [一、为什么这件事重要](#一为什么这件事重要)
- [二、核心设计理念](#二核心设计理念)
- [二.5、硬约束](#二5硬约束必须遵守的边界)
- [三、不要做](#三不要做硬规则)
- [四、数据获取路由表](#四数据获取路由表)
- [五、轻量模式与完整模式](#五轻量模式与完整模式)
- [六、工作流](#六工作流完整模式)
- [七、本周看点编辑洞察](#七本周看点编辑洞察头版导语必做)
- [八、网络环境自适应](#八网络环境自适应国内外差异)
- [九、发布与第三方依赖说明](#九发布与第三方依赖说明合规)
- [十、文件清单](#十文件清单)

## §0 限制总表（读前必看）

> 本技能的能力边界，**诚实列出**，避免误用。评测中「降级却不说明」才会扣分，下面每一项都写明已知限制与红线。

| 维度 | 当前能力 | 已知限制 / 红线 |
|---|---|---|
| 可达性 | 国内 7 + 国外 7 共 14 个 RSS 源实测全通；国外榜源（LMArena / Artificial Analysis）直连**实测可达**（2026-09-02 起翻转旧结论） | 个别海外源在受限网络下可能不可达；技能据此**优雅降级到国内源与离线快照，绝不编造**（见 §8.1） |
| 数据口径 | 市场/融资数据支持「国内优先、国外对照」双口径路由（§8.3） | 市场数据为**静态快照注入**，非实时；榜单为实时抓取或**诚实标注日期的快照**，绝不冒充实时 |
| 翻译 | 中文翻译三级取值：本地缓存 → 远程译文源（**默认开启**，175 条）→ 本地 Ollama；**完全断网也有离线译文包** `translations_offline.json` | 无本地模型且远程源也未命中的个别条目，显式标注「未翻译·原文保留」而非静默留英文（F3） |
| 历史 | 每周快照自动留存（`snapshots/`），可复现任意一期 | 无快照的极早期（如 8/17 之前）榜单数据不可复原，诚实标注而非编造 |
| 体量 | 单文件 HTML，可搜索 / 筛选 / 暗色模式 | 周报条数取决于 RSS 窗口（默认近 7 天），非全量归档 |

## 快速开始（一句话怎么用）

不知道说什么话才能让本技能干活？下面 5 个真实对话直接复制即可触发全链路，**无需先读下文**：

```
用户：帮我生成一份本周 AI 行业新闻周报
→ 技能自动激活：RSS 抓取近 7 天新闻 →（建议用 WebSearch 注入市场/融资数据）
  → 撰写「本周看点」→ 生成单文件 HTML → 校验 → 展示。

用户：这周的 AI 新闻怎么样？给我看个简报就行
→ 技能激活，走「轻量模式」：直接在对话里输出 Markdown 分组列表，不生成网站。

用户：帮我把上周的周报推送到飞书
→ 技能激活，读取已生成的 report.json，调飞书连接器推头条卡片
  （部署托管可用 deploy.py --deploy-to 选腾讯云 COS / Vercel 等，不必依赖 GitHub Pages）。

用户：生成 8 月最后一周的 AI 周报，时间范围 2026-08-25 到 2026-08-31
→ 技能遵从你指定的时间窗，其余同完整模式。

用户：用我导出的 AI HOT 数据增强这期周报
→ 技能把你的 JSON 以 --external-news-json 注入（页脚自动署名），是否启用完全由你决定。
  （若这份 JSON 来自 AI HOT：其 legacy 接口已于 2026-10-31 停服，v1 参数名为
   limit / window 而非 take / since，取数时按 v1 写，否则会静默拿到空结果。）
```

> 卡片文案 + 更多对话示例见 [references/FAQ.md](references/FAQ.md)。飞书配置一步到位见 [scripts/init_feishu_config.py](scripts/init_feishu_config.py)。

🌐 **线上 Demo（最新一期产出形态）**：
https://elisabeth15501.github.io/ai-weekly/AI_News_2026-09-07.html
— 直接看单文件 HTML 周报：可搜索 / 筛选 / 暗色模式 / 中英文对照。
（历史各期见 https://github.com/Elisabeth15501/ai-weekly/wiki 的「Optimization Plan」索引，或 `AI_News_<日期>.html` 同名文件。）

### 1.1 真实对话场景（多轮：澄清 / 纠偏 / 排障 / 边界）

上面 5 条是「一句话触发」的语法层。下面是更接近真实使用的多轮对话——
覆盖**时间窗歧义怎么澄清、中途改主意怎么处理、抓取失败怎么排障、历史周报复现的真实边界**。
这些场景里的每条命令都已在 3.4.2 实测可用。

**① 时间窗歧义：先反问，不猜**

```
用户：这周的 AI 周报呢？
Agent：今天 9/9（周三），本周一是 9/7，所以「这周」有两种理解——
      · W37（8/31–9/7）：news.json 里已有 115 条，可以直接生成
      · W38（9/7–9/9）：只有 2 天数据，条数会偏少
      你要哪个？
用户：用 W37 那份
Agent：好 → generate_site.py --api-json news.json --date 2026-09-07 -o AI_News_2026-09-07.html
```

> **`--date` 是周期截止日**，显式传它才能保证「报告周期」与「文件名」一致。
> 不传会被写成「今天−7 ~ 今天」，历史周报会被逐步改写成当期内容。**重生成历史周报时必须显式传。**

**② 中途改主意：没有的功能直说，别硬凑**

```
用户：图表太占地方了，能去掉吗？
Agent：没有隐藏图表区块的开关，硬删会破坏报告完整性。三个真选项——
      ① 轻量模式：对话里直接给你 Markdown 分组列表，不出 HTML（最快）
      ② 保留网站但不注入市场数据：图表显示「示例/估算数据」标注
      ③ 改模板折叠该区块：要动 assets/news_site_template.html，我可以做
      你要哪个？
用户：① 就行
Agent：→ 轻量模式，对话内直接输出分组列表
```

**③ 抓取异常：先排查，别交一份空报告**

```
用户：跑一下这周周报
Agent：⚠️ RSS 只回来 3 条，14 个源里国内源全挂。先体检一下：
      → fetch_ai_news.py --check-feeds
      结果：3 个源超时、其余被限流。三个方案——
      ① 10 分钟后重试（限流常见，多半自愈）
      ② 用现有 3 条生成（页脚会标注源健康度，不假装数据完整）
      ③ WebSearch 手动补齐后写成同结构 JSON，走 --api-json
      我建议先 ①。
用户：那就重试一次
```

**④ 历史周报复现：保留期是硬边界**

```
用户：把 8/24 那期重新生成一份
Agent：先说清边界——RSS 源只保留约 1 周，现在回抓 8/24 那周只能拿个位数条目，
      **无法忠实复现**。两个路径——
      ① 有当时的快照（如 news_w34.json）→ 直接用它 + --date 2026-08-24
      ② 没有快照 → 只能用最新周数据，但那样标题会与内容不符，我不建议
      你本地有那周的备份吗？
用户：有，news_w34.json
Agent：→ generate_site.py --api-json news_w34.json --date 2026-08-24 -o AI_News_2026-08-24.html
```

**⑤ 参数细化：榜单条数与翻译行为**

```
用户：模型榜多给我看几条，另外英文标题别翻译了
Agent：→ generate_site.py --api-json news.json --ranking-top 20 --no-translate-title -o AI_News.html
      （摘要仍会翻译，只保留英文标题原文）
```

生成一个**可搜索、可筛选、响应式**的 AI 行业新闻网站（单文件 HTML）。
每条新闻附带原始报道链接，支持按分类 / 关键词筛选，桌面端和移动端均可使用。

## 一、为什么这件事重要

在 AI 协作工作流里，行业情报往往散落在十几个 RSS、公众号和付费简报里，且**大量"AI 周报"内容是模型生成的空话摘要**。
本技能的价值是把分散信号聚合成**可溯源、有编辑判断、可交叉验证**的单文件情报页，并让它在任意支持 `SKILL.md` 的 Agent 里都能跑——
不绑定任何商业 API、不依赖特定 Agent SDK，输出就是一份能被托管、被转发、被检索的静态 HTML。

## 二、核心设计理念

- **自治优先，增强可选**：新闻内容**默认全部来自 RSS 抓取**（`scripts/fetch_ai_news.py`，14 个精选源：国内 7 个优先 + 国外 7 个），**默认不调用任何付费/商业 API**（唯一例外是可选的 NewsAPI 接入，见 frontmatter 说明，默认关闭）；若用户希望用 AI HOT 等「AI 行业知识类」外部 API 增强可信度，由用户自行获取数据并以 `--external-news-json` 注入（含来源署名），是否启用完全由用户决定、风险自担（AI HOT 的 legacy 接口已于 2026-10-31 停服，需按 v1 的 `limit`/`window` 参数取数）
- **单文件交付**：所有 CSS/JS 内联，Chart.js 也内联进 HTML，无需任何外部文件
- **高可信度**：每条新闻必须附带原始报道 URL
- **零脑补**：市场/融资图表数据必须由 Agent 从 WebSearch 获取真实值后注入；未提供时明确标注「示例/估算数据」，绝不编造模型榜单
- **零运维**：生成后直接可用的静态 HTML
- **跨平台单源**：本 `SKILL.md` 同时服务 Claude Code / Codex / OpenCode / OpenClaw / Coze / WorkBuddy；引擎接口另见 `manifest.json`（LangGraph / Dify / Coze 等框架的最小接口描述）。兼容性按 AgentSkills 规范声明；**已实测 WorkBuddy，其余平台尚未逐一回归**，如遇加载问题请反馈。

## 二.5、硬约束（必须遵守的边界）

| 约束 | 上限 | 违反后果 |
|---|---|---|
| 单次抓取新闻条数 | ≤100 条 | 超过截取前 100，保留高评分项 |
| HTML 体积建议 | ≤5 MB | 超过自动压缩 Chart.js 数据点 |
| 每榜排行榜模型数 | ≤50 条 | 超过截取 top 50 |
| 趋势线数据点 | ≤20 点 | 超出处以均值或分段 |
| 趋势线渲染前提 | ≥2 周快照数据 | 第 1 周数据趋势线为空（非 Bug） |

> 详细参见 `scripts/aiweekly/const.py` 和 `scripts/validate_checks/constraints.py`（`validate_report.py --html` 会审计）。

## 三、不要做（硬规则）

1. **不要凭训练数据脑补数字**——所有市场数据、融资金额必须有可追溯来源
2. **不要丢掉新闻的 source URL**——每条新闻卡片必须包含可点击的原始链接
3. **不要用 "this week" / "最近" 搜索**——搜索关键词强制带年份 + 月份
4. **不要把旧闻当本周新闻**——检查发布日期，早于 7 天前的内容标注 `[n天前]`
5. **图表数据必须来自真实搜索**——市场规模/融资额由 WebSearch 获取后通过 `--market-data` / `--funding-data` 注入；**未提供时图表必须标注「示例/估算数据」**，不得伪装成实时数据
6. **不要让新闻卡片没有来源**——每张卡片底部必须有来源名称 + 链接
7. **不要省略任何章节**——某类别无数据时标注"暂无数据"但不删除章节
8. **不要编造模型榜单**——排行榜抓取失败时显示「暂无实时数据」，绝不用训练数据虚构模型名

## 四、数据获取路由表

| 数据类型 | 获取方式 | 优先级 |
|---------|---------|--------|
| 新闻列表 | `scripts/fetch_ai_news.py`（RSS：国内 量子位/36氪/雷峰网/智东西/极客公园/InfoQ 中国/钛媒体 + 国外 TechCrunch/MIT TR/HF Blog/TechMeme/MIT News/VentureBeat/Google AI；2026-09-10 实测 **14/14 全通**，国内源作地板，见 § 8.2） | **主** |
| 模型发布 | RSS（HF Blog / 关键词分类） | 主 |
| 产品发布 | RSS（关键词分类） | 主 |
| 行业动态 | RSS + WebSearch（政策/融资补充） | 主 |
| 学术论文 | RSS（arXiv/MIT News 类源）+ WebSearch | 主 |
| 市场数据（规模/采用率/份额） | **口径路由（见 § 8.3）**：`--region cn` 时**国内源优先**——中国信通院·中商产业研究院 / IDC 中国 / 艾瑞（可自行核对）；国外源 Statista / Gartner / Grand View Research 为**可选增强**（海外机构静态快照，作对照）。结果通过 `--market-data` / `--cn-market-data` 注入 | 主（需搜索） |
| 融资并购金额 | **口径路由**：`--region cn` 时国内源优先——IT桔子 / 烯牛数据 / 新浪创投Plus（可自行核对）；国外源 Crunchbase / CB Insights 为**可选增强**。结果通过 `--funding-data` / `--cn-funding-data` 注入 | 主（需搜索） |
| 模型排行榜 | **网络环境自适应多源池**（国外源 LMArena/Artificial Analysis/Hugging Face + 国内源 OpenCompass 司南/SuperCLUE/ModelScope）；按运行环境（国内/国外）自动排序优先级，实时源全失败则回退国内快照或本地缓存，绝不空白 | 主 |
| 政策监管 | RSS + WebSearch | 主 |
| **外部 API 增强（可选）** | 用户自备 AI 行业知识类 API（如 AI HOT）导出 JSON，以 `--external-news-json` 注入，页脚自动署名；是否启用由用户决定。注：AI HOT legacy 接口已于 2026-10-31 停服，v1 参数为 `limit`/`window`/`by` | 可选增强 |

> **依赖说明**：`scripts/fetch_ai_news.py` 需要 `feedparser`、`requests`、`beautifulsoup4`（随技能提供 `requirements.txt`）。
> 运行：一律用仓库根目录的 `bash run_report.sh scripts/xxx.py ...` 启动，启动器会自动探测并复用 `aiweekly` 受管 venv；若 venv 缺失，按提示 `python -m venv` + `pip install -r requirements.txt` 即可。
> 若这些包不可用，可手动用 WebSearch 搜集新闻后写成同样结构的 JSON，再走 `--api-json` 消费；
> 也可用你自己的外部 API（如 AI HOT）导出 JSON 后以 `--external-news-json` 注入——**注意：使用任何第三方 API 须遵守其服务条款，并自行承担合规风险**。
> AI HOT 的 legacy `/api/public/*` 已于 2026-10-31 停服（域名 301 到 `aihot.news`）；改用 v1 时参数名是 `limit`（非 `take`）、`window`（非 `since`），另有新增的 `by`，沿用旧参数会静默返回 400 空结果。

## 五、轻量模式与完整模式

根据用户意图选择模式：

| 用户说的 | 模式 | 输出 |
|---------|------|------|
| "快速看看" / "简单总结" / "不用图表" | **轻量** | Markdown 分组列表，直接在对话中展示 |
| 默认（无特别说明） | **完整** | 生成完整新闻网站 HTML |
| "生成报告" / "生成网站" / "周报" | **完整** | 生成完整新闻网站 HTML |

## 六、工作流（完整模式）

### 1. 确定时间范围

默认：过去 7 天。用户指定时遵从用户。

### 2. 抓取新闻（主路径：RSS）

```bash
# 用统一启动器运行（自动探测并复用 aiweekly venv，无需手动选解释器）
bash run_report.sh scripts/fetch_ai_news.py --output news.json
```

返回 `{"count": N, "items": [{title, summary, url, source, publishedAt, category, score}]}`，
分类已由脚本完成（`ai-models` / `ai-products` / `industry` / `paper` / `tip`）。

**降级**：若 RSS 抓取不可用（缺依赖/无网络），可手动用 WebSearch 搜集后写成同样结构的 JSON，
再走 `--api-json` 消费；也可用你自己的外部 API（如 AI HOT）导出 JSON 后以 `--external-news-json` 注入（AI HOT legacy 接口已于 2026-10-31 停服，按 v1 的 `limit`/`window` 取数）。

### 3. 补充市场/融资数据（必需搜索，结果注入图表）

各做 1-2 次 WebSearch，拿到真实数值后用 `--market-data` / `--funding-data` 注入：

| 数据类型 | 搜索关键词示例 | 注入参数 |
|---------|--------------|---------|
| 融资并购 | `AI funding Q2 2026`, `AI融资 2026年` | `--funding-data 17.4,13.1,... --funding-labels 23Q1,23Q2,... --funding-source "Crunchbase 2026"` |
| 市场数据 | `AI market size 2026 statistics`, `AI市场规模 2026` | `--market-data 51,71,103,... --market-labels 2020,2021,... --market-source "Statista 2026"` |

**若搜索无结果**：不伪造，直接省略参数——图表会显示「示例/估算数据」标注，由读者知悉非实时。

### 4. 生成新闻网站 HTML

读取 `assets/news_site_template.html` 理解结构，然后用 `Write` 生成完整网站。

**新闻网站必须包含：**
- 顶部搜索栏（实时过滤）
- 分类标签栏（全部 / 模型 / 产品 / 行业 / 论文 / 技巧）
- **「本周看点」编辑洞察区（头版导语，必做）**——见下方第七节
- 新闻卡片网格（响应式：3列 → 2列 → 1列）
- 每张卡片：类别色块缩略图、标题、摘要（2行截断）、来源名 + 原始链接、发布时间
- 市场数据区（2×2 四个 Chart.js 图表：全球/中国市场规模 + 全球/中国融资趋势）
- 模型排行榜区（表格式 Top 10，标注数据来源与排名标准）
- 暗色模式切换按钮
- 页脚：数据来源说明

```bash
bash run_report.sh scripts/generate_site.py --api-json news.json \
  --ranking-json ranking.json --profiles-json model_profiles.json \
  --insights-json insights.json --lead "本周主线：……" \
  -o AI_News_YYYY-MM-DD.html
```

> **推荐（强）**：尽量每次都传 `--insights-json` 与 `--lead`，这是头版核心、产品力所在。若**漏传**，`generate_site.py` 会自动从本周新闻派生基线「本周看点」（标题+摘要+分类+原文链接），**整段不再静默消失**——但自动版只是摘要级，缺少人工「编辑洞察」深度，故仍建议撰写 curated 版本覆盖。

> **「本周看点」三块内容的必现保证（无需任何参数）**：
> | 内容块 | 兜底机制 | 相关函数 |
> |--------|---------|---------|
> | 看点卡片 | 无 `--insights-json` 时从本周新闻按信号词打分派生 Top6 | `_auto_insights()` / `_auto_lead()` |
> | 「给本周的你」三张受众卡 | 无 `audience_summary` 时用内置三段文案 | `_DEFAULT_AUDIENCE_SUMMARY` |
> | 关键词的彩色分类标签 | 缺 `tag` 自动推断分类；完全无关键词时从新闻派生带标签关键词 | `_normalize_keywords()` / `_auto_keywords()` / `_infer_tag()` |
>
> 这三块均在**生成阶段服务端预渲染进静态 HTML**（`_render_audience_chips_html()` / `_render_keyword_chips_html()`），JS 只负责后续交互切换。因此**即使浏览器禁用 JS 或脚本报错，这些内容依然可见**——不会再出现「区块静默消失」。
>
> ⚠️ **排错提醒**：若重新生成后仍看不到某块内容，先确认 ① 输出路径是否就是你打开的那个文件（不要输出到 `-fixed`/`-static` 之类旁路文件名）；② 浏览器是否硬刷新（Ctrl/Shift+R）。用 `grep -c 'class="kw-tag"'` 判断**不可靠**——CSS 里有同名类定义，恒返回 ≥1；应改查 `grep -o 'class="kw-tag"[^>]*>[^<]*'` 看实际渲染内容。

### 5. 质量检查

生成后运行验证：

```bash
bash run_report.sh scripts/validate_report.py --html AI_News_YYYY-MM-DD.html
```

校验器检查新闻卡片、排行榜章节、市场图表、洞察与关键词；并内置 XSS 守护（脚本上下文 JSON 无原始 `</script>`、全文无 `javascript:`/`data:` href）。

### 6. 交付

- 文件名：`AI_News_YYYY-MM-DD.html`（如 `AI_News_2026-07-09.html`）
- 调用 `present_files` 展示
- 总结核心发现（3-5 条）

### 6.1 部署到网页托管（多后端，**必须用户明确要求**才执行）

> **决策边界（硬约束）**：本节所有动作都是**高权限运维动作**（改仓库设置 / git push / 对外发布），不是本技能的默认行为。
> **仅当用户明确点名要求某一项时**才执行对应的那一条；未点名时**一律不执行、不追问、不「顺手做掉」**。
> 内容请求（要新闻/周报/简报）与运维动作是**两件事**：要内容就只生成内容。
> 凭据只从环境变量或用户本次提供的值读取，**不写入项目文件、不回显、不进子进程 argv**。

飞书卡片里的「查看完整周报」按钮 `view_url` 需要一个可公开访问的地址。**不一定要用 GitHub Pages**——`scripts/deploy.py` 统一入口按 `--deploy-to` 选后端（**白名单校验，非法取值直接报错退出**）：

| `--deploy-to` | 适合 | GitHub 依赖 |
|------|------|------|
| `github-pages`（默认） | 已用 GitHub、熟悉 Pages | 需要（PAT + push + 切 Pages 源） |
| `tencent-cos` | 国内访问最稳、无需境外托管 | **不需要**（需 COS 桶 + 密钥） |
| `vercel` / `netlify` / `cloudflare-pages` | 海外免备案、一条命令 | **不需要**（需对应平台 token） |
| `local` | 自托管 / 内网文件服务 | **不需要** |

非 github-pages 后端无需配置 GitHub，飞书卡片 `view_url` 由后端自动推导（可用 `--view-base` 覆盖）。配置示例见 `delivery/deploy_config.example.json`。

默认（GitHub Pages）路径：`view_url` 指向 `https://<owner>.github.io/<repo>/AI_News_<date>.html`——该地址由 **`gh-pages` 分支**提供（仓库 Pages 源 = `Deploy from a branch: gh-pages / /root`）。用 `run_report.sh deploy` 即可把当期周报推到该分支：

```bash
# 流水线封装：底层调用 scripts/deploy_ghpages.py
bash run_report.sh deploy --html AI_News_YYYY-MM-DD.html
#   --push           推送（默认不推送，仅本地生成+提交）；--no-push 兼容旧调用
#   --switch-pages  部署后通过 GitHub API 把 Pages 源切到 gh-pages / /root（需 GITHUB_TOKEN）
#   --dry-run       只做 worktree+复制+index 预览，不提交不推送
```

`deploy_ghpages.py` 用 **git worktree** 操作 `gh-pages`（不污染 `main`、不进 SkillHub 包），并把所有 `AI_News_*.html` 累加进根目录 `index.html` 存档页（最新高亮）。脚本自动清理 worktree，本地 `gh-pages` 提交始终保留。

**一步到位**：`publish.py` 在推送飞书卡片的同时可顺带部署周报（需传 `--html`）：

```bash
bash run_report.sh scripts/publish.py \
  --news-json news.json --insights-json insights.json \
  --audience-json audience_summary.json \
  --html AI_News_YYYY-MM-DD.html --deploy
#   --deploy           生成 report.json 后顺带部署（默认 github-pages）
#   --deploy-to tencent-cos   改用腾讯云 COS（国内最稳，无需 GitHub）
#   --deploy-to vercel        改用 Vercel（海外免备案，无需 GitHub）
#   --push            部署时显式推送（默认仅本地提交不推送）；--no-push 兼容旧调用
#   --switch-pages     部署时一并把 Pages 源切到 gh-pages
```

**首次启用（一次性）**：`git push origin gh-pages` → 仓库 Settings → Pages → Source 选 `gh-pages / /root`（或 `run_report.sh deploy --switch-pages`）。注意：GitHub Pages 只允许单一来源，原先的 `.github/workflows/mirror.yml`（Actions artifact 部署）因此已停用（`if: false`），以免两种来源互斥导致部署失败。

### 6.2 分发：飞书头条卡片推送（P0，可选但推荐）

生成报告后，可把**本周头条速览**推到飞书，让情报在"工作者已在用的地方"被消费。卡片由 `delivery/feishu_bot.build_headline_card` 构造，经 **飞书连接器**（lark-cli，密钥由连接器托管、绝不落配置文件）发送——`publish.py` 组装 `report.json` 后自动经连接器推送。

```bash
# 组装 report.json 并经飞书连接器推送到群（bot 身份，需先把「WorkBuddy-Feishu CLI」机器人加进群）
bash run_report.sh scripts/publish.py \
  --news-json news.json --audience-json audience_summary.json \
  --output report.json --chat-id oc_xxxx

# 推给自己（user 身份 → 私聊，首次冒烟测试最省心，无需加机器人）
bash run_report.sh scripts/publish.py \
  --news-json news.json --output report.json --user-id ou_xxxx --as user

# 仅构造卡片预览、不推送：
bash run_report.sh scripts/publish.py --news-json news.json --audience-json audience_summary.json --dry-run

# 也可直接调连接器 CLI（等价于上面 publish.py 内部行为）：
python delivery/feishu_connector.py --report report.json --chat-id oc_xxxx --dry-run
```

- **目标解析优先级**：`--chat-id/--user-id` > 环境变量 `FEISHU_CHAT_ID/FEISHU_USER_ID` > `delivery/feishu_target.json`（`{"chat_id":"oc_xxx"}` 或 `{"user_id":"ou_xxx"}`）。
- **发送身份**：`--as bot`（默认，应用机器人，需机器人已入群）/ `--as user`（以你本人身份，需你对该会话有发消息权限）。
- 依赖：仅标准库 + 已连接的飞书连接器；**无需 `requests`**，卡片构建路径不会因缺 `requests` 而失败。
- 未配置任何目标时自动跳过推送（exit 0，不阻断报告生成）；推送返回业务错误时 exit 1。

**卡片内容**：本周主线 + 🔥本周重点（按 score 取 Top5，带链接/来源）+ 💡本周看点（Top3）+ 👥分角色摘要（开发者/PM/自媒体）+ 🔖关键词 + 「查看完整周报」按钮（链接自动追加 `?src=feishu&uid=<uid>` 度量参数）。

### 7. 自动化设置

当用户要求"每周自动生成"时，创建 recurring automation：

| 参数 | 值 |
|------|-----|
| name | `AI新闻网站自动更新` |
| scheduleType | `recurring` |
| rrule | `FREQ=WEEKLY;BYDAY=MO` |
| status | `ACTIVE` |
| prompt | 见下方自动化 Prompt 模板 |

```
你是 AI 行业新闻编辑。请生成一个 AI 新闻网站（默认公开 RSS 取数，不调用任何付费/商业 API）：

1. 运行 RSS 抓取获取近 7 天新闻：
   bash run_report.sh scripts/fetch_ai_news.py --output news.json
   （若依赖缺失/失败，改为 WebSearch 手动搜集，写成相同 JSON 结构再往下走）
2. 用 WebSearch 获取市场/融资真实数据（2-3 次搜索），记录数值与来源
3. 读取 assets/news_site_template.html 理解结构
4. 代入「有 AI 产品经理经验的专业科技媒体工作者」人设，基于 news.json 撰写「本周看点」：
   - 顶部写 3-6 个 keywords（{term, tag, note}；tag 为分类彩色标签可省略——省略时生成器自动推断，note 可为字符串或按受众分述的对象 {开发者, PM, 自媒体}），渲染在「本周看点」开头、带网页搜索链接；
   - 写 3-5 条 insight（每条覆盖：AI 产品/开发角度重点分析 + 本周 trends + 预计未来发展），务必去 AI 味、有观点锋芒；
   - 写顶层 audience_summary（{开发者, PM, 自媒体} 各一句），渲染为「给本周的你」三张受众卡；可省略（用内置 _DEFAULT_AUDIENCE_SUMMARY 兜底，区块永不隐藏）——注意键必须与 keywords[].note 的受众键一致；
   - 拟一句头版导语 lead。
   写入 insights.json（schema 见第七节），insight 字段承载「编辑洞察」栏。
5. 运行生成脚本（注入第 2 步真实图表数据 + 第 4 步洞察）：
   bash run_report.sh scripts/generate_site.py --api-json news.json \
     --market-data <数值> --market-source "<来源>" --funding-data <数值> --funding-source "<来源>" \
     --insights-json insights.json --lead "<本周主线一句话>" \
     -o AI_News_[日期].html
6. 运行 validate_report.py 检查质量
7. 调用 present_files 展示结果
8. （可选）部署到 GitHub Pages，让飞书卡片的「查看完整周报」可点击访问：
   bash run_report.sh deploy --html AI_News_[日期].html
   若沙箱网络/凭据不可用导致推送失败，跳过此步也不影响报告生成（本地 gh-pages 提交已就绪）。

注意：默认流程不含任何外部商业 API。若用户明确要求用 AI HOT 等外部 API 增强可信度，
     请提示用户自行从官方渠道导出 JSON，并以 --external-news-json 注入（含 --external-source-name/url 署名）。
     AI HOT 的 legacy /api/public/* 已于 2026-10-31 停服（域名 301 到 aihot.news）；
     v1 端点与参数均已改版（limit/window/by），沿用 legacy 参数会静默取到空结果。
```

## 七、「本周看点」编辑洞察（头版导语，必做）

这是本技能从「新闻聚合器」升级为「科技情报产品」的关键一步。**必须由你（Agent）基于本周新闻亲自撰写**，而非简单罗列。

**人设（务必代入）**：你是一个**有 AI 产品经理经验的专业科技媒体工作者**。你既懂怎么把 AI 能力做成产品、踩过工程与商业化的坑，又能像专栏编辑一样把行业信号讲清楚。

撰写要求：
- **顶部 `keywords`（必做）**：3-6 个本周 AI 行业最值得追踪的**关键词**，每条 `{term, tag, note}`。
  - `tag`：分类标签，取值建议 `模型 / 资本 / 产品 / 安全 / 基建 / 监管`，渲染为词条上的彩色小标签。**可省略**——省略时生成器会用 `_infer_tag()` 按词义自动推断，但显式指定更准。
  - `note`：可以是一句话字符串，也可以是**按受众分述的对象** `{"开发者": "...", "PM": "...", "自媒体": "..."}`（推荐），点击「给本周的你」的受众卡时，所有词条的 note 会联动切换成该受众视角。
  - 每个关键词渲染为**网页搜索链接**（点击在新标签打开搜索引擎，搜索词固定为「词语 AI」；搜索基址默认百度，可用 `--keyword-search-base` 覆盖）。整段下方固定一句引导：**"以上为本周 AI 行业最值得追踪的信号，建议你顺着这些词去做更多资料搜集与交叉验证。"**——目的是鼓励读者深挖，而非替他们下结论。
- **`audience_summary`（推荐）**：顶层字段，给三类读者各写一句本周结论 `{"开发者": "...", "PM": "...", "自媒体": "..."}`，渲染为「给本周的你」三张受众卡。**可省略**——省略时用内置 `_DEFAULT_AUDIENCE_SUMMARY` 兜底，该区块永不隐藏。注意：这里的键必须与 `keywords[].note` 的受众键**保持一致**，否则切换受众时 note 取不到值。
- **数量**：3-5 条，挑本周最影响「AI 产品方向」与「应用开发决策」的动向，不要面面俱到。
- **每条结构**：`kicker`（栏目标签）+ `title`（判断句，不是新闻标题复述）+ `analysis`（发生了什么、为什么重要，2-3 句的事实陈述，不用第一人称）+ `insight`（**编辑洞察栏**，见下）+ 可选 `related`（1-3 条指向原文的新闻链接）。
- **`insight` 三段式（核心）**：以"有 AI 产品经理经验的专业科技媒体工作者"口吻写，必须覆盖：
  1. **重点分析**：循着 AI 产品 / 应用开发的发展角度，拆解这条新闻对"做产品、做开发"到底意味着什么；
  2. **本周 trends**：点明本周正在发生的趋势（用"本周趋势是……"自然带出）；
  3. **预计未来发展**：给出未来判断（用"往后看 / 我判断 / 我倾向于认为"等带观点的口吻，要有具体指向，不要空泛）。
- **开头一条 `lead`**（电梯演讲）：一句话概括本周主线，作为头版导语。
- **语气（务必去 AI 味）**：写成一个有十年经验的科技专栏编辑的手笔，而不是模型生成的摘要。具体要求：
  - 有**明确观点与锋芒**，敢于下判断（"是该重新翻一遍账单了""别高兴太早""没人再犹豫了"这类口吻），不要全程中立。
  - **禁止**工整对仗的「对 AI 产品开发：…… 对应用开发：……」分述模板；把产品/开发的影响自然揉进一段连贯的散文里。
  - **禁用** AI 套话：避免「信号很明确／意义重大／不容忽视／值得关注／总的来说／综上所述」这类空泛收束；少用「赋能／抓手／闭环／范式」等黑话堆叠。
  - 用具体、口语化、带行业质感的表达（"翻一遍调用账单""把宝押在单一云""demo 更炸"），句子长短错落，像人在说话。
  - `analysis` 保持客观陈述事实，`insight` 才是编辑的主观判断——两者分工清晰，不要混成同一段。

写入 JSON（schema 与下方一致）后，用 `--insights-json` 注入；`--lead` 传导语：

```json
{
  "audience_summary": {
    "开发者": "旗舰模型单价下探，先把上季度调用账单重算一遍再决定要不要换栈。",
    "PM": "能力过剩、成本骤降，产品差异化重心从「用哪个模型」挪到「场景与数据」。",
    "自媒体": "「单位智能降价」是本周传播力最强的选题，配上账单对比图最好用。"
  },
  "keywords": [
    {
      "term": "单位智能降价",
      "tag": "资本",
      "note": {
        "开发者": "价格锚松动，重算模型调用预算",
        "PM": "定价模型要跟着推理成本重做",
        "自媒体": "降价幅度对比是天然爆款素材"
      }
    },
    {"term": "智能复利", "tag": "产品", "note": "曾鸣提出，Agent 进业务流程、算得清 ROI"}
  ],
  "insights": [
    {
      "kicker": "模型格局",
      "title": "旗舰模型密集上新，单位智能的定价开始松动",
      "analysis": "本周 Claude Opus 5 正式发布……（客观事实陈述）",
      "insight": "做 AI 产品的团队最纠结的……（重点分析）这一周的趋势是……（本周 trends）往后看半年，我判断……（预计未来发展）",
      "related": [{"title": "原标题", "url": "https://..."}]
    }
  ]
}
```

## 八、网络环境自适应（国内 / 国外差异）

不同运行环境对国内外网站的连通性差异很大，本技能对此做了显式处理：

- **源池与 region 标签**：综合榜源池 `[Artificial Analysis(国外), LMArena(国外), OpenCompass 司南(国内), SuperCLUE(国内)]`；开源榜源池 `[Hugging Face(国外), ModelScope 魔搭(国内)]`。每个源带 `region` 标签。
- **自动探测**：`--region auto` 同时探测一个国内哨兵与一个国外哨兵，判定 `cn` / `global` / `unknown`，并据此排序源优先级（国内环境优先国内源，反之亦然）。也可显式 `--region cn` / `--region global`。
- **出站代理（企业内网场景）**：部分企业内网要求全部出站流量经统一代理，技能遵循标准 `HTTPS_PROXY` 环境变量与 `--proxy` 参数，便于在合规内网环境中运行。**该参数仅用于合法的企业内网出站场景，本技能不提供、也不支持任何规避网络管理措施的能力。**
- **国内可直连榜的局限（重要）**：OpenCompass 司南、SuperCLUE、ModelScope 官网均为 **JS 渲染 SPA**，其数据 API 无法用简单 HTTP 稳定抓取（返回 SPA 兜底页 / 需鉴权）。因此这些"live"解析器按**尽力而为**实现——连不上或解析不到结构化数据就返回 None，由多源池优雅降级。
- **兜底不空白**：国内环境且实时源全失败 → 自动回退到随技能附带的 `cn_leaderboard_snapshot.json`（OpenCompass 司南 LLM 综合榜 + 开源榜快照，标注数据截止日，徽章显示「缓存快照」）；国外/未知环境且实时源失败 → 回退本地 `leaderboard_cache.json`。
- **来源透明**：排行榜每个子榜头部用徽章标注「实时·国内源 / 实时·国外源 / 缓存快照」，页脚注明探测到的网络环境与选用策略，用户始终知道数据从哪来。

排行榜来源优先级：`--ranking-json` > 多源池实时（按 region 排序）> 国内快照 / 本地缓存 > 显示「暂无实时数据」。
图表数据未注入时，图表注释自动标注「示例/估算数据」，不伪装为实时。

### 8.1 国内用户怎么办：实测数据与诚实结论（2026-09-09 复核）

**先说结论：LMArena 与 Artificial Analysis 没有官方国内镜像，国内受限网络下这两榜拿不到——这是硬边界，不假装能解决。**

下面是 33 次真实运行统计出的**各榜源成功率**（`leaderboard_health.jsonl`）：

| 源 | 标记 | 成功率 | 国内受限网络下 |
|---|---|---|---|
| Artificial Analysis | global | **97%** ✅ | ❌ 受限网络下不可达 |
| DataLearner | global | **81.8%** ✅ | ❌ 受限网络下不可达 |
| LMArena | global | 48.5% | ❌ 受限网络下不可达 |
| HuggingFace Open LLM | global | 42.4% | ⚠️ 原站不稳，**另有国内可访问镜像源可回退** |
| LLM-Stats | global | 0% | ❌ 长期空，等同失效 |
| OpenCompass 司南 | **cn** | **0%** ❌ | 页面为 SPA，抓不到结构化数据 |
| SuperCLUE | **cn** | **0%** ❌ | 同上 |
| ModelScope 魔搭 | **cn** | 0% → **已修复** | ✅ 改用官方 `openapi/v1/models` 后可直连 |

> ⚠️ 表中三个标记为 `cn` 的"国内源"，实测**成功率全是 0%**——它们只是"服务器在国内"，
> 页面却是 JS 渲染的 SPA，HTTP 直抓只能拿到骨架。所以"国内环境优先国内源"这条策略
> 过去实际是失效的（代码在跑，但从没拿到过数据）。

**已补齐的国内可直连源（2026-09-09 新增/修复）**

| 源 | 地址 | 状态 |
|---|---|---|
| ModelScope 魔搭 | `www.modelscope.cn/openapi/v1/models` | ✅ 官方 API，国内直连，含下载量/许可证 |
| HF 镜像热门模型 | `hf-mirror.com/api/models` | ✅ 国内直连，仅收录文本生成/对话类 |

**同时清除了两个"假镜像"（重要）**：代码里曾登记 `lmarena.org.cn`（**域名根本不存在**）
与 `aa-cn.mirror.xyz`（返回的是 mirror.xyz **博客平台**页面，与 AA 无关）。
后者尤其危险——HTTP 200 但内容无关，一旦解析出数据会直接污染榜单。
> 教训：**镜像必须逐个验证「域名存在 + 返回预期内容」，只看 HTTP 200 不够**。

**海外源不可达时的三条路径**（均为合法、不涉及任何网络访问规避手段）

1. **接受降级（推荐）**：开源榜由「国内可访问镜像 + ModelScope」两个国内源供给（热度榜，非能力基准，报告会注明）；综合榜若拿不到就显示「暂无实时数据」——**绝不编造名次**。
2. **自备数据注入**：`--ranking-json` 传入你自己的榜单 JSON，完全不走网络抓取。
3. **企业内网出站代理**：若你所处网络架构本身要求经统一代理出站，技能遵循标准 `HTTPS_PROXY` 环境变量与 `--proxy` 参数，可直接沿用该合规配置（详见下节）。

### 企业内网出站代理（合规场景）

部分企业内网要求所有出站流量经统一代理，这是标准的网络架构，并非本技能的特殊能力——技能只是遵循 `HTTPS_PROXY` / `--proxy` 这一通用约定，使自身能在该架构下正常工作。

> **合规边界**：本参数面向合法的企业内网/自建网关出站场景。**本技能不提供、不指导、也不支持任何规避网络管理措施的做法**；当某个源因网络原因不可达时，技能的既定行为是**降级到国内源与随技能附带的离线快照**，而不是设法绕行。

- **通过环境变量**
  ```bash
  HTTPS_PROXY=http://<proxy-host>:<port> bash run_report.sh scripts/generate_site.py --api-json news.json -o AI_News.html
  ```
- **通过参数**
  ```bash
  bash run_report.sh scripts/generate_site.py --api-json news.json --proxy http://<proxy-host>:<port> -o AI_News.html
  ```
- **降级行为**：代理不可达时，海外源优雅降级到国内快照 / 本地缓存，不会崩溃。

### 模型资料卡档案同步（real-time archive update）

排行榜资料卡所需的「机构 / 许可证 / 成本 / 上下文 / 多模态 / 适用场景 / 信息源」等字段，来自一个**联网核实的 canonical 档案**，随技能一起维护、随每次运行累积更新：

- **canonical 档案**：`model_profiles.json`（技能目录内）按模型名索引，存放逐模型核实过的资料；无需每次手动传入，`generate_site.py` 每次生成**自动加载**并注入资料卡。
- **新模型实时建档**：生成时会比对排行榜全部上榜模型与档案。若有模型缺档案，脚本写入 `model_profiles.pending.json` 并告警。运行方（Agent）应据此闭环：
  1. 读取 `model_profiles.pending.json` 中的模型名；
  2. 用 WebSearch 逐模型联网核实（官方公告 / 模型卡 / Artificial Analysis / Hugging Face）；
  3. 产出 `{模型名: {org, license, commercial, intel_index, hf_avg, cost_in, cost_out, context, multimodal, use_case, source}}` 的 JSON；
  4. 以 `--profiles-json 该JSON` 重新生成——脚本会将其**合并写回** `model_profiles.json`（canonical 实时更新），并自动清除 pending 清单。
- **写入优先级**：`--profiles-json` 合并 > canonical 档案 > 资料卡留空（绝不编造字段）。

### 8.2 新闻源可达性实测（2026-09-10 体检，与排行榜结论相反）

**结论：新闻类（RSS）与排行榜类（网页抓取）的国内可达性完全不同——RSS 目前 14/14 全通。**

逐源裸连实测（国内网络，无代理）：

| 分组 | 实测 | 说明 |
|---|---|---|
| 国内源（7） | **7/7** ✅ | 量子位 / 36氪 / 雷峰网 / 智东西 / 极客公园 / InfoQ 中国 / 钛媒体 |
| 国外源（7） | **7/7** ✅ | TechCrunch / MIT TR / HF Blog / TechMeme / MIT News / VentureBeat / Google AI |

用 `fetch_ai_news.py --check-feeds` 可随时自测，输出按 `cn` / `global` 分区统计，并对失败源直接给「人话建议」。

**本次体检修掉的三个真问题**

| 问题 | 根因 | 修复 |
|---|---|---|
| 36氪 0 条 | URL 缺 `www`，被反爬拦截（200 + HTML，无条目） | 改用 `www.36kr.com/feed`（30 条） |
| 机器之心 0 条 | RSS **已下线**，返回「机器之心·数据服务」落地页 | 替换为**雷峰网 AI 科技评论**（20 条，AI 垂直媒体） |
| VentureBeat 429 | 站点对自报爬虫 UA（`compatible; AIWeeklyReport/4.0`）限流 | 统一改用常规浏览器 UA（常量 `FEED_UA`），即时恢复 200 |

**为什么新闻源没那么脆弱**：RSS 是各站主动对外公开的订阅接口（本来就是给机器读的），不像排行榜网页那样靠 JS 渲染、依赖访问来源。所以「海外源拿不到就等于没有国外信息」在**新闻**这一侧并不成立；真正受限的是**排行榜**（见 § 8.1），而技能对此已有国内源与离线快照兜底。

**仍然存在的边界**（诚实说明）：
- RSS **只保留约 1 周**，回抓 2–3 周前的历史周报只能拿个位数条目，无法忠实复现。
- 源站随时可能改版 / 下线 / 限流（机器之心就是这么没的）。`--check-feeds` 建议每周跑一次。
- 若你的网络确实访问不了某个国外源：其余 13 个源会兜底，报告**不会空白**；这是技能的既定降级路径，无需任何额外配置。

### 8.3 市场数据口径路由：国内优先，国外为可选增强（2026-09-10）

**先说边界：市场数据不是实时抓取的。** 它是运行方用 WebSearch 核实后以 `--market-data` / `--cn-market-data` 等参数注入的**静态快照**（快照日期印在每张图下方）。所以"国内优先"不是说国外源抓不到，而是说**两套数字该信哪个**。

| 口径 | 国内源（可自行核对） | 国外源（可选增强） |
|---|---|---|
| 市场规模 | 中国信通院·中商产业研究院、IDC 中国、艾瑞 | Grand View Research、Statista、Gartner |
| 融资并购 | IT桔子、烯牛数据、新浪创投Plus | Crunchbase、CB Insights |

**`--region cn` 时（或自动探测为国内网络）的处理**：

1. **主口径切到国内**：市场板块顶部插入一条「口径路由条」（服务端预渲染，禁 JS 也可见）——「当前口径：国内优先，中国口径为主；全球口径属海外机构静态快照，仅作趋势对照，国内无法一手核实」。
2. **每张图注标可核实性**：国内源图注加「✅ 国内公开数据，可自行核对」；全球源图注加「🌍 海外机构静态快照 · 作对照」。
3. **不编造**：未注入真实数据时用基准值并在图注标注快照日期，**不伪装成实时**。

**为什么这么设计**：GVR / Crunchbase 这类海外机构数据，国内用户通常无法一手核实（且多位于付费墙之后），把它们和"信通院白皮书面上的数字"标成同等可靠是误导。路由条的作用就是把"该信哪个、哪个只是对照"明写给用户。

### 8.4 英文报道中文翻译：三级取值 + 译文源（2026-09-10）

英文报道的中文总结（`cn_title` / `cn_summary`）按**三级优先级**取值，前两级都**不需要本地模型**：

| 优先级 | 来源 | 前提 | 说明 |
|---|---|---|---|
| 1 | **本地译文缓存** `.translate_cache.json` | 曾在本机翻译过 | 零开销，`src_hash` 校验原文未变 |
| 2 | **远程译文源** `--translations-url` | 能访问 Pages | **没有本地 Ollama 的用户靠这一级**（见下） |
| 3 | **本地 Ollama 实时翻译** `qwen2.5:7b` | 本机装了 Ollama 且在运行 | 约 19s/条（CPU 推理），best-effort |

**三级都落空 → 保留英文原文**，并在结束时的「💡 给你的提示」里说明原因（不会静默）。

> ⚠️ **运营方必读**：历史上有期次（8/24、8/31）因为生成那一刻 Ollama 没运行而**整期没有中文**，且事后无法补救——RSS 只保留约 1 周，原始 `news.json` 回抓不到。**生成前请确认 Ollama 在线，或配置 `--translations-url`。**

#### 远程译文源（给没有本地模型的用户）

每周生成周报时顺带把译文汇总发布到 Pages：

```
https://elisabeth15501.github.io/ai-weekly/translations.json
```

- 格式：`{"schema":"ai-weekly-translations/v1","count":N,"entries":{<原文URL>:{src_hash,cn_title,cn_summary}}}`
- 按**原文 URL** 索引，`src_hash` 校验原文是否变化（变了就视为未命中，避免张冠李戴）
- 拉取失败静默降级，绝不阻断生成

用法：

```bash
python scripts/generate_site.py --api-json news.json -o AI_News.html \
  --translations-url https://elisabeth15501.github.io/ai-weekly/translations.json
```

#### 历史期次回填

已发布的 HTML 若缺译文，可用回填脚本**直接改 HTML 内的 `NEWS_DATA`**（不需要原始 `news.json`）：

```bash
python scripts/backfill_translations.py --check AI_News_*.html        # 只核查
python scripts/backfill_translations.py --no-ollama AI_News_*.html    # 只复用缓存，离线可用
python scripts/backfill_translations.py --emit-source translations.json AI_News_*.html
```

## 九、发布与第三方依赖说明（合规）

本技能**默认不调用任何付费/商业 API**——全部默认数据源都是公开 RSS 订阅接口与公开榜单页面，可安全开源发布（GitHub / Gitee）：

### 9.0 网络访问合规声明（重要）

- **本技能不提供、不指导、也不支持任何规避网络管理措施的能力。** 技能的全部网络行为仅为：读取各站点**主动对外公开**的 RSS 订阅接口与公开榜单页面。
- **数据源默认国内优先**：14 个 RSS 源中国内 7 个、国外 7 个；`--region auto` 会优先选用国内源。海外源不可达时，技能的既定行为是**降级到国内源与随技能附带的离线快照**，并在报告中如实标注数据来源与快照日期——**绝不编造、也绝不为取数而改变网络路径**。
- **`--proxy` / `HTTPS_PROXY` 的定位**：这是**通用的标准 HTTP 客户端参数**（pip / npm / git / curl 等均有），本技能仅为适配「企业内网要求所有出站流量经统一代理」这类常见网络架构而遵循该约定。**它不是为访问任何特定站点而设，也不构成任何规避手段**；公网直连环境无需配置。
- **不做的事**：不内置任何代理服务、不提供代理节点、不指导任何形式的网络访问规避；不使用非公开接口、不破解任何访问控制、不伪造身份绕过鉴权。

- 新闻默认全部来自 14 个公开 RSS 源（国内 7 + 国外 7）；市场/融资图表由运行方通过 WebSearch 注入；排行榜从公开网页（LMArena / Artificial Analysis / Hugging Face / OpenCompass / SuperCLUE / ModelScope 等）自适应抓取，国内兜底快照随技能附带。
- **不内置、不打包任何 AI HOT / 卡兹克的内容**。页脚仅保留基础参考来源链接（Grand View Research / Crunchbase / CB Insights / 中国信通院 / IT桔子 / 新浪创投Plus / Stanford HAI / LMMarketCap），与报告实际引用的 `DEFAULT_*_SOURCE` 保持一致。
- **外部 API 增强是用户 opt-in 的**：技能**默认不调用任何外部商业 API**。两条可选增强路径——① `--news-api` 走 NewsAPI（需自备 `NEWSAPI_KEY`，默认关闭）；② 用户自备 JSON 以 `--external-news-json` 注入 AI HOT 等来源（页脚自动署名）。两条路径都需用户显式开启，是否启用、是否遵守其服务条款均由用户自行决定。AI HOT 的 legacy 接口已于 2026-10-31 停服，取数需改用 v1（`limit`/`window`/`by`）。
- **发布建议**：① 附带 `LICENSE` 文件（如 MIT / Apache-2.0）；② 如需大范围传播，建议提示用户使用外部 API 前先取得授权。
- **跨平台分发**：本技能以单一 `SKILL.md`（开放 Agent Skill 规范）为唯一入口，直接放入支持该规范的任意 Agent 目录即可加载；框架级调用（LangGraph / Dify / Coze）参考 `manifest.json` 的引擎接口描述。无需任何平台专属包装（无 `plugin.json`、无 per-agent 副本）。

### 9.1 内容标识与免责声明（合规）

- **AIGC 标识（必留）**：生成的 HTML 报告**页脚固定展示「本报告由 AI 辅助编制」标识与免责声明**。这是按《生成式人工智能服务管理暂行办法》第十二条对生成内容标识的要求设置的，**转载或二次分发时请保留，不要移除**。
- **不构成投资建议**：报告中的**市场规模、融资额度、公司估值、模型成本**等数据，均为公开来源的**静态快照或折算估算**，仅供信息参考，**不构成任何投资建议**；据此作出决策的风险由使用者自行承担。
- **数据准确性**：每条新闻均附原始报道链接，请以原始来源为准；模型榜单为实时抓取或**标注日期的快照**，不冒充实时；成本栏的外币折算值仅供参考。
- **内容来源**：本技能不生产、不编辑新闻内容，仅对公开 RSS 订阅接口与公开榜单页面做聚合与结构化呈现。

## 十、文件清单


> **目录职责边界**（改东西前先看这里，避免跨目录混放）：
> - `scripts/` = 生成管线（抓取 / 翻译 / 渲染 / 部署），**纯 Python**，所有业务逻辑只在这里改；
> - `assets/` = HTML 模板与静态资源（Chart.js、截图占位），**勿在其中写业务逻辑**，改样式只动这里；
> - `references/` = 独立文档（FAQ / 数据源 / 结构说明），与代码解耦，改说明只动这里；
> - 根目录 `translations_offline.json` = 离线译文包（随技能附带，断网可用），由 `scripts/backfill_translations.py --emit-source` 重新生成。

| 文件 | 用途 |
|------|------|
| `SKILL.md` | 本文件（单一跨平台入口） |
| `manifest.json` | 通用引擎接口描述（框架级调用参考） |
| `assets/news_site_template.html` | v3.0 新闻网站 HTML 模板 |
| `assets/report_template.html` | v2.0 周报模板（保留兼容） |
| `scripts/generate_site.py` | **v3.0** 一键从 API 生成新闻站 |
| `scripts/validate_report.py` | v3.0 质量检查（含 XSS 守护，自动识别 v2/v3 格式） |
| `scripts/fetch_ai_news.py` | 离线 RSS 抓取（备用） |
| `scripts/deploy_report.py` | 部署摘要提取（框架无关通知文本） |
| `scripts/deploy_ghpages.py` | **部署到 GitHub Pages**：git worktree 操作 `gh-pages` 分支，累加根 `index.html` 存档页并推送（底层被 `deploy.py` 调用） |
| `scripts/deploy.py` | **统一部署入口（P0-1）**：按 `--deploy-to` 选后端（github-pages/tencent-cos/vercel/netlify/cloudflare-pages/local），非 GitHub 后端无需配置 GitHub |
| `scripts/validate_models.py` | **模型档案守护（P0-2）**：`--check` 扫描 `model_profiles.json` 有无未核实条目；`--fix` 将无来源推测条目移入 `model_profiles_unverified.json` |
| `scripts/leaderboard_diagnose.py` | **排行榜源探活（P0-3）**：逐个源探测可达性 + 统计国内镜像回退命中 |
| `scripts/install_scheduler.py` | **R4 系统级调度兜底**：注册每日 09:00 刷新任务（Windows 任务计划 / Linux cron），会话不在线也能刷新 |
| `scripts/publish.py` | 组装本周头条 `report.json` 并经飞书连接器推送卡片（`--deploy`/`--deploy-to` 顺带部署） |
| `delivery/feishu_bot.py` | 飞书卡片构造库（`build_headline_card`，纯卡片 schema）；连接器复用 |
| `delivery/feishu_connector.py` | 飞书连接器直推 CLI（lark-cli，密钥不落盘），复用前者的卡片构造 |
| `scripts/init_feishu_config.py` | **飞书配置向导**：交互式生成连接器推送目标 `feishu_target.json`，免去手动建文件 |
| `tools/accumulate_data.py` | 历史数据累积（独立辅助工具，不在主流程） |
| `model_profiles.json` | **canonical 模型资料档案**（按模型名索引，逐条 `verified=true` + 真实来源），每次生成自动加载、新模型研究后合并写回 |
| `model_profiles.pending.json` | 新上榜但档案缺失的模型清单（**运行期生成、不随包分发**；检测为空自动删除；运行方据此联网补档） |
| `model_profiles_unverified.json` | **隔离存放（P0-2）**：被 `validate_models.py` 移出的无来源推测条目，不参与排行榜，待联网核实后回填 |
| `cn_leaderboard_snapshot.json` | 国内排行榜**本地兜底快照**（由 `refresh_snapshot.py` 生成；**不入库、不随包分发**，缺失时降级到 `leaderboard_cache.json`） |

### 10.1 完整模块清单（随包分发的全部文件）

> 上表是**面向使用者**的关键文件说明；下表是**随包分发的完整清单**，用于让「声明的能力范围」与「实际分发的内容」一一对应——避免出现「代码里有、文档里没声明」的模块（这既影响可审计性，也会让自动审核把正常子模块误判为"描述与代码不符"）。
>
> 本清单按 `git archive HEAD --worktree-attributes` 的**实际导出结果**核对（2026-09-24，共 91 个文件），非人工记忆。**不随包分发**的文件见 §10.2。

| 路径 | 用途 |
|---|---|
| `SKILL.md` · `README.md` · `CHANGELOG.md` · `LICENSE` | 入口文档 · 使用说明 · 变更日志 · 许可证（MIT） |
| `manifest.json` | 通用引擎接口描述（框架级调用参考） |
| `requirements.txt` | 运行期依赖（**已钉版本**：feedparser / requests / beautifulsoup4） |
| `run_report.sh` | 一键跑周报的 shell 入口 |
| `translations_offline.json` | 离线译文包（随技能附带，断网可用；由 `backfill_translations.py --emit-source` 重新生成） |
| `model_profiles.json` · `model_profiles_unverified.json` · `model_aliases.json` · `models_cost.json` | 模型资料档案（canonical，逐条带来源）· 无来源推测条目的隔离区 · 别名表 · 成本表 |
| `assets/news_site_template.html` · `assets/report_template.html` · `assets/chart.umd.min.js` | v3.0 新闻站模板 · v2.0 周报模板（保留兼容）· 内联图表库 |
| `scripts/aiweekly/` | **核心引擎包（20 模块）**：`news`（RSS 抓取/解析/分类/去重）· `leaderboard` + `leaderboard_sources` + `leaderboard_fetch` + `leaderboard_checks`（榜单多源抓取/合并/质量校验/资料卡权威覆盖）· `insights`（本周看点聚类 + 受众摘要）· `market`（市场与融资数据）· `render`（HTML 渲染 + XSS 安全序列化）· `translate`（英文报道中文翻译）· `charts_svg`（纯 SVG 图表兜底）· `model_meta`（模型元数据）· `utils`（HTTP 重试退避/出站代理/区域探测/ISO8601）· `const`（硬约束常量）· `errors`（错误码体系）· `health`（源健康检查）· `diagnostics`（错误提示渲染）· `cli_utils`（CLI 公共逻辑）· `canon`（模型名归一化原语，拆解循环依赖的叶子模块）· `leaderboard_snapshot`（榜单时序快照 / 本地缓存 / 国内兜底快照读写）· `market_snapshot`（外置市场快照读取、兜底常量与过期判定） |
| `scripts/validate_checks/` | 产出校验规则包（8 模块，由 `validate_report.py` 导入：结构 / 新闻体量 / 看点 / 市场 / 来源 / 关键词 / 约束） |
| `scripts/generate_site.py` | v3.0 主入口：从 API 数据生成新闻站 |
| `scripts/fetch_ai_news.py` | RSS 抓取（备用离线路径；可选 `--news-api` 走 NewsAPI，需自备 key） |
| `scripts/validate_report.py` | 产出质量校验（含 XSS 守护，自动识别 v2/v3 格式） |
| `scripts/validate_models.py` | 模型档案守护（`--check` 扫描未核实条目 / `--fix` 移入隔离区） |
| `scripts/leaderboard_diagnose.py` | 排行榜源探活（逐个源探测可达性 + 统计镜像回退命中） |
| `scripts/deploy.py` | 统一部署入口（`--deploy-to` 选后端：github-pages/tencent-cos/vercel/netlify/cloudflare-pages/local） |
| `scripts/deploy_ghpages.py` | GitHub Pages 后端（`gh-pages` worktree 操作，**被 `deploy.py` 导入调用**） |
| `scripts/deploy_report.py` | 部署摘要文本提取（框架无关通知文本） |
| `scripts/setup_pages_source.sh` | **GitHub Pages 首次配置脚本**：设置仓库 Pages 源（按 README 指引运行一次；不参与日常生成） |
| `scripts/publish.py` | 组装本周头条 `report.json` 并经飞书连接器推送卡片 |
| `scripts/init_feishu_config.py` | 飞书连接器配置向导（交互式生成推送目标） |
| `scripts/install_scheduler.py` | R4 系统级调度：注册每日 09:00 刷新任务（**以子进程调用 `refresh_deploy.py`**） |
| `scripts/refresh_deploy.py` | 每日刷新周报站（**由 `install_scheduler.py` 调用**；会话不在线也生效） |
| `scripts/refresh_snapshot.py` | 刷新国内榜源兜底快照 `cn_leaderboard_snapshot.json`（**手动运行**，无自动调用方） |
| `scripts/mirror_build.py` | 镜像站构建（**被 `build_pages_site.py` 引用**） |
| `scripts/build_pages_site.py` | 在 CI 内生成周报站并产出 Pages artifact（**由 `.github/workflows/mirror.yml` 调用**） |
| `scripts/backfill_translations.py` | 离线译文包回填（`--emit-source` 重新生成 `translations_offline.json`） |
| `tools/accumulate_data.py` | 历史数据累积（独立辅助工具，不在主流程） |
| `delivery/feishu_bot.py` · `delivery/feishu_connector.py` · `delivery/__init__.py` | 飞书卡片构造库 · 连接器直推（lark-cli，密钥不落盘） |
| `delivery/deploy_config.example.json` · `delivery/feishu_target.example.json` | 部署与飞书连接器目标**示例文件**（用户据此生成真实配置，示例本身不含凭据） |
| `delivery/sample_report.json` · `delivery/v3.4.6_release_notes.md` | 示例报告 · 历史发布说明 |
| `references/FAQ.md` · `references/data_sources.md` · `references/report_structure.md` · `references/SKILL_full.md` | 常见问题集中解答 / 备用数据源 / v2.0 报告结构 / **SKILL.md 完整版（精简版的展开文档，同仓库 GitHub）** |
| `releases/` | 19 个历史版本的发布说明（归档用，反映逐版真实改动） |
| `.github/workflows/ci.yml` · `.github/workflows/mirror.yml` | 单测 + 语法门禁 + 样张生成再校验 · 每日刷新榜源与周报站 |

**运行期生成（不随包分发，首次运行或按需创建）**：`delivery/feishu_target.json`（配置向导产出，含真实推送目标，永不入库）· `model_profiles.pending.json`（待补档清单，为空自动删除）· `cn_leaderboard_snapshot.json`（本地兜底快照，缺失时降级到 `leaderboard_cache.json`）· `index.html` / `report.json` / `public/`（生成与部署产物）。

### 10.2 不随包分发的文件（发布裁剪，附理由）

> 下列**路径模式**不进入发布包（其中部分为开发者本地预留路径，当前仓库内可能不存在）。单列此节是为了让「声明面」与「分发面」严格互补——避免自动审核把仓库内文件与发布包逐一比对时产生歧义。
> 裁剪由两条通道实施：`.gitattributes` 的 `export-ignore`（SkillHub 的 `git archive` 通道）与 `.clawhubignore`（ClawHub 通道）。

| 路径 | 理由 |
|---|---|
| `scripts/aiweekly/tests/` | 单元测试与离线 fixture，仅供 CI 与本地 `pytest` |
| `scripts/conftest.py` | pytest 配置，仅测试期需要 |
| `scripts/compliance_check.py` | **发布者自用的发布前合规门禁**（属"发布流程"而非"用户能力"；规则表为明文词表，不随包分发） |
| `.gitignore` · `.clawhubignore` · `.gitattributes` | 仓库与发布工具配置；SkillHub 亦将其判为不允许的文件类型 |
| `data/` · `docs/` | 开发者本地数据与参考文档；**按路径模式排除，当前仓库内可能为空或不存在（预留）** |
| `clean_code_audit_generate_site.md` | 发布者本地的一次性代码审计记录（`.gitignore:8`） |
| `__pycache__/` · `*.pyc` · `*.pyo` | Python 字节码 |
| `openclaw-edition/` · `*.skill` | 本地打包产物 |
| `delivery/feishu_target.json` · `.github_token` | **含真实凭据，绝不入库**（`.gitignore` 已覆盖） |

## 参考资料

- **[references/data_sources.md](references/data_sources.md)** — 备用 / 候选数据源清单
- **[references/report_structure.md](references/report_structure.md)** — v2.0 报告结构参考
- **[manifest.json](manifest.json)** — 通用引擎接口（框架级调用）

> 说明：发布者本地曾有一份 Agent 技能格式格局调研（`docs/`），因**不随包分发**（见 §10.2），此处不再提供链接，避免发行包内出现死链。
