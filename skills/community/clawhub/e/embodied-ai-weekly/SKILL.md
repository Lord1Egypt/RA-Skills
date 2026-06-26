---
name: embodied-ai-weekly
description: "具身智能周报自动化生成与发布技能。当用户需要生成具身智能领域一周动态报告时使用，覆盖完整工作流：ArXiv论文多方向检索与整理、GitHub开源项目趋势追踪、综合可视化HTML报告生成（含导读+统计图表），以及将报告推送到 GitHub Pages 仓库发布。适用于每周定期生成具身智能领域动态报告的场景。"
---

# Embodied AI Weekly 具身智能周报生成 Skill

## 概述

本 Skill 封装了具身智能周报从「信息检索」到「报告生成」再到「GitHub 发布」的完整 SOP，分三个阶段：

1. **Phase 1 — ArXiv 论文检索**：按 7 个研究方向检索最新论文
2. **Phase 2 — GitHub 开源项目检索**：按 7 个方向追踪新增仓库与经典仓库动态
3. **Phase 3 — 综合报告生成与发布**：整合两部分内容，生成 Markdown + HTML 综合报告并推送至 GitHub

---

## Phase 1 — ArXiv 论文检索

### 检索策略

使用 `web_fetch` 工具逐一检索 7 个方向，每个方向独立请求。参考 `references/arxiv_search_guide.md` 获取各方向的检索关键词与 API URL 模板。

**API URL 模板：**
```
https://arxiv.org/search/?query=<KEYWORDS>&searchtype=all&start=0&order=-announced_date_first
```

或使用 arXiv 官方 RSS / cs.RO 分类页面：
```
https://arxiv.org/list/cs.RO/recent
https://arxiv.org/list/cs.CV/recent
```

### 检索方向（共 7 个）

每个方向的详细关键词见 `references/arxiv_search_guide.md`：

| 序号 | 方向 | 核心关键词（示例） |
|------|------|-------------------|
| 1 | 具身感知与场景理解 | egocentric perception, affordance, 3D scene graph |
| 2 | 具身决策与规划 | embodied planning, LLM robot, TAMP, long-horizon |
| 3 | 具身控制与操作 | dexterous manipulation, diffusion policy, visuomotor |
| 4 | 具身强化学习与世界模型 | embodied RL, world model robot, sim-to-real |
| 5 | 具身智能体与大模型 | VLA, vision-language-action, OpenVLA, LLM robotics |
| 6 | 仿真、数据与平台 | robotic simulation, embodied benchmark, x-embodiment |
| 7 | 人机交互与具身社会智能 | human-robot interaction, shared autonomy, HRI |

### 输出格式

为每篇论文整理以下字段：
- 标题（中英对照）
- ArXiv 链接
- 作者与机构
- 核心贡献（200字以内）
- 方向标签

生成文件：`embodied_ai_weekly_arxiv_<YEAR>_w<WEEK>.md` 和对应 `.html`

---

## Phase 2 — GitHub 开源项目检索

### 检索策略

使用 `web_fetch` 工具，检索两类仓库：
- **新增仓库**：`created:>YYYY-MM-DD`（过去7天），按 stars 排序
- **经典仓库**：`pushed:>YYYY-MM-DD`，关注有重要更新的高星仓库

**GitHub API URL 模板：**
```
https://api.github.com/search/repositories?q=<KEYWORDS>&sort=stars&order=desc&per_page=10
```

> ⚠️ 注意：GitHub API 对 OR 运算符有限制（最多 5 个），需要拆分查询。若 API 超时，改用 GitHub 网页搜索：`https://github.com/search?q=<KEYWORDS>&type=repositories&s=updated&order=desc`

### 检索方向

与 ArXiv 对应的 7 个方向，详见 `references/github_search_guide.md`

### 输出格式

每个仓库整理：
- 仓库名 + GitHub 链接
- 简介（50字内）
- Stars 数量
- 是否为本周新增 / 经典更新
- 所属方向

生成文件：`embodied_ai_weekly_github_<YEAR>_w<WEEK>.md` 和对应 `.html`

---

## Phase 3 — 综合报告生成与发布

### 3.1 综合 Markdown 报告

读取 Phase 1 和 Phase 2 的 `.md` 文件，整合为一份综合报告，结构如下：

```
# 具身智能深度周报 <YEAR>-W<WEEK>
> 报告周期：<DATE_START> ~ <DATE_END>

## 📖 一周导读
- 快速导航（7方向跳转链接）
- 本周 Top 5 必读（论文 + 项目）
- 核心趋势卡片（5大趋势）
- 开放问题（4个待关注点）

## 📊 数据总览
- 论文方向分布表格
- GitHub 仓库统计表格
- 每日发表趋势

## 📄 ArXiv 论文精选
（7方向，每方向列出所有检索论文，精选论文配 ArXiv 原文 figure）

## 🐙 GitHub 开源项目
（新建仓库精选 + 经典仓库重点更新，配项目截图）

## 💡 核心洞察
（5大趋势分析 + 下周关注点）
```

生成文件：`embodied_ai_weekly_report_<YEAR>_w<WEEK>.md`

### 3.2 论文配图获取

报告需要配图来增强可读性。配图来源为 ArXiv 论文原文和 GitHub 项目页面，**禁止使用 AI 生成图片**。

**图片获取策略：**

1. **ArXiv 论文图片**：使用 Playwright 或直接 HTTP 请求访问论文 HTML 版本，下载其中的 figure 图片
   - HTML 版本 URL 模板：`https://arxiv.org/html/<ARXIV_ID>v<VERSION>/`
   - 图片通常为 `x1.png`、`x2.png` 等命名
   - 可直接用 HTTP 下载：`https://arxiv.org/html/<ARXIV_ID>v<VERSION>/x1.png`
   - 保存到工作区 `images/` 目录

2. **GitHub 项目截图**：使用 Playwright 对 GitHub 仓库页面进行截图
   - 截取 README Banner 或项目首页区域
   - 保存到 `images/` 目录

3. **论文项目页截图**：部分论文有配套项目页（如 `https://faceong.github.io/CoEnv/`），可直接截图

**图片嵌入位置：**
- **封面区（Hero）**：选择当周最重要/最热门的论文项目页截图
- **精选论文卡片**：每篇精选论文配 1-2 张 ArXiv 原文 figure
- **GitHub 热榜卡片**：配 GitHub 仓库截图
- 每张图片附带 `<figcaption>` 注明来源链接

**批量下载脚本示例（Node.js + Playwright）：**

```javascript
const { chromium } = require('playwright');
// 使用 Playwright 截图 GitHub 页面
// 使用 fetch/axios 下载 ArXiv 论文图片
// 保存到 images/ 目录
```

**图片 CSS 样式（添加到 HTML 内联样式）：**

```css
.paper-figure { margin: 14px 0; border-radius: 10px; overflow: hidden; border: 1px solid var(--border); }
.paper-figure img { width: 100%; display: block; max-height: 400px; object-fit: contain; background: #fff; }
.paper-figure figcaption { padding: 8px 14px; font-size: 11px; color: var(--text3); text-align: center; }
.hero-figure { margin: 30px auto; max-width: 900px; border-radius: 16px; overflow: hidden; box-shadow: 0 8px 40px rgba(99,102,241,.15); }
.hero-figure img { width: 100%; display: block; }
.github-figure { margin: 12px 0; border-radius: 8px; overflow: hidden; border: 1px solid var(--border); }
.github-figure img { width: 100%; display: block; max-height: 320px; object-fit: cover; }
```

### 3.3 综合 HTML 可视化报告

HTML 报告的视觉风格参考 `references/html_template_guide.md`。

**必须包含的模块：**

1. **Header Hero 区**：渐变标题 + 报告日期 + Executive Summary + 封面图
2. **Stats Cards 数据卡片**：论文数、GitHub 仓库数、方向数等
3. **ArXiv 分布条形图**：使用 Chart.js 或纯 CSS 条形图展示7方向论文分布
4. **论文卡片区**：Top 3-5 精选论文深度解读 + 每篇配图 + 完整论文表格（可折叠）
5. **GitHub 热榜**：Top 3 仓库卡片 + 仓库截图 + 全方向仓库矩阵
6. **核心洞察区**：5大趋势 + 下周关注

**技术规范：**
- 自包含（不依赖外部 CSS 框架，内联所有样式）
- 暗色主题（背景 `#0B0E14`，强调色 indigo/cyan/neon）
- 使用 Chart.js CDN：`https://cdn.jsdelivr.net/npm/chart.js`
- 支持滚动动画（IntersectionObserver）
- 响应式布局（移动端适配）

生成文件：`embodied_ai_weekly_report_<YEAR>_w<WEEK>.html`

### 3.4 推送到 GitHub Pages

**目标仓库结构：**
```
<github-repo>/
├── <YEAR>-W<WEEK>/
│   ├── index.html     ← 综合 HTML 报告
│   └── report.md      ← Markdown 全文
├── archive/
│   └── index.html     ← 归档索引（需更新）
└── latest/
    └── index.html     ← 最新周报入口（需更新为重定向）
```

**推送流程：**

```bash
# 1. 克隆仓库（优先 SSH，避免 HTTPS 网络问题）
git clone git@github.com:<USER>/<REPO>.git <LOCAL_PATH> --depth 1

# 2. 创建当周文件夹
mkdir <LOCAL_PATH>/<YEAR>-W<WEEK>

# 3. 复制文件
cp <REPORT>.html <LOCAL_PATH>/<YEAR>-W<WEEK>/index.html
cp <REPORT>.md   <LOCAL_PATH>/<YEAR>-W<WEEK>/report.md

# 4. 更新 latest/index.html（改为 meta refresh 重定向到新周）
# 5. 更新 archive/index.html（在列表顶部插入新周条目）

# 6. 提交推送
git add -A
git commit -m "feat: add W<WEEK> report (<DATE_START> ~ <DATE_END>)"
git push origin main
```

> ⚠️ HTTPS 推送若超时，改用 SSH (`git@github.com:...`)

**latest/index.html 模板（重定向）：**
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="0; url=./<YEAR>-W<WEEK>/index.html">
  <title>重定向...</title>
</head>
<body><p><a href="./<YEAR>-W<WEEK>/index.html">点击跳转</a></p></body>
</html>
```

**archive/index.html 新增条目模板：**
```html
<div class="archive-item">
  <span class="archive-date">📅 <YEAR>-W<WEEK> · <DATE_START> ~ <DATE_END></span>
  <a href="../<YEAR>-W<WEEK>/index.html" class="archive-link">查看详情 →</a>
</div>
```

---

## 输出文件清单

| 文件 | 内容 | 位置 |
|------|------|------|
| `images/` | 论文配图与项目截图目录 | 工作区根目录 |
| `embodied_ai_weekly_arxiv_<Y>_w<W>.md` | ArXiv 论文整理 | 工作区根目录 |
| `embodied_ai_weekly_arxiv_<Y>_w<W>.html` | ArXiv 报告网页版 | 工作区根目录 |
| `embodied_ai_weekly_github_<Y>_w<W>.md` | GitHub 项目整理 | 工作区根目录 |
| `embodied_ai_weekly_github_<Y>_w<W>.html` | GitHub 报告网页版 | 工作区根目录 |
| `embodied_ai_weekly_report_<Y>_w<W>.md` | 综合 Markdown 报告 | 工作区根目录 |
| `embodied_ai_weekly_report_<Y>_w<W>.html` | 综合可视化 HTML 报告 | 工作区根目录 |

---

## 用户配置信息

在开始前，需确认以下信息（若未提供则询问用户）：

| 参数 | 说明 | 示例 |
|------|------|------|
| 报告周期 | 起止日期 | 2026-03-26 ~ 2026-04-02 |
| 周编号 | ISO 周数 | W13 |
| GitHub 仓库 | 发布目标仓库 | `Jessy-Huang/embodied-ai-weekly` |
| 推送方式 | SSH 或 HTTPS | SSH（推荐） |
| 工作区路径 | 报告文件保存路径 | 当前 WorkBuddy 工作区 |
