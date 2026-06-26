# Competitive-Ops v2

Claude Code 的 AI 竞争情报分析工具。

<p align="center">
  <a href="https://github.com/anthropics/claude-code">
    <img src="https://img.shields.io/badge/Claude_Code-000?style=flat&logo=anthropic&logoColor=white" alt="Claude Code">
  </a>
  <a href="https://github.com/nextlevelbuilder/ui-ux-pro-max-skill">
    <img src="https://img.shields.io/badge/Design_System-ui--ux--pro--max-blue?style=flat" alt="UI UX Pro Max">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License">
  </a>
</p>

---

## 这是什么

Competitive-Ops 是一个 **Claude Code Skill** — 可通过 `/competitive-ops` 或自然语言触发（如"分析 Anthropic"），将 Claude Code 变成**竞争情报指挥中心**。

### 解决的痛点

- **无历史沉淀** — 基于 ChatGPT 的调研每次会话从零开始，竞品洞察随对话结束而消失
- **变化检测盲区** — 定价调整、产品发布、市场动向需人工重新调研才能发现
- **输出结构混乱** — 非结构化分析导致难以聚合、对比或趋势追踪
- **被动应急姿态** — 竞争情报停留在救火阶段，缺乏系统化、持续化的监控机制

### 功能

- **结构化分析** — SWOT 框架 + 六维评分，支持行业特定模板
- **专业报告输出** — Markdown 和 HTML 报告，内置 ECharts 可视化
- **自动变化检测** — 任何定价变化立即告警（无阈值），功能变化长期追踪
- **横向竞品对比** — 多竞品矩阵分析，评分 delta 变化
- **批量智能处理** — 多智能体并行（~3x 提速），每个 agent 独立上下文（避免污染）
- **定价深耕** — 价值评分（功能数/价格）配合市场标准化因子

---

## 快速开始

### 1. 安装

```bash
# 克隆仓库
git clone https://github.com/dalianmao000/competitive-ops-v2.git
cd competitive-ops-v2

# 安装 Python 依赖
pip install -r requirements.txt
```

### 2. 配置 API Key（可选）

```bash
# 添加到环境变量或 .env 文件
export TAVILY_API_KEY="tvly-xxxxx"
```

在 [tavily.com](https://tavily.com) 获取 API key。或者如果已配置 Claude Code 的 Tavily MCP server，则无需设置。

### 3. 在 Claude Code 中使用

```bash
# 添加竞品
/competitive-ops add Anthropic

# 完整分析 + HTML 报告
/competitive-ops analyze Anthropic

# 对比两个竞品
/competitive-ops compare Anthropic vs OpenAI

# 检查定价变化
/competitive-ops pricing Anthropic

# 批量处理（支持 tier 1/2/3 过滤）
/competitive-ops batch tier 1

# 查看追踪面板
/competitive-ops track

# 生成综合报告
/competitive-ops report
```

---

## 功能

### 命令

| 命令 | 说明 |
|------|------|
| `/competitive-ops setup` | 安装依赖并配置系统 |
| `/competitive-ops add <公司>` | 添加竞品到追踪列表 |
| `/competitive-ops analyze <公司>` | 完整分析：SWOT + 评分 + HTML 报告 |
| `/competitive-ops compare <A> vs <B>` | 横向功能矩阵对比 |
| `/competitive-ops update <公司>` | 检查自上次分析以来的变化 |
| `/competitive-ops pricing <公司>` | 定价研究 + 变化检测 |
| `/competitive-ops pricing-deep-dive <公司>` | 定价深耕 + 价值评分 |
| `/competitive-ops batch` | 批量处理多个竞品（支持 tier 1/2/3 过滤） |
| `/competitive-ops report` | 生成综合报告 |
| `/competitive-ops track` | 查看追踪面板 |
| `/competitive-ops monitor [daily\|weekly\|monthly]` | 设置定时监控（使用 /loop 持续更新） |
| `/competitive-ops pdf [报告]` | 导出报告为 PDF（使用 Playwright） |
| `/competitive-ops png [报告]` | 导出报告为 PNG 图片（使用 Playwright） |

### 评分系统

6 个维度评估竞品（1-5 分制）：

| 维度 | 权重 |
|------|------|
| 产品成熟度 | 20% |
| 功能覆盖 | 20% |
| 定价 | 15% |
| 市场存在 | 15% |
| 增长轨迹 | 10% |
| 品牌实力 | 10% |

### 原型分类

将竞品分类为：

- **直接竞争** — 相同产品，相同市场
- **间接竞争** — 不同方案，相同需求
- **新兴威胁** — 新技术，新模式
- **替代威胁** — 替代解决方案
- **邻近玩家** — 用户重叠
- **参考基准** — 行业标杆

### 置信度

多源交叉验证：

| 级别 | 条件 |
|------|------|
| 🟢 高 | 3+ 个来源一致 |
| 🟡 中 | 2 个来源一致 |
| 🔴 低 | 数据冲突或不足 |

### 行业模板

行业特定的 SWOT 分析框架和评分权重：

| 行业 | 重点 | 关键指标 |
|------|------|---------|
| AI（默认） | 模型能力、API 定价 | Tokens/$、上下文窗口 |
| SaaS | MRR、流失率、NPS | 净收入留存、集成数 |
| FinTech | 合规、安全 | 交易量、欺诈率 |

在 `config/profile.yml` 中配置：
```yaml
company:
  industry: "saas"  # ai、saas 或 fintech
```

### 定价追踪单点深耕

追踪竞品定价变化，带价值评分：

```bash
/competitive-ops pricing-deep-dive Anthropic
```

- **价值评分** = (功能数 / 价格) × 市场标准化因子
- **任何定价变化都会触发告警**（无阈值）
- 快照存储在 `data/pricing-snapshots/{company}.json`

---

## 项目结构

```
competitive-ops-v2/
├── CLAUDE.md                        # 项目说明
├── cv.md                           # 你的产品定义（用户层）
├── config/
│   ├── profile.yml                # 公司/产品配置（用户层）
│   └── industry-profiles.yml      # 行业配置（AI/SaaS/FinTech）
├── .claude/skills/competitive-ops/ # Skill 定义
│   ├── SKILL.md                   # 路由 + 各模式定义
│   └── modes/                    # 模式实现
├── scripts/                        # Python 工具
│   └── pricing_analyzer.py        # 价值评分 + 变化检测
├── templates/
│   └── report/
│       └── markdown/              # 报告模板
│           ├── swot-template-ai.md
│           ├── swot-template-saas.md
│           ├── swot-template-fintech.md
│           └── pricing-deep-dive-template.md
├── modes/
│   ├── _industry-context.md      # 行业特定 SWOT 问题
│   ├── _shared.md                # 共享规则和评分
│   ├── _profile.md              # 用户自定义
│   ├── add.md, analyze.md, batch.md, compare.md
│   ├── pricing.md, pricing-deep-dive.md, report.md
│   ├── track.md, update.md, monitor.md, pdf.md, png.md
├── data/
│   ├── competitors.md              # 竞品追踪表
│   ├── batch-queue.md             # 批处理队列
│   ├── batch-status.json          # 批处理状态
│   ├── pricing-snapshots/         # JSON 定价快照
│   │   └── {company}.json
│   ├── reports/
│   │   ├── {date}/              # 按日期归档
│   │   └── latest/               # 最新报告 symlink
│   └── snapshots/                 # 历史快照
└── exports/                        # PNG/PDF 导出
    └── index-{date}.png
```

---

## 报告输出示例

### 报告文件结构

报告按日期归档，`latest/` 提供 symlink 方便访问：

```
data/reports/
├── 2026-04-07/
│   ├── anthropic-2026-04-07.md
│   ├── openai-2026-04-07.md
│   └── consolidated-2026-04-07.md   # 综合报告
├── latest/
│   ├── anthropic.md → ../2026-04-07/anthropic-2026-04-07.md
│   └── openai.md → ../2026-04-07/openai-2026-04-07.md
└── html/
    ├── index.html                   # 综合 HTML
    └── anthropic-2026-04-07.html   # 单个 HTML 报告
```

### Markdown 报告

```markdown
# 竞争分析：Anthropic

**日期：** 2026-04-07
**层级：** Tier 1（直接竞争）
**综合评分：** 79.6 / 100
**置信度：** 高（多源验证）

## 评分矩阵

| 维度 | 评分 | 权重 | 加权分 |
|------|------|------|--------|
| 产品成熟度 | 4.6 | 20% | 0.92 |
| 功能覆盖 | 4.6 | 20% | 0.92 |
| 定价 | 4.3 | 15% | 0.645 |
| 市场存在 | 4.1 | 15% | 0.615 |
| 增长轨迹 | 4.5 | 10% | 0.45 |
| 品牌实力 | 4.3 | 10% | 0.43 |
| **合计** | | **100%** | **3.98 → 79.6** |
```

### HTML 报告

专业响应式 HTML 报告，采用 Tailwind dark theme：
- 评分概览卡片
- 带进度条的评分矩阵
- 四象限 SWOT 分析
- 关键发现与风险评估
- 含所有竞品对比的综合索引页
- **ECharts 交互图表：**
  - 综合评分排名柱状图
  - 六维能力雷达图
  - API 定价格局热力图
- **定价变化 Alert** 带 🔴 变化徽章

### PDF 导出

导出报告用于外部分享：
```bash
node scripts/export_pdf.js data/reports/html/index.html
```
- 使用 Playwright 等待 ECharts 渲染
- A4 格式，15mm 边距
- 页脚含页码
- CSS page-break 控制防止分页打断

### PNG 导出

导出报告为高清图片：
```bash
node scripts/export_image.js data/reports/html/index.html
node scripts/export_image.js data/reports/html/index.html --full  # 全页截图
node scripts/export_image.js data/reports/html/index.html --jpeg   # JPEG 格式
```
- ECharts 完整渲染
- 保留深色背景
- 默认 PNG，支持 JPEG
- 支持视口或全页截图

---

## 数据隐私

- **本地优先**：所有数据存储在项目目录
- **无外部 API**：除非你同意（Tavily 是可选的）
- **用户层**：你的 CV、配置、追踪数据不会共享
- **系统层**：Skill 模式可更新但不会覆盖你的配置

---

## License

MIT — 可自由使用、修改和分发。

---

## 相关

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) — AI 编程助手
