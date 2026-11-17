---
name: drawio-skills
description: DrawIO图表技能。功能：(1)生成.drawio架构图、流程图、ER图、UML/时序图、网络拓扑、ML模型图等 (2)从已有.drawio文件确定性提取个人绘制风格生成style preset (3)按"linlan"个人风格（黑描边#000000+浅色填充+Tahoma+直角矩形）生成图表 (4)导出PNG/SVG/PDF。当用户需要画架构图、技术架构图、流程图、拓扑图、ER图时使用此技能。
---

# DrawIO 图表技能

> 技能版本：v1.0
> 训练日期：2026-08-26
> 依赖：Python 3.8+（脚本零第三方依赖）；导出图片可选 draw.io 桌面版 CLI
> 参考：https://github.com/Agents365-ai/drawio-skill（MIT License）

## 功能概述

本技能基于开源工程 [Agents365-ai/drawio-skill](https://github.com/Agents365-ai/drawio-skill) 微调，核心能力：

- **生成 .drawio 图表**：架构图、流程图、ER 图、UML/时序图、网络拓扑、ML/DL 模型图、思维导图等
- **个人风格预设**：从老板自己画过的 `.drawio` 源文件确定性提取配色/形状/字体/排版习惯，固化为 `styles/linlan.json`，生成时一键套用
- **风格学习**：`extract_style.py` 可对新源文件重新学习风格（含压缩格式解码）
- **导出**：`.drawio` 可经 draw.io 桌面版 CLI 导出 PNG/SVG/PDF/JPG

## 个人风格预设（linlan）

从 15 张老板源图（架构图 + 流程图两类）提取并人工复核的个人绘制风格：

### 风格速查表

| 维度 | 特征 |
|------|------|
| **描边** | 黑色 `#000000` 主导（全量 814 次，远超任何彩色描边） |
| **填充** | 留白/透明为主（903 次）；浅色填充 `#F5F5F5`、`#FFFAFA`、`#FFFFFF` |
| **分组描边色** | 红 `#EA6B66`、绿 `#00994D`、蓝 `#6666FF`、深红 `#660000`（用于架构图分组/分层） |
| **字体** | `Tahoma`（架构图，个人笔触）/ `Helvetica`（流程图，drawio 默认），约各半 |
| **字号** | `12` 为主，`10` 次之，`14` 用于标题 |
| **圆角** | 直角矩形为主（圆角仅约 9%） |
| **形状** | AWS 图标 + 自定义 stencil + 流程图标准件（start_2 / process / direct_data / multi-document） |
| **页面** | 1169×827（A4 横向），grid=1，gridSize=10 |
| **笔宽** | 默认 1（图标内部的 strokeWidth=2 是导入图标自带，非手绘） |

### 两类笔触

1. **架构图类**（互联网大厂/微服务/钓鱼防护/政务外网）：`Tahoma`、字号 10-12、黑描边 + 红绿蓝分组色、填充多留白、AWS 图标 + stencil
2. **流程图/技术架构类**（BERT/大模型训练/MCP/RAG/人才* 系列）：`Helvetica`、字号 14、流程图标准形状、浅色填充 + 彩色描边

### preset 文件

- `styles/linlan.json` — 个人风格预设（浅色语义填充 + 黑描边签名 + Tahoma + 直角 + 笔宽1）
- `styles/schema.json` — preset 结构定义（7 色槽 + 角色映射 + 形状词表 + 字体 + 边 + extras）

> **为什么 preset 用浅色填充而非留白**：preset schema 要求 `fillColor` 为 `#RRGGBB`（无法表达"透明"）。故将老板的"黑描边+留白"签名近似为"黑描边+浅色语义填充"，既保留黑描边辨识度，又保留语义颜色可读性。真正的"透明填充+分组彩描边"用法见下方「分组描边色」约定，需按需手写 XML。

### 分组描边色（架构图分层约定）

preset schema 无法表达"多组彩色描边"，这部分按需手写。老板架构图的分层习惯：

| 分组 | 描边色 | 填充 |
|------|--------|------|
| 默认/主体 | `#000000` | 无/白 |
| 红色分组 | `#EA6B66` | 无 |
| 绿色分组 | `#00994D` | 无 |
| 蓝色分组 | `#6666FF` | 无 |
| 深红/告警 | `#660000` | 无 |

## 核心脚本

### 1. extract_style.py — 风格提取（确定性）

```bash
# 从目录批量提取（生成 styles/linlan.json）
python scripts/extract_style.py <源文件目录> --name linlan

# 指定输出路径
python scripts/extract_style.py <目录或单文件> --name my-style --out styles/my-style.json
```

**算法**（参照参考工程 XML 提取路径，本地化微调）：
- 自动解码压缩格式 drawio（URL解码 → base64 → raw deflate → URL解码 → XML）
- 统计 `(fillColor, strokeColor)` 对 → 取 top 7 填 7 色槽
- 形状类判定：`cylinder3 > ellipse > rhombus > swimlane > rounded=1 > rounded=0`
- 角色推断：形状类优先，再 `dashed+灰底=external`，再标签词表（**已补中文词表**：队列/网关/认证/错误/数据库 等）
- 字体/字号取众数，加粗大字号子集识别为标题
- 边样式取众数（剥离坐标键），虚线标签 ≥2 共享词入 `dashedFor`

> **注意**：确定性算法对"每个角色固定 fill+stroke 对"的预设模型有效，但老板的"黑描边+留白"风格会令角色→色槽映射失真（如把 diff 图的 `#C925D1` 误判为数据库色）。故最终 preset 以人工复核为准，脚本用于快速得到数据底稿 + 后续新文件再学习。

### 2. analyze_style.py — 逐文件风格统计（复核用）

```bash
# 逐文件打印填充色/描边色/字体/字号/形状 TOP5 + 全局汇总，并落盘 style_report.json
python scripts/analyze_style.py <源文件目录>
```

## 风格 preset 机制

preset 是命名 JSON，`palette` 含 7 个语义色槽：

| 色槽 | 语义角色 | 老板配色（fill / stroke） |
|------|----------|--------------------------|
| primary | service 服务 | `#DAE8FC` / `#000000` |
| success | database 数据库 | `#D5E8D4` / `#000000` |
| warning | queue 队列 | `#FFF2CC` / `#000000` |
| accent | gateway 网关 | `#FFE6CC` / `#000000` |
| danger | error 错误 | `#F8CECC` / `#000000` |
| neutral | external 外部 | `#F5F5F5` / `#000000` |
| secondary | security 安全 | `#E1D5E7` / `#000000` |

生成时：角色 → `roles[role]` 得色槽 → `palette[slot]` 得 `(fillColor, strokeColor)`；形状用 `shapes[role]` 前缀；字体统一 `font.fontFamily` + `font.fontSize`；边用 `edges.style` + `edges.arrow`。

## 使用工作流（生成图表）

1. **确认需求**：图类型（架构/流程/ER/UML/拓扑）、输出格式、组件范围
2. **套用个人风格**：默认按 `styles/linlan.json`（黑描边 + 浅色填充 + Tahoma + 直角 + 笔宽1）
3. **生成 .drawio**：手写 XML（自定义样式/图标/泳道/精确几何）或 Mermaid 转 .drawio（标准无样式需求）
4. **自检**：结构 lint（悬空边/重复 id/重叠），视觉自检
5. **导出**：draw.io CLI 导出 PNG/SVG/PDF/JPG

## 参考图生成工作流（参考某张图 → 生成新图）

当用户说"参考 X.drawio 生成 Y 架构图"时，按此流程：

1. **分析参考图**：跑 `ref_analyze.py` 产出「参考报告」（风格 + 结构双模板）
   ```bash
   python scripts/ref_analyze.py <参考图.drawio> -o ref_report.md
   ```
   报告含：配色/字体/形状、页面尺寸、分组泳道层级、节点类型分布、边方向、布局模式（纵向分层/横向分层/网格）

2. **读报告**：理解参考图的风格 + 结构骨架（分层、节点类型、边组织方式）

3. **生成新图**：按新需求手写 XML，复用参考图的：配色/字体/形状（风格一致）、分组泳道骨架（层级命名按新需求替换）、布局模式（纵向/横向分层，节点数按需增减）、边样式（正交箭头，层间单向流）

4. **自检 + 导出**：结构 lint + 视觉自检，draw.io CLI 导出

> **风格默认套 linlan.json**：单图重提取 palette 会失真（"黑描边+留白"风格使角色→色槽映射不稳），故 `ref_analyze.py` 默认用人工复核的 `linlan.json` 作为风格；`--style <preset>` 指定其他预设，`--self` 才从参考图单图重提取。

## 目录结构

```
drawio-skills/
├── SKILL.md                  # 技能说明（本文件）
├── README.md                 # 用户文档
├── scripts/
│   ├── extract_style.py      # 风格提取（确定性，生成 preset）
│   ├── analyze_style.py      # 逐文件风格统计（复核）
│   └── ref_analyze.py        # 参考图分析（风格+结构，供 AI 参考生成新图）
├── styles/
│   ├── schema.json           # preset 结构定义
│   └── linlan.json           # 个人风格预设
└── style_report.json         # 风格分析报告（analyze_style.py 落盘）
```

## 参考来源

- 开源工程：<https://github.com/Agents365-ai/drawio-skill>（MIT，36 脚本/11 预设/万+形状/自检导出）
- 本技能做了四处微调：(1) 增补**中文角色词表**适配中文标签；(2) 增补**压缩格式解码**（老板源图为压缩 drawio）；(3) 将老板个人风格固化为 `linlan` preset，并文档化"黑描边+分组彩描边"签名；(4) 新增 `ref_analyze.py` 参考图结构分析（页面/分组泳道/节点类型/边方向/布局模式）

## 已知限制

| 问题 | 原因 | 状态 |
|------|------|------|
| 角色→色槽映射在"黑描边+留白"风格下失真 | 预设模型假设每角色固定 fill+stroke 对 | 人工复核为准 |
| "透明填充"无法进 preset | schema 要求 fillColor 为 #RRGGBB | 近似为浅色填充，真透明按需手写 XML |
| 自定义 stencil 形状无法保留 | 非标准 shape= 关键词 | 颜色/标签/边仍可捕获，图标丢失 |
| 布局分析对图标密集架构图有限 | 坐标聚类无法识别用图标背景表达的"层" | 节点类型/边/泳道仍可靠，布局作参考 |
| 导出需 draw.io 桌面版 CLI | 浏览器自动化不可靠 | 可选依赖，未装则只产出 .drawio |
