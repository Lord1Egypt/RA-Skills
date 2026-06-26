---
name: code-analysis
license: MIT
description: >
  This skill should be used when the user needs to analyze Git repositories,
  compare developer commit patterns, work habits, development efficiency,
  code style, code quality, and slacking behaviors. It generates honest,
  direct developer evaluations with scores, grades, strengths, weaknesses,
  and actionable suggestions. Trigger phrases include "analyze code",
  "analyze repository", "compare developers", "code quality report",
  "commit patterns", "developer efficiency", "developer evaluation",
  "slacking index", "摸鱼指数", "工作习惯分析", "代码分析",
  "研发效率", "代码质量", "开发者评估", "developer score".
---

# 代码分析技能

📦 **GitHub**: [https://github.com/Wscats/code-analysis-skills](https://github.com/Wscats/code-analysis-skills)

扫描指定仓库或目录下所有 Git 仓库，分析并对比开发者的提交习惯、工作习惯、研发效率、代码风格、代码质量和摸鱼指数，对每个开发者进行严肃、直接的评估打分，生成结构化分析报告（支持 Markdown / HTML / JSON / PDF）。

## 💬 自然语言对话（推荐）

你不需要记住任何命令——直接用你熟悉的语言描述你的需求即可：

### 🇨🇳 中文

```
💬 "分析一下这个仓库 Alice 的研发效率"
💬 "帮我看看团队成员的工作习惯"
💬 "对比一下 Alice 和 Bob 的代码质量"
💬 "看看这个项目的摸鱼指数"
💬 "给所有开发者做个完整评估打分"
💬 "谁的代码质量最差？帮我分析下"
💬 "最近一个月团队的提交习惯怎么样？"
💬 "这个仓库有什么问题？帮我诊断下"
```

### 🇺🇸 English

```
💬 "Analyze Alice's development efficiency in /path/to/repo"
💬 "Show me the team's work habits in this project"
💬 "Compare Alice and Bob's code quality"
💬 "What's the slacking index of this project?"
💬 "Generate a full developer evaluation report"
💬 "Score all developers and tell me who's slacking"
💬 "What's wrong with Bob's commit habits?"
💬 "Here's my repo, can you analyze the team?"
```

### 🇯🇵 日本語

```
💬 "このリポジトリの開発者効率を分析してください"
💬 "チームメンバーの作業習慣を見せてください"
💬 "AliceとBobのコード品質を比較してください"
💬 "このプロジェクトのサボり指数は？"
💬 "全開発者の評価レポートを作成してください"
```

### 🇰🇷 한국어

```
💬 "이 레포지토리의 개발 효율성을 분석해줘"
💬 "팀원들의 작업 습관을 보여줘"
💬 "Alice와 Bob의 코드 품질을 비교해줘"
💬 "이 프로젝트의 땡땡이 지수가 뭐야?"
💬 "모든 개발자에 대한 평가 보고서를 만들어줘"
```

### 🇪🇸 Español

```
💬 "Analiza la eficiencia de desarrollo de Alice en este repositorio"
💬 "Muéstrame los hábitos de trabajo del equipo"
💬 "Compara la calidad del código de Alice y Bob"
💬 "¿Cuál es el índice de holgazanería de este proyecto?"
💬 "Genera un informe de evaluación completo de los desarrolladores"
```

### 🇫🇷 Français

```
💬 "Analyse l'efficacité de développement d'Alice dans ce dépôt"
💬 "Montre-moi les habitudes de travail de l'équipe"
💬 "Compare la qualité du code d'Alice et de Bob"
💬 "Quel est l'indice de paresse de ce projet ?"
💬 "Génère un rapport d'évaluation complet des développeurs"
```

### 🇩🇪 Deutsch

```
💬 "Analysiere die Entwicklungseffizienz von Alice in diesem Repository"
💬 "Zeig mir die Arbeitsgewohnheiten des Teams"
💬 "Vergleiche die Codequalität von Alice und Bob"
💬 "Was ist der Faulenzer-Index dieses Projekts?"
💬 "Erstelle einen vollständigen Bewertungsbericht für alle Entwickler"
```

> **注意**：你需要提供仓库路径（`repo_path`），这是必填参数。如果你已经在某个仓库上下文中工作，代理可能会从对话中推断路径，但建议始终明确指定路径以确保准确性。

Skill 能理解上述所有语言。只需描述你的需求，它就会对你的仓库执行分析并返回结构化报告。

---

## 🚀 快速开始（CLI 命令行）

### 安装依赖

```bash
pip install gitpython pydriller radon tabulate jinja2 click reportlab
```

如需更高质量的 PDF 输出（可选）：

```bash
pip install weasyprint   # 推荐，需要系统安装 cairo 库
# 或
pip install pdfkit       # 需要系统安装 wkhtmltopdf
```

### 常用命令

```bash
# 分析单个仓库（所有贡献者）
python -m src.main -r /path/to/repo

# 扫描目录下所有仓库
python -m src.main -r /path/to/projects --scan-all

# 对比指定开发者
python -m src.main -r /path/to/repo -a "Alice" -a "Bob"

# 指定时间范围 + HTML 输出
python -m src.main -r /path/to/repo -s 2024-01-01 -u 2024-12-31 -f html -o report.html

# 同时生成 Markdown + HTML + PDF
python -m src.main -r /path/to/repo -f "markdown,html,pdf" -o report

# 仅生成 PDF 报告
python -m src.main -r /path/to/repo -f pdf -o report.pdf

# 保存报告到文件
python -m src.main -r /path/to/repo -o report.md
```

### CLI 参数一览

| 参数 | 缩写 | 说明 | 默认值 |
|------|------|------|--------|
| `--repo-path` | `-r` | Git 仓库路径或父目录 | 必填 |
| `--scan-all` | | 递归扫描所有 `.git` 仓库 | `false` |
| `--author` | `-a` | 按作者过滤（可重复使用） | 全部作者 |
| `--since` | `-s` | 起始日期（ISO 格式） | 无 |
| `--until` | `-u` | 截止日期（ISO 格式） | 无 |
| `--branch` | `-b` | 分析的分支 | 当前活跃分支 |
| `--format` | `-f` | 输出格式：`markdown`、`json`、`html`、`pdf`（逗号分隔支持多格式） | `markdown` |
| `--output` | `-o` | 输出文件路径 | 标准输出 |

---

## 使用场景

- 当用户需要分析某个 Git 仓库的开发者行为时
- 当用户需要对比团队成员的提交习惯和研发效率时
- 当用户需要了解代码质量趋势和代码风格一致性时
- 当用户需要扫描目录下所有 `.git` 仓库进行批量分析时
- 当用户需要生成开发者工作习惯报告（工作时段、周末加班、深夜编码等）时
- 当用户需要评估每个开发者的综合能力并给出评分、优缺点和建议时
- 当用户想查看团队的"摸鱼指数"排行榜时
- 当用户需要 PDF 格式的正式报告时

## 工作流程

### 步骤 1: 确认分析参数

询问用户以下信息：
- **仓库路径**: 单个 Git 仓库路径，或包含多个仓库的父目录
- **分析范围**: 是否扫描目录下所有 `.git` 仓库（`--scan-all`）
- **目标作者**: 指定分析特定开发者（可多选），或分析全部贡献者
- **时间范围**: 可选的起止日期（ISO 格式，如 `2024-01-01`）
- **分支**: 指定分析的分支，默认为当前活跃分支
- **输出格式**: `markdown`（默认）、`json`、`html`、`pdf`，或逗号分隔的多格式组合

### 步骤 2: 执行分析

使用确认的参数执行分析脚本（参见上方"快速开始"中的命令示例）。

### 步骤 3: 解读报告

分析报告包含以下七个维度，逐一向用户解读关键发现：

1. **🏆 开发者评估** — 综合评分（S/A/B/C/D/E/F）、优点、缺点、改进建议、一句话定论
2. **🐟 摸鱼指数** — 活跃度、琐碎提交率、消失比率、低产出、拖延症等信号评分
3. **📝 提交习惯** — 提交频率、提交大小、merge 比率、消息质量
4. **⏰ 工作习惯** — 工作时段分布、周末/深夜编码比例、连续编码天数
5. **🚀 研发效率** — 代码流失率(churn)、返工率(rework)、Bus Factor、文件所有权
6. **🎨 代码风格** — 语言分布、Conventional Commits 遵循率、文件分类
7. **🔍 代码质量** — Bug Fix 比率、Revert 频率、大提交比例、测试覆盖、复杂度

如果有多位开发者，额外提供：
- 📋 横向对比摘要表
- 🏆 开发者评分排行榜
- 🐟 摸鱼指数排行榜

### 步骤 4: 深入解读评估结果

对每位开发者的评估，用严肃、直接的语气向用户解读：

1. **评分与等级**: 总分(0-100)和对应等级(S/A/B/C/D/E/F)
2. **六大维度得分**: 提交纪律、工作一致性、效率、代码质量、代码风格、参与度
3. **优点**: 每条都有数据支撑，具体而非泛泛
4. **缺点**: 不粉饰，直指问题本质和影响
5. **建议**: 可操作的改进措施，每条都能立即执行
6. **摸鱼指数**: 解读各个信号及其含义

## 可用资源

### 脚本

- `src/main.py` — 主入口脚本，支持 CLI 参数，编排全部分析流程并生成报告
- `src/scanner.py` — 仓库扫描器，发现单个或递归扫描多个 Git 仓库
- `src/analyzers/base_analyzer.py` — 分析器基类，提供 Git 历史遍历和作者过滤
- `src/analyzers/commit_analyzer.py` — 提交习惯分析（频率、大小、消息质量）
- `src/analyzers/work_habit_analyzer.py` — 工作习惯分析（时段、周末、深夜、连续天数）
- `src/analyzers/efficiency_analyzer.py` — 研发效率分析（churn、rework、bus factor）
- `src/analyzers/code_style_analyzer.py` — 代码风格分析（语言分布、commit 规范）
- `src/analyzers/code_quality_analyzer.py` — 代码质量分析（bug fix、revert、复杂度）
- `src/analyzers/slacking_analyzer.py` — 摸鱼指数分析（活跃度、琐碎提交、消失模式、拖延症等）
- `src/evaluator/developer_evaluator.py` — 开发者评估引擎（综合评分、优缺点、建议、定论）
- `src/reporters/markdown_reporter.py` — Markdown 格式报告生成器
- `src/reporters/json_reporter.py` — JSON 格式报告生成器
- `src/reporters/html_reporter.py` — HTML 格式报告生成器（含丰富的可视化样式）
- `src/reporters/pdf_reporter.py` — PDF 格式报告生成器（支持 weasyprint/pdfkit/reportlab）

### 参考文档

- `references/metrics-guide.md` — 各指标含义、计算方式和健康值参考范围。当用户询问某个指标的含义时，读取此文件。

## ⚠️ 隐私与数据安全声明

> **重要提示**：本工具会从 Git 提交历史中提取开发者个人活动数据，包括但不限于：
> - 提交时间戳（精确到小时）
> - 周末/深夜编码频率
> - 个人提交频率和产出量
> - 代码所有权归属
> - 摸鱼指数等行为评估

**使用前请务必遵守以下原则：**

1. **知情同意** — 在分析他人仓库之前，必须获得相关开发者的知情同意
2. **非惩罚性** — 分析结果**不应**直接用于绩效考核、薪酬决策或惩罚性管理
3. **上下文理解** — 数据需结合实际工作场景理解（如架构师天然提交少，不代表产出低）
4. **数据保护** — 生成的报告包含个人信息，应妥善保管，不应公开分享
5. **合规性** — 使用前请确认符合所在组织的 HR 政策和当地数据保护法规（如 GDPR）
6. **本地运行** — 本工具完全本地运行，不会向外部服务器传输任何数据

## 评估体系说明

### 综合评分 (0-100)

| 等级 | 分数范围 | 含义 |
|------|----------|------|
| S | 90-100 | 顶级贡献者，各方面表现出色 |
| A | 80-89 | 优秀开发者，可靠且高效 |
| B | 70-79 | 扎实的贡献者，有少量改进空间 |
| C | 60-69 | 合格，但需要在多个方面提升 |
| D | 50-59 | 勉强及格，有明显短板 |
| E | 35-49 | 低于预期，需要严肃对待 |
| F | 0-34 | 严重问题，需要辅导或谈话 |

### 六大维度权重

| 维度 | 权重 | 评估内容 |
|------|------|----------|
| 📝 提交纪律 | 15% | 提交频率、消息质量、规范遵循 |
| ⏰ 工作一致性 | 15% | 作息规律、工作连续性 |
| 🚀 效率 | 20% | 代码流失率、返工率、产出量 |
| 🔍 代码质量 | 25% | Bug修复率、回滚率、测试覆盖、复杂度 |
| 🎨 代码风格 | 10% | Conventional Commits、Issue引用 |
| 💪 参与度 | 15% | 摸鱼指数的反向指标 |

### 摸鱼指数 (0-100)

| 等级 | 分数范围 | 含义 |
|------|----------|------|
| 🔥 工作狂 | 0-20 | 高度投入，持续贡献 |
| ✅ 正常 | 21-40 | 健康的工作模式 |
| 😏 有嫌疑 | 41-60 | 检测到部分摸鱼信号 |
| 🐟 摸鱼达人 | 61-80 | 显著的低参与指标 |
| 🏆 摸鱼大师 | 81-100 | 职业摸鱼选手 |

## 注意事项

- 分析大型仓库（10万+提交）时可能耗时较长，建议限定时间范围
- Python 代码复杂度分析依赖 `radon` 库，仅对 `.py` 文件生效
- 作者匹配支持模糊匹配（名称或邮箱包含关键字即可）
- 扫描目录时默认最大深度为 5 层，避免过深递归
- PDF 生成优先使用 weasyprint，回退到 pdfkit，最终回退到 reportlab
- 评估结果仅基于 Git 提交历史数据，不代表开发者的全部能力
- 摸鱼指数仅供参考，需结合实际工作场景理解
- **本工具完全本地运行，不会向任何外部服务器发送数据**
- **在分析团队仓库前，请务必获得相关人员知情同意**
- **报告结果不应直接用于绩效考核或惩罚性管理决策**

... EOF
