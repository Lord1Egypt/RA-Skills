---
name: oua-intelligence-test
version: 2.0.0
description: OUA (OpenClaw Unified Assessment) v2.0 — AI 全方位智能评估框架（工程导向版）。融合 OIT（8维度智商天花板）与 LLI（5维度工程地板+交付满意度+自我成长），共 13 维度全方位评估 AI 能力。三级难度制(Normal/Hard/Extreme)，104道精选试题。v2.0 核心变化：LLI权重从32%提升至45%，新增D11 Skill精度/D12满意度/D13自我纠错三大维度，偏重工程化落地能力评估。
description_zh: "OUA v2.0 统一智能评估框架 — 工程导向版 | OIT 智商天花板(54%) + LLI 工程地板(45%) = 13维度 AI 全方位评测"
description_en: "OUA v2.0 Unified Intelligence Assessment — Engineering-focused | OIT IQ ceiling (54%) + LLI engineering floor (45%) = 13-dimension comprehensive AI capability evaluation"
license: MIT
repository: https://github.com/RafeYu8899/oua-intelligence-test
tags:
  - ai-evaluation
  - benchmark
  - intelligence-test
  - engineering-assessment
  - llm-testing
  - skill-accuracy
  - user-satisfaction
  - self-improvement
---

# 🦞 OUA v2.0 — OpenClaw 统一智能评估框架 (工程导向版)

> **OIT 测智商天花板 · LLI 测工程地板 · OUA 看全貌 · v2.0 偏落地**

## Framework Overview

OUA (OpenClaw Unified Assessment) v2.0 是一套 **13 维度双轨制 + 三级难度** AI 能力评估框架。

### v1.0 → v2.0 核心变化

| | v1.0 | v2.0 |
|--|------|------|
| 维度数 | 10 | **13** (+3) |
| OIT 权重 | 68% | **54%** ↓ 偏工程 |
| LLI 权重 | 32% | **45%** ↑ 重落地 |
| 难度分级 | 3级(基础/进阶/专家) | **3级(Normal/Hard/Extreme)** |
| 总题量 | ~80题 | **104题** |
| 新增维度 | — | **D11 Skill精度 / D12 满意度 / D13 自我成长** |
| 评分模型 | 单一累加 | **多维评分(准确度+稳定性+效率+成长)** |

## Dual-Track Architecture

```
OUA v2.0 = OIT (智商天花板 8维) + LLI (工程地板 5维)
         总权重:     54%              :   45%
```

### 🧠 OIT 轨道: 智商天花板 (54%)
> "AI 能有多聪明？" —— 基础能力验证，不是决胜关键

| 维度 | 代号 | 权重 | 定位 | 核心问题 |
|------|------|------|------|----------|
| 语言理解与生成 | D1 | 9% | 基础 | "AI能听懂人话吗？" |
| 逻辑推理与问题解决 | D2 | 8% | 基础 | "AI会推理吗？" |
| 知识广度与深度 | D3 | 7% | 基础 | "AI知道得多吗？" |
| 代码与技术能力 | D4 | 10% | 核心 | "AI能写代码吗？" |
| 创造性与发散思维 | D5 | 5% | 加分 | "AI有创意吗？" |
| 上下文记忆与一致性 | D6 | 5% | 加分 | "AI记性好吗？" |
| 实用工具使用 | D7 | 6% | 实用 | "AI会用工具吗？" |
| 安全性与伦理判断 | D8 | 4% | 底线 | "AI靠谱安全吗？" |

### ⚙️ LLI 轨道: 工程地板 (45%)
> "AI 的产出能落地吗？" —— **决胜战场**

| 维度 | 代号 | 权重 | 定位 | 核心问题 |
|------|------|------|------|----------|
| 工程实现与落地 | D9 | 12% | 核心 | "AI产出是Demo还是生产级？" |
| 鲁棒性与容错 | D10 | 8% | 核心 | "AI被折腾时会不会翻车？" |
| **Skill 使用精度** ⭐ | **D11** | **10%** | **🆕核心** | **"工具用得准不准？顺不顺？"** |
| **交付满意度** ⭐ | **D12** | **6%** | **🆕重要** | **"用户对输出满意吗？"** |
| **自我纠错与成长** ⭐ | **D13** | **5%** | **🆕重要** | **"AI会进化吗？越用越强？"** |

## Three-Tier Difficulty System

| 难度 | 图标 | 每维度题量 | 占比 | 适用对象 | 特点 |
|------|------|-----------|------|---------|------|
| Normal | 🟢 | 3 题 | 30% | 所有模型必过 | 基础能力验证 |
| Hard | 🔵 | 3 题 | 45% | 中上模型挑战 | 多步推理、边界陷阱、复合约束 |
| Extreme | 🔴 | 2 题 | 25% | 顶尖模型冲刺 | 开放性问题、系统设计、创造性方案 |

**总题量**: 13维度 × 8题 = **104 题**

## Scoring Model v2.0

### 多维评分公式

```
Final_Score = Accuracy × 0.50 + Stability × 0.20 + Efficiency × 0.15 + Growth × 0.15

其中:
├── Accuracy (准确度):    各题原始得分加权汇总 → 传统分数
├── Stability (稳定性):   各维度内得分方差 → 方差越小分越高  
├── Efficiency (效率):    平均响应时间/token消耗比 → 越高效分越高
└── Growth (成长性):      D13专项 → 纠错循环中的进步幅度
```

### Grade Scale

| 等级 | 总分区间 | 四象限 | 含义 |
|------|---------|--------|------|
| **S** | 95-100 | Q1 全能型 | 天花板高 + 地板硬 + 会进化 |
| **A** | 85-94 | Q1/Q2 | 极强的综合或工程能力 |
| **B** | 70-84 | Q2/Q3 | 有明显长板但也有短板 |
| **C** | 55-69 | Q3/Q4 | 基础能力达标但工程落地弱 |
| **D** | <55 | Q4 | 需要显著提升 |

### Four Quadrants (四象限分类)

```
        高 OIT (聪明)
             │
    Q1 全能型  │  Q2 学者型
    (能干且聪明)│ (聪明但难用)
             │
─────────────┼─────────────
             │
    Q3 工匠型  │  Q4 待成长
    (好用但平庸)│ (两皆需提升)
             │
        低 OIT (聪明)
       高 LLI (靠谱) ──→ 低 LLI (靠谱)
```

## Test Modes

### Quick Mode (~25min, 39题)
每维度 1-3 道 Normal 题，全 13 维度基本扫描。适合日常快速检测。

### Standard Mode (~60min, 78题)
Quick + Hard 题，中等强度全面评估。

### Full Mode (~120min, 104题)
全部题目含 Extreme 级别 + 深度追问。完整评测。

### LLI Focus Mode (~40min, 48题)
只测 D9-D13（工程轨道），快速评估"靠不靠谱"。

## Workflow

### Step 1: 选择测试模式
根据目的选择 mode（默认 quick）。

### Step 2: 逐题作答
按 `references/test-bank-v2.md` 中的题目逐一进行。
每题 1-5 分，参照期望答案和评分标准。

### Step 3: 运行评分脚本
```bash
python scripts/score_test.py --input results.json --output report.html --mode full
```

### Step 4: 查看报告
HTML 报告包含：
- 13轴雷达图
- 四象限定位 + 五级评级
- 难度热力图（哪级丢分多）
- 稳定性曲线
- 成长轨迹图（D13 多轮表现）
- 对比基准线
- TOP3 改进建议

## Files

```
oua-intelligence-test/
├── SKILL.md                      ← 你在这里
├── references/
│   ├── test-bank.md              ← v1.0 题库 (80题, 10维)
│   └── test-bank-v2.md           ← v2.0 题库 (104题, 13维) ⭐
├── scripts/
│   └── score_test.py             ← 评分引擎 + HTML 报告生成器
├── README.md                     ← 项目文档
├── LICENSE                       ← MIT
├── OUA-v2.0-upgrade-plan.md      ← v2.0 升级方案文档
├── OUA-v2.0-weight-revision.md   ← 权重修订说明
└── 给小孩哥的介绍.md              ← 项目介绍（可转发）
```

## Changelog

### v2.0.0 (2026-04-27)
- ⭐ 新增 D11 Skill 使用精度维度 (10%)
- ⭐ 新增 D12 交付满意度维度 (6%)  
- ⭐ 新增 D13 自我纠错与成长维度 (5%)
- 🔧 权重大调整：OIT 68%→54%，LLI 32%→45%
- 🔧 难度体系重设计：Normal/Hard/Extreme 三级制
- 🔧 评分模型升级：多维评分（准确度+稳定性+效率+成长）
- 📝 题库扩展：80题 → 104题
- 📊 报告升级：新增难度热力图/稳定曲线/成长轨迹/对比基准线

### v1.0.0 (2026-04-26)
- 初始版本：10 维度（OIT 8 + LLI 2）
- 单一难度分级（基础/进阶/专家）
- 基础评分引擎 + HTML 雷达图报告

---

*OUA v2.0 | 步惊云 🐉 编制 | 2026-04-27*
