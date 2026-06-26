---
name: academic-paper-refinement
description: 综合多评审系统的学术论文精修技能。适用于学术论文从初稿到终稿的全流程修订，包括多轮评审、意见整合、结构优化和语言润色。
version: 7.5.0
author: Clark_St.
license: MIT
tags: [Academic Writing, Peer Review, Paper Revision, Multi-Reviewer Integration, LaTeX, PDF Generation, Humanizer, AI Detection]
dependencies:
  - pandoc
  - wkhtmltopdf
  - EvoScientist (/usr/local/bin/EvoScientist)
  - researchclaw (/usr/local/bin/researchclaw)
  - AI-Research-SKILLs (skills/AI-Research-SKILLs/)
  - peer-reviewer (skills/peer-reviewer/)
ccf_reference: https://www.ccf.org.cn/Academic_Evaluation/By_category/
---

# Academic Paper Refinement - 学术论文精修技能 v7.5.0

## 📋 技能概述

本技能提供学术论文从初稿到终稿的全流程精修能力，核心特点：
- **四工具评审**：EvoScientist → AutoResearchClaw → AI-Research-SKILLs → peer-reviewer
- **双工具修订**：EvoScientist（主）+ AutoResearchClaw（辅）
- **多轮迭代**：评审 → 修订 → 再评审，直至收敛
- **完整清理**：参考文献、格式、命名最终统一

---

## 🔧 可用工具一览

### 论文评审工具（4种，按顺序执行）

| 顺序 | 工具 | 位置 | 状态 | 调用命令 |
|:----:|------|------|:----:|----------|
| 1 | **EvoScientist** | `/usr/local/bin/EvoScientist` | ✅ | `EvoScientist --prompt "..." --mode run --auto-approve` |
| 2 | **AutoResearchClaw** | `/usr/local/bin/researchclaw` | ✅ | `researchclaw run --stage 18` |
| 3 | **AI-Research-SKILLs** | `skills/AI-Research-SKILLs/` | ✅ | 加载 SKILL.md 执行 |
| 4 | **peer-reviewer** | `skills/peer-reviewer/` | ✅ | `node dist/index.js` |

### 论文修订工具（2种，按优先级执行）

| 优先级 | 工具 | 角色 | 状态 | 调用命令 |
|:------:|------|:----:|:----:|----------|
| 1 | **EvoScientist** | 主要 | ✅ | `EvoScientist --prompt "Revise..." --mode run --auto-approve` |
| 2 | **AutoResearchClaw** | 辅助 | ✅ | `researchclaw run --stage 19` |

---

## ⚠️ 强制执行要求

### 必须完整执行全部12步骤

**严格执行原则**：
1. **禁止跳过步骤**：所有12个步骤必须按顺序执行，不得跳过任何步骤
2. **禁止提前终止**：即使Step 7收敛判断显示"已收敛"，也必须继续执行Step 8-12
3. **禁止省略输出**：每个步骤必须生成对应的输出文件和报告

### 步骤执行规则

| 步骤类型 | 规则 | 说明 |
|---------|------|------|
| **Step 1-2** | 强制执行 | 格式分析和数据核查是基础 |
| **Step 3-6** | 强制执行两轮迭代 | 即使Round 1评分较高，也必须执行Round 2评审 |
| **Step 7** | 强制执行 | 收敛判断仅作为参考，不作为终止条件 |
| **Step 8** | 强制执行 | 最终优化必须执行 |
| **Step 9** | 条件执行 | 仅当页数超过目标时执行 |
| **Step 10** | 强制执行 | Humanizer改写必须执行 |
| **Step 11** | 强制执行 | 最终清理必须执行 |
| **Step 12** | 强制执行 | 批判性终审必须执行 |

### 违规行为

以下行为被视为违规：
- ❌ 在Step 7收敛判断后跳过Step 8-12
- ❌ 跳过Step 5-6（Round 2评审和修订）
- ❌ 跳过Step 10（Humanizer改写）
- ❌ 未生成完整的目录结构（v0, v1, v2, v3, v4, v5, v_final, humanlike, reviews）
- ❌ 未生成所有评审报告

### 完整输出要求

每个精修任务必须生成以下完整目录结构：
```
输出目录/
├── v0/              ← Step 1-2 输出
├── v1/              ← Step 2 输出
├── v2/              ← Step 4 Round 1修订
├── v3/              ← Step 6 Round 2修订
├── v4/              ← Step 8 最终优化
├── v5/              ← Step 9 内容压缩（如执行）
├── v_final/         ← Step 11 最终版本
├── humanlike/       ← Step 10 Humanizer改写
└── reviews/         ← 所有评审报告
    ├── Step1_Format_Analysis.md
    ├── Step2_Data_Verification.md
    ├── Round1_Critical_Review.md
    ├── Round2_Critical_Review.md
    ├── Step7_Convergence_Check.md
    ├── Step8_Final_Optimization.md
    ├── Step9_Content_Compression.md（如执行）
    ├── Step10_Humanizer.md
    ├── Step11_Final_Cleanup.md
    └── Step12_Final_Critical_Review.md
```

---

## 📐 完整工作流程（12步骤）

```
┌─────────────────────────────────────────────────────────────────────┐
│                    学术论文精修完整流程（12步骤）                     │
├─────────────────────────────────────────────────────────────────────┤
│  Step 1:   期刊格式分析          → v0/        [结构整理]            │
│  Step 2:   数据核查与实验完善    → v1/        [数据验证]            │
│  Step 3:   第一轮评审 (Round 1)  → reviews/   [四工具评审]          │
│  Step 4:   第一次修订            → v2/        [双工具修订+合并]      │
│  Step 5:   第二轮评审 (Round 2)  → reviews/   [四工具评审]          │
│  Step 6:   第二次修订            → v3/        [双工具修订+合并]      │
│  Step 7:   第三轮评审+收敛判断   → reviews/   [四工具评审+多维判断]  │
│  Step 8:   最终优化              → v4+/       [图表/引用/格式]       │
│  Step 9:   内容压缩与篇幅优化    → v5+/       [条件执行]             │
│  Step 10:  Humanizer语言改写     → humanlike/ [降低AI痕迹]          │
│  Step 11:  最终清理与格式统一    → v_final/   [投稿前必执行]         │
│  Step 12:  批判性终审与修改建议  → final/     [拒稿视角评审]         │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Step 1: 期刊格式分析与结构整理

### 操作内容
1. 搜索目标期刊最新5篇论文
2. 分析维度：章节结构、行文方式、格式规范、内容分配
3. 重构论文结构，避免编号项
4. 生成 v0 版本

### 输出
```
v0/
├── paper.tex
└── paper.pdf
```

---

## Step 2: 数据核查与实验完善

### A. 数值一致性核查

#### 核查维度
| 维度 | 检查方法 | 容错范围 |
|------|----------|----------|
| **正文-表格对照** | 逐一核对数值 | 0误差 |
| **正文-图表对照** | 数值+趋势核对 | 0误差 |
| **摘要-正文对照** | 关键数据核对 | 0误差 |
| **结论-正文对照** | 关键数据核对 | 0误差 |
| **引用数据-原文对照** | 抽查关键引用 | 0误差 |

#### 常见数据问题
| 问题类型 | 示例 | 检查方法 |
|----------|------|----------|
| 计算错误 | 增长率计算口径不一致 | 统一计算公式 |
| 精度不一致 | 同一数据在不同位置精度不同 | 统一数据来源 |
| 单位错误 | 单位换算错误或标注缺失 | 逐一检查 |
| 百分比错误 | 占比计算基数错误 | 验证分母 |

---

### B. 统计报告完整性

#### 必须报告项
| 统计量 | 报告格式 | 示例 |
|--------|----------|------|
| **效应量** | Cohen's d = X [95% CI] | d = 0.85 [0.78, 0.92] |
| **置信区间** | 均值 ± CI | 95% CI: [X, Y] |
| **样本量** | n = X | n = 10,000 |
| **p值** | p < 0.001 或 p = X | p < 0.001 |
| **统计量** | χ² = X, U = Y | χ² = 15.32 |

#### 大样本注意事项
```
⚠️ 大样本陷阱（n > 10000）:
├── p值几乎必然 < 0.05
├── 应强调效应量而非p值
├── 报告效应量置信区间
└── 解释实际意义而非统计显著性
```

---

### C. 数据术语定义

#### 定义位置
- **必须在Methods章节**明确定义
- 后续章节使用统一定义

#### 定义模板
```latex
\textbf{数据术语定义。} 为确保清晰性和一致性，本文定义如下术语：

\begin{itemize}
\item \textbf{术语A}: 定义内容。总计: X条记录。
\item \textbf{术语B}: 定义内容。总计: Y条记录。
\end{itemize}
```

---

### D. 数据来源追溯

#### 数据来源表
| 数据项 | 来源 | 时间范围 | 精度 |
|--------|------|----------|------|
| 核心指标A | 系统日志记录 | 研究周期内 | 精确 |
| 核心指标B | 设备清单审计 | 研究周期内 | 精确 |
| 实验数据 | 数据库记录 | 研究周期内 | 精确 |

---

### E. 数值精度统一

| 场景 | 精度要求 | 示例 |
|------|----------|------|
| 计数 | 精确值 | 12,345 |
| 百分比 | 1位小数 | 40.2% |
| 效应量 | 2位小数 | d = 0.85 |
| 增长倍数 | 1位小数 | 3.5-fold |
| 时间 | 适当精度 | 8.5 hours |

---

### 输出
```
v1/
├── paper.tex
├── paper.pdf
├── references.bib
└── data_verification_report.md
```

---

## Step 3/5/7: 论文评审（三轮相同流程）

### ⚠️ 核心要求

**【重要】批判性评审原则：**

**评审视角**：假设你是审稿人，正在寻找拒稿理由。以最严苛的标准发现潜在问题，确保论文在投稿前达到最高质量。

```
┌─────────────────────────────────────────────────────────────────────┐
│                    批判性评审核心原则                                 │
├─────────────────────────────────────────────────────────────────────┤
│  🎯 评审视角：假设你是审稿人，正在寻找拒稿理由                       │
│                                                                      │
│  ❌ 不要：                                                           │
│     ├── 客套话、表扬性评价                                           │
│     ├── 泛泛而谈的修改建议                                           │
│     ├── 忽略细节问题                                                 │
│     └── 过度宽容                                                     │
│                                                                      │
│  ✅ 要：                                                             │
│     ├── 直击要害，指出致命问题                                       │
│     ├── 与现有SOTA方法逐一对比                                       │
│     ├── 质疑每一个创新点                                             │
│     ├── 挑战实验设计的合理性                                         │
│     └── 深挖数据支撑的不足                                           │
└─────────────────────────────────────────────────────────────────────┘
```

**【重要】评审执行流程：**

1. **按顺序执行四种工具进行评审**
2. **第1个工具完成后，不要立即进行下一个工具**
3. **等待该工具评审完成，保存评审报告**
4. **再执行下一个工具的评审**
5. **所有4个工具的评审报告都生成后，综合判断，再进行论文修订**

### 批判性评审执行流程

```
批判性论文评审执行流程:
│
├── [1] EvoScientist 批判性评审
│   ├── 命令: EvoScientist --prompt "Critical review from rejection perspective..." --mode run --auto-approve
│   ├── 重点: 创新性质疑、方法学缺陷、数据支撑不足
│   ├── ⏳ 等待: 评审完成
│   └── ✅ 输出: reviews/EvoScientist_round[N]_critical_review.md
│
├── [2] AutoResearchClaw 批判性评审
│   ├── 命令: researchclaw run --config config.arc.yaml --stage 18 --mode critical
│   ├── 重点: 创新性质疑、Evidence不足、Methodology-Evidence不一致
│   ├── ⏳ 等待: 评审完成
│   └── ✅ 输出: reviews/AutoResearchClaw_round[N]_critical_review.md
│
├── [3] AI-Research-SKILLs 批判性评审
│   ├── 操作: 加载 SKILL.md 执行批判性评审
│   ├── 重点: 方法学缺陷、实验设计缺陷、对比分析不足
│   ├── ⏳ 等待: 评审完成
│   └── ✅ 输出: reviews/AI-Research-SKILLs_round[N]_critical_review.md
│
└── [4] peer-reviewer 批判性评审
    ├── 命令: node dist/index.js [paper_path] --mode reject
    ├── 重点: 逻辑漏洞、过度声称、创新性不足、实验分析不足
    ├── ⏳ 等待: 评审完成
    └── ✅ 输出: reviews/peer-reviewer_round[N]_critical_review.md
```

### 批判性评审维度与要点

#### A. 创新性质疑

| 质疑点 | 检查方法 | 潜在问题 |
|--------|----------|----------|
| **创新是否真实？** | 对比近3年SOTA论文 | 声称的创新可能已被他人解决 |
| **创新是否重要？** | 评估问题影响力 | 解决的问题可能不重要 |
| **创新是否显著？** | 量化改进幅度 | 改进幅度可能不足以支撑论文 |
| **创新是否通用？** | 测试场景覆盖 | 可能只在特定场景有效 |

#### B. 方法论批判

| 批判点 | 检查方法 | 潜在问题 |
|--------|----------|----------|
| **实验设计是否合理？** | 对照组设置、变量控制 | 可能存在混淆变量 |
| **数据集是否充分？** | 数据量、多样性、代表性 | 可能存在数据偏差 |
| **评估指标是否恰当？** | 指标选择、统计方法 | 可能存在指标选择偏差 |
| **对比是否公平？** | 对比方法版本、参数设置 | 可能存在不公平对比 |

#### C. 技术细节深挖

| 深挖点 | 检查方法 | 潜在问题 |
|--------|----------|----------|
| **超参数敏感性？** | 参数敏感性分析 | 方法可能对超参数过度敏感 |
| **计算复杂度？** | 时间/空间复杂度分析 | 实际可用性可能受限 |
| **可复现性？** | 代码、数据、环境说明 | 他人可能无法复现结果 |
| **失败案例？** | 错误案例分析 | 可能隐藏大量失败案例 |

#### D. 与SOTA对比不足

| 对比维度 | 检查方法 | 潜在问题 |
|----------|----------|----------|
| **覆盖广度** | 是否覆盖主流SOTA方法 | 可能遗漏重要对比方法 |
| **对比深度** | 是否深入分析差异 | 可能流于表面的数值对比 |
| **失败承认** | 是否承认方法不足 | 可能隐瞒方法劣势场景 |
| **公平性** | 是否使用相同条件 | 可能存在不公平对比 |

#### E. 写作与表达问题

| 问题类型 | 检查方法 | 潜在问题 |
|----------|----------|----------|
| **逻辑漏洞** | 逐段逻辑检查 | 推理可能存在跳跃 |
| **术语混乱** | 术语一致性检查 | 可能存在定义不清 |
| **过度声称** | 声称与证据对照 | 声称可能超出证据支撑 |
| **引用问题** | 引用完整性检查 | 可能存在选择性引用 |

### 工具调用详解

#### 1. EvoScientist 批判性调用

```bash
# 批判性论文评审
EvoScientist --prompt "Review the paper at [paper_path] from a rejection perspective. Act as a critical reviewer seeking reasons to reject. Challenge every claim, question every innovation point, identify methodological flaws, and demand stronger evidence. Evaluate: (1) Is the claimed novelty truly novel? (2) Are the experiments fairly designed? (3) Is the comparison with SOTA comprehensive? (4) Are the conclusions supported by evidence? Generate detailed critical review with rejection risk assessment." --mode run --auto-approve
```

**批判性评审维度**：
- 创新真实性（与SOTA对比）
- 方法学严谨性（实验设计缺陷）
- 数据充分性（样本量、偏差）
- 结论可靠性（过度声称检测）

---

#### 2. AutoResearchClaw 批判性调用

```bash
# 设置环境变量
export TENCENT_CODING_API_KEY="your-api-key"

# 运行批判性论文评审（Stage 18: CRITICAL_PEER_REVIEW）
cd ~/.openclaw/workspace/skills/AutoResearchClaw/
researchclaw run --config config.arc.yaml --stage 18 --paper-path [paper_path] --mode critical
```

**批判性评审特点**：
- Evidence Gap分析（证据缺口）
- Methodology-Evidence Inconsistency（方法与证据不一致）
- Comparison Insufficiency（对比不充分）
- Claim-Evidence Mismatch（声称与证据不匹配）

---

#### 3. AI-Research-SKILLs 批判性调用

```bash
# 使用 autoresearch 技能进行批判性评审
# 读取 SKILL.md 获取详细调用方式
cat ~/.openclaw/workspace/skills/AI-Research-SKILLs/0-autoresearch-skill/SKILL.md
```

**批判性评审特点**：
- 实验设计漏洞检测
- 基线方法覆盖不足分析
- 消融实验缺失检查
- 负面结果隐瞒识别

---

#### 4. peer-reviewer 批判性调用

```bash
# 进入技能目录
cd ~/.openclaw/workspace/skills/peer-reviewer/

# 批判性评审论文文件
node dist/index.js "/path/to/paper.tex" --mode reject
```

**批判性评审系统**：
- **Deconstructor（解构）**：拆解论文论证结构，识别逻辑断层
- **Devil's Advocate（攻击）**：主动寻找拒稿理由，挑战每个声称
- **Judge（评判）**：综合评估，给出录用/拒稿建议及拒稿风险等级

---

### 输出文件（每轮）

```
reviews/
├── EvoScientist_round[N]_critical_review.md       # 必需
├── AutoResearchClaw_round[N]_critical_review.md   # 必需
├── AI-Research-SKILLs_round[N]_critical_review.md # 必需
└── peer-reviewer_round[N]_critical_review.md      # 必需
```

---

### 批判性评审报告模板

```markdown
# 批判性评审报告 - Round [N]

## 基本信息
- 论文标题: [标题]
- 评审日期: YYYY-MM-DD
- 目标期刊: [期刊名]

---

## 一、拒稿风险评估

### 🔴 高风险拒稿理由（必须修改）

| 序号 | 问题 | 严重程度 | 页码/位置 | 修改建议 |
|:----:|------|:--------:|:---------:|----------|
| 1 | [具体问题描述] | 致命 | X页Y行 | [具体修改方案] |

### 🟡 中等风险问题（强烈建议修改）

| 序号 | 问题 | 严重程度 | 页码/位置 | 修改建议 |
|:----:|------|:--------:|:---------:|----------|
| 1 | [具体问题描述] | 重要 | X页Y行 | [具体修改方案] |

### 🟢 低风险问题（建议完善）

| 序号 | 问题 | 严重程度 | 页码/位置 | 修改建议 |
|:----:|------|:--------:|:---------:|----------|
| 1 | [具体问题描述] | 次要 | X页Y行 | [具体修改方案] |

---

## 二、与现有技术方法对比不足之处

### 2.1 遗漏的重要对比方法

| 方法名 | 发表信息 | 为何重要 | 未对比的影响 |

### 2.2 对比不充分的方法

| 对比方法 | 不足之处 | 建议补充 |

### 2.3 方法劣势场景未充分展示

| 场景 | 本方法表现 | SOTA表现 | 是否已展示 |

---

## 三、核心创新点质疑

### 创新点1: [创新点名称]

**论文声称**: [论文中的声称]

**质疑理由**:
- [质疑1]
- [质疑2]

**证据支撑不足之处**:
- [不足1]
- [不足2]

**修改建议**: [具体建议]

---

## 四、实验设计问题深挖

### 4.1 数据集问题
### 4.2 评估指标问题
### 4.3 对比实验问题

---

## 五、写作问题清单

### 5.1 逻辑漏洞
### 5.2 过度声称
### 5.3 表达问题

---

## 六、综合评估与建议

### 录用概率评估

| 评审工具 | 评分 | 录用概率预估 |
|----------|:----:|:------------:|
| EvoScientist | X/10 | X% |
| AutoResearchClaw | X/10 | X% |
| AI-Research-SKILLs | X/10 | X% |
| peer-reviewer | X/10 | X% |
| **综合评估** | **X/10** | **X%** |

### 必须修改项（P0）
### 强烈建议修改项（P1）
### 建议完善项（P2）

---

## 七、结论

**总体评价**: [简要总结论文质量]

**主要风险**: [列出最大的拒稿风险]

**核心建议**: [列出最重要的修改建议]

**是否建议投稿**: ✅ 建议投稿 / ⚠️ 修改后投稿 / ❌ 不建议投稿
```

---

### 评审维度对照表

| 维度 | EvoScientist | AutoResearchClaw | AI-Research-SKILLs | peer-reviewer |
|------|:------------:|:----------------:|:------------------:|:-------------:|
| 创新/严谨性 | Quality | ✅ | ✅ | Merit Score |
| 清晰度 | Clarity | ✅ | ✅ | Logic Score |
| 重要性 | Significance | ✅ | ✅ | Novelty Score |
| 原创性 | Originality | ✅ | ✅ | Novelty Score |
| 可复现性 | Reproducibility | ✅ | ✅ | - |
| 方法学一致性 | - | Evidence Check | ✅ | Logic Check |
| **拒稿风险** | **✅** | **✅** | **✅** | **✅** |

---

## Step 4/6: 论文修订（两轮相同流程）

### ⚠️ 核心要求

**【重要】修订执行流程：**

1. **读取批判性评审报告**，提取所有P0/P1/P2问题
2. **先执行 EvoScientist 修订**，等待完成
3. **再执行 AutoResearchClaw 修订**，等待完成
4. **综合合并两版本修改意见**
5. **以 EvoScientist 版本为基准**

### 基于批判性评审的修订流程

```
论文修订执行流程:
│
├── [Phase 0] 问题提取与优先级排序
│   ├── 读取四工具批判性评审报告
│   ├── 提取所有P0问题（必须修改）
│   ├── 提取所有P1问题（强烈建议修改）
│   ├── 整理P2问题（建议完善）
│   └── ✅ 输出: reviews/round[N]_consolidated_issues.md
│
├── [Phase 1] EvoScientist 修订（主要）
│   ├── 命令: EvoScientist --prompt "Revise paper based on critical review..." --mode run --auto-approve
│   ├── 输入: 论文 + consolidated_issues.md
│   ├── 重点: P0问题修复、创新点加强、对比实验补充
│   ├── ⏳ 等待: 修订完成
│   └── ✅ 输出: v[EvoSci]/ + EVO_REVISION_LOG.md
│
├── [Phase 2] AutoResearchClaw 修订（辅助）
│   ├── 命令: researchclaw run --config config.arc.yaml --stage 19
│   ├── 输入: 论文 + consolidated_issues.md
│   ├── 重点: 数据补充、方法学完善、证据加强
│   ├── ⏳ 等待: 修订完成
│   └── ✅ 输出: v[ARC]/ + ARC_REVISION_LOG.md
│
└── [Phase 3] 综合合并（以EvoScientist为主）
    ├── 对比两版本修改差异
    ├── 以EvoScientist版本为基准
    ├── 整合AutoResearchClaw独特改进
    ├── 验证所有P0问题已修复
    └── ✅ 输出: v[merged]/ + MERGED_REVISION_NOTES.md
```

### 问题提取与优先级排序模板

```markdown
# Round [N] 综合问题清单

## 一、P0问题（必须修改，影响录用决策）

| 序号 | 问题来源 | 问题描述 | 页码/位置 | 修改方案 | 状态 |
|:----:|:--------:|----------|:---------:|----------|:----:|
| 1 | EvoSci | [问题] | X页Y行 | [方案] | ⬜ |
| 2 | ARC | [问题] | X页Y行 | [方案] | ⬜ |
...

## 二、P1问题（强烈建议修改，严重影响质量）

| 序号 | 问题来源 | 问题描述 | 页码/位置 | 修改方案 | 状态 |
|:----:|:--------:|----------|:---------:|----------|:----:|
| 1 | AI-SKILLs | [问题] | X页Y行 | [方案] | ⬜ |
...

## 三、P2问题（建议修改，提升论文质量）

| 序号 | 问题来源 | 问题描述 | 页码/位置 | 修改方案 | 状态 |
|:----:|:--------:|----------|:---------:|----------|:----:|
| 1 | peer-reviewer | [问题] | X页Y行 | [方案] | ⬜ |
...

## 四、问题分布统计

| 问题类型 | P0 | P1 | P2 | 合计 |
|----------|:--:|:--:|:--:|:----:|
| 创新性质疑 | X | X | X | X |
| 方法论问题 | X | X | X | X |
| 对比不足 | X | X | X | X |
| 写作问题 | X | X | X | X |
| **合计** | **X** | **X** | **X** | **X** |
```

### 综合合并原则

| 合并场景 | 处理方式 |
|---------|---------|
| 两工具修改一致 | ✅ 直接采用 |
| EvoScientist独有修改 | ✅ **优先采用** |
| AutoResearchClaw独有修改 | ⚠️ 评估后决定 |
| 两工具修改冲突 | ✅ **以EvoScientist为准** |

### 修订后验证清单

```
修订后验证清单:
│
├── [ ] P0问题修复验证
│   ├── [ ] 所有问题已定位修改位置
│   ├── [ ] 修改内容符合评审建议
│   └── [ ] 修改未引入新问题
│
├── [ ] P1问题修复验证
│   ├── [ ] 主要P1问题已修复
│   └── [ ] 剩余P1问题有合理解释
│
├── [ ] 内容一致性检查
│   ├── [ ] 摘要与正文一致
│   ├── [ ] 数据前后一致
│   └── [ ] 引用完整正确
│
└── [ ] 格式规范性检查
    ├── [ ] 符合期刊格式
    ├── [ ] 图表引用正确
    └── [ ] 参考文献格式正确
```

---

### 修订优先级

| 优先级 | 定义 | 示例 | 处理要求 |
|:------:|------|------|----------|
| **P0** | 必须修改，影响录用决策 | 创新性质疑、缺乏对比实验、因果推断过度 | **本轮必须修复** |
| **P1** | 强烈建议修改，严重影响质量 | 数据不一致、引用错误、方法学缺陷 | **本轮尽量修复** |
| **P2** | 建议修改，提升论文质量 | 对比分析不足、图表优化 | 视时间修复 |
| **P3** | 可选修改，完善细节 | 格式统一、拼写检查 | 后续修复 |

---

## Step 7: 打分对比与收敛判断

### 多维度收敛标准

| 维度 | 收敛标准 | 权重 |
|------|----------|:----:|
| **评分差异** | 平均差异 ≤ 1.0分 | 40% |
| **P0问题数** | P0问题 = 0 | 30% |
| **四工具共识** | 3/4工具同意录用 | 20% |
| **格式合规** | 期刊要求100%满足 | 10% |

### 收敛判断流程

```
判断流程:
│
├── [1] 计算评分差异
│   └── 平均差异 ≤ 1.0? → 通过 → 继续下一步
│                    → 未通过 → 返回Step 6
│
├── [2] 检查P0问题
│   └── P0问题 = 0? → 通过 → 继续下一步
│                   → 未通过 → 返回Step 6
│
├── [3] 检查四工具共识
│   └── ≥3工具同意? → 通过 → 继续下一步
│                   → 未通过 → 返回Step 6
│
├── [4] 检查格式合规
│   └── 100%满足? → 通过 → 进入Step 8
│                  → 未通过 → 修复后进入Step 8
│
└── ✅ 收敛完成
```

### 打分对比模板

```markdown
## 四工具三轮评分对比

| 评审工具 | Round 1 | Round 2 | Round 3 | R2→R3变化 | 收敛 |
|---------|:-------:|:-------:|:-------:|:---------:|:----:|
| EvoScientist | /10 | /10 | /10 | ± | ✅/❌ |
| AutoResearchClaw | /10 | /10 | /10 | ± | ✅/❌ |
| AI-Research-SKILLs | /10 | /10 | /10 | ± | ✅/❌ |
| peer-reviewer | /10 | /10 | /10 | ± | ✅/❌ |

**综合收敛判断：**
- 平均差异: 分
- P0问题数: 个
- 收敛工具数: /4
- 格式合规: %
- **后续操作**: [进入Step 8 / 返回Step 6]
```

### 终止条件

| 条件 | 说明 |
|------|------|
| **正常终止** | 4个维度全部通过 |
| **强制终止** | 迭代 ≥ 5轮，评分不再提升 |
| **人工干预** | 评审意见存在根本性分歧 |

---

## Step 8: 最终优化

### 优化方向

| 优化项 | 具体内容 | 版本 |
|--------|---------|:----:|
| 图表整合 | 添加实验图表、优化可视化 | v4 |
| 引用密度 | 增加引用次数、优化引用分布 | v5 |
| 参考文献质量 | CCF分级、替换预印本、补充DOI | v6 |

### 输出
```
v4/ v5/ v6/
├── paper.tex
├── paper.pdf
├── references.bib
├── REVISION_LOG.md
└── figures/
```

---

## Step 9: 内容压缩与篇幅优化（条件执行）

### 触发条件

| 条件 | 判断标准 | 执行压缩 |
|------|----------|----------|
| 总页数超标 | Preprint > 40页 / 双栏 > 20页 | ✅ 执行 |
| 某章节过长 | 单章节 > 总篇幅30% | ✅ 执行 |
| 评审建议压缩 | 评审工具建议"长度问题" | ✅ 执行 |

---

## Step 10: Humanizer语言改写（降低AI生成痕迹）

### 目的

在保持论文内容、数据、引用不变的前提下，通过语言改写降低AI生成检测概率，使论文表达更接近人类自然写作风格。

### 触发条件

| 条件 | 建议 |
|------|:----:|
| AI生成检测概率 > 70% | ✅ 强烈建议执行 |
| AI生成检测概率 50-70% | ⚠️ 建议执行 |
| 语言风格评审建议 | ✅ 根据评审意见执行 |
| 用户明确要求 | ✅ 执行 |

### 核心原则

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Humanizer改写核心原则                             │
├─────────────────────────────────────────────────────────────────────┤
│  ✅ 必须保持不变：                                                    │
│     ├── 所有数据、统计数字、百分比                                    │
│     ├── 所有参考文献引用 (\cite{})                                    │
│     ├── 所有图表引用 (Figure~\ref{}, Table~\ref{})                    │
│     ├── 因果语言控制（如已使用"associated with"等）                   │
│     └── 学术格式（Highlights, Keywords, Abstract结构）               │
│                                                                      │
│  🔧 改写重点：                                                        │
│     ├── 过渡词替换（模式化→自然化）                                   │
│     ├── 句式变换（打破重复结构）                                      │
│     ├── 结构调整（减少过度对称）                                      │
│     └── 语言自然化（更接近人类风格）                                  │
└─────────────────────────────────────────────────────────────────────┘
```

### 改写方法

#### A. 过渡词替换表

| AI模式化过渡词 | 自然化替代 | 示例 |
|---------------|-----------|------|
| Notably, | Worth noting / Importantly | Notably, we found → We found |
| Significantly, | Importantly / Of note | Significantly, the change → The change |
| In conclusion, | To summarize / Overall | In conclusion, this study → Overall, this study |
| In summary, | Briefly / To recap | In summary, we present → We present |

#### B. 句式变换策略

**1. 长句拆分**

```
原版（AI痕迹）:
This study documents the transformation from separately operated 
supercomputing centers and AI computing facilities toward integrated 
HPC-AI converged computing centers at a major Chinese research university 
using longitudinal case study methodology.

改写版（自然表达）:
This paper tracks how a major Chinese research university moved from 
operating separate supercomputing and AI facilities to building integrated 
HPC-AI converged infrastructure. Drawing on longitudinal case study 
methodology, we analyze...
```

**2. 被动转主动**

```
原版: This transformation was driven by...
改写: This shift came about through...
```

**3. 名词化转动词化**

```
原版: The emergence of AI for Science as a dominant research paradigm 
has fundamentally altered the landscape of scientific computing.

改写: AI for Science has emerged as a leading research paradigm, 
reshaping how we think about scientific computing.
```

**4. 打破列举式结构**

```
原版（AI痕迹）:
This study makes three primary contributions: From an empirical 
perspective... From a conceptual perspective... From a practical 
perspective...

改写版（自然表达）:
We contribute in three ways. Empirically, we provide... Conceptually, 
we propose... Practically, we derive...
```

#### C. 结构调整策略

**1. 段落开头多样化**

| AI模式化开头 | 自然化替代 |
|-------------|-----------|
| This study... | We / Our analysis / The data |
| It is worth noting that... | Worth noting: / One thing stands out: |
| It should be emphasized that... | Key point: / The main thing is |
| There are several factors... | Several factors come into play |

**2. 段落长度变化**

```
AI模式化：段落长度均匀，结构对称
人类风格：段落长短交替，结构灵活
```

**3. 段落内部结构**

```
AI模式化：
├── 主题句
├── 支持句1（举例）
├── 支持句2（数据）
└── 总结句

人类风格：
├── 主题句（可能省略）
├── 支持内容（灵活组合）
└── 过渡到下一段（可选）
```

### 执行流程

```
Humanizer改写执行流程:
│
├── [1] AI生成检测
│   ├── 使用检测工具评估原版AI生成概率
│   ├── 生成检测报告
│   └── 记录主要AI痕迹特征
│
├── [2] 段落级改写
│   ├── 按段落逐一改写
│   ├── 保持数据、引用不变
│   ├── 应用过渡词替换表
│   └── 应用句式变换策略
│
├── [3] 整体一致性检查
│   ├── 检查数据完整性
│   ├── 检查引用完整性
│   ├── 检查因果语言保持
│   └── 检查学术格式保持
│
├── [4] 编译验证
│   ├── LaTeX编译
│   ├── 检查编译错误
│   └── 生成改写版PDF
│
├── [5] 改写后检测
│   ├── 再次评估AI生成概率
│   ├── 对比改写前后概率
│   └── 生成改写报告
│
└── [6] 评审验证（可选）
    ├── 使用四工具评审改写版
    ├── 确认学术质量未降低
    └── 确认录用概率未下降
```

### 输出文件

```
humanlike/
├── paper_humanized.tex          # 改写版TEX
├── paper_humanized.pdf          # 改写版PDF
├── references.bib               # 参考文献复制
├── figures/                     # 图片文件夹复制
├── HUMANIZER_REPORT.md          # 改写报告
└── AI_DETECTION_BEFORE.md       # 改写前检测报告（可选）
```

### 改写报告模板

```markdown
# Humanizer改写报告

## 基本信息
- 原版路径: v_final/paper.tex
- 改写版路径: humanlike/paper_humanized.tex
- 改写日期: YYYY-MM-DD

## 改写前后对比

| 项目 | 原版 | 改写版 |
|------|:----:|:------:|
| 页数 | X页 | Y页 |
| 大小 | X KB | Y KB |
| AI生成概率 | A% | B% |

## 改写内容统计

| 改写类型 | 数量 | 示例 |
|---------|:----:|------|
| 过渡词替换 | N处 | Notably → Importantly |
| 句式变换 | N处 | 被动 → 主动 |
| 结构调整 | N处 | 段落重组 |

## 保持不变的内容

- ✅ 所有数据（XXX条记录）
- ✅ 所有参考文献引用
- ✅ 所有图表引用
- ✅ 因果语言控制
- ✅ 学术格式

## 主要改写示例

### 示例1: 句式变换
**原版**: This study documents the transformation...
**改写**: This paper tracks how...

## 结论
改写完成，AI生成检测概率从 A% 降至 B%。
```

### 注意事项

```
⚠️ Humanizer改写注意事项:

1. 数据保护
   ├── 检查所有数字是否保持不变
   ├── 检查所有百分比是否一致
   └── 检查所有统计量是否正确

2. 引用保护
   ├── 检查所有 \cite{} 是否完整
   ├── 检查引用编号是否正确
   └── 检查参考文献列表是否完整

3. 格式保护
   ├── 检查 Figure~\ref{} 是否正确
   ├── 检查 Table~\ref{} 是否正确
   └── 检查 Section~\ref{} 是否正确

4. 语言保护
   ├── 保持因果语言控制
   ├── 保持学术严谨性
   └── 避免口语化过度

5. 编译验证
   ├── 确保LaTeX编译成功
   ├── 确保PDF生成正常
   └── 确保无新增编译错误
```

### 与其他步骤的关系

```
Step 10 与其他步骤的关系:

├── Step 7（收敛判断后）
│   └── Step 10 可选执行，降低AI痕迹
│
├── Step 8（最终优化后）
│   └── Step 10 可选执行，降低AI痕迹
│
├── Step 9（篇幅优化后）
│   └── Step 10 推荐执行，作为最后语言润色
│
└── Step 11（最终清理前）
    └── Step 10 最后机会，在格式统一前改写

推荐执行顺序:
Step 7 → Step 8 → Step 9 → Step 10 → Step 11
```

### 压缩优先级

1. **P0（首选）**：冗余解释、重复数据、过度例举
2. **P1（次选）**：合并相似段落、精简过渡句
3. **P2（谨慎）**：压缩技术细节、简化方法论描述

### 压缩策略

| 章节类型 | 压缩策略 | 注意事项 |
|----------|----------|----------|
| Abstract | 精简背景铺垫 | 保留核心贡献 |
| Introduction | 压缩文献综述 | 保留研究问题 |
| Methods | 合并流程描述 | 保留关键参数 |
| Results | 精简数据列表 | 保留关键发现 |
| Discussion | 压缩背景重述 | 保留核心观点 |
| Conclusion | 合并段落 | **保留所有核心数据** |

### 压缩后验证

- ✅ 核心数据完整性检查
- ✅ 论证逻辑连贯性检查
- ✅ 引用完整性检查
- ✅ 必要时进行新一轮评审

---

## Step 11: 最终清理与格式统一

### A. 参考文献清理

#### 检测未被引用的文献

```bash
# Step 1: 提取被引用的文献
grep -o '\\cite[tp]*{[^}]*}' paper.tex | sed 's/\\cite[tp]*{//g; s/}//g' | tr ',' '\n' | sort -u > cited_keys.txt

# Step 2: 提取BibTeX中的所有文献
grep -E "^@\w+\{" references.bib | sed 's/^@\w*{//; s/,$//' | sort -u > bib_keys.txt

# Step 3: 找出未被引用的文献
comm -23 bib_keys.txt cited_keys.txt > uncited_keys.txt

# Step 4: 输出未引用文献详情
while read key; do
  echo "=== $key ==="
  grep -A10 "^@\w*{$key," references.bib | head -12
done < uncited_keys.txt
```

#### 相关性判断决策树

```
未引用文献处理:
│
├── 相关性判断
│   ├── ✅ 高度相关 → 在正文中补充引用
│   ├── ⚠️ 部分相关 → 评估后决定
│   └── ❌ 不相关 → 从BibTeX删除
│
├── 相关性判断标准
│   ├── 研究主题直接相关 → 高度相关
│   ├── 方法论相关 → 高度相关
│   ├── 对比分析需要 → 部分相关
│   ├── 深度学习基础/通用知识 → 不相关
│   └── 背景性弱 → 不相关
│
└── CCF等级参考（第七版目录）
    ├── CCF A类 → 质量最高，优先保留
    ├── CCF B类 → 质量较高，推荐保留
    ├── CCF C类 → 质量适中，适量保留
    └── 非CCF收录 → 谨慎评估
```

#### 参考文献质量标准

| 质量等级 | 期刊/会议类型 | 优先级 |
|----------|--------------|:------:|
| **CCF A类** | CCF推荐顶级会议/期刊 | 优先 |
| **CCF B类** | CCF推荐高质量会议/期刊 | 推荐 |
| **CCF C类** | CCF推荐合格会议/期刊 | 适量 |
| **高影响力期刊** | Nature, Science, Cell等 | 优先 |
| **预印本** | arXiv等 | 谨慎 |
| **非学术来源** | 媒体、博客等 | 避免 |

> **CCF目录参考**：第七版中国计算机学会推荐国际学术会议和期刊目录
> 网址：https://www.ccf.org.cn/Academic_Evaluation/By_category/

---

### B. 命名一致性检查

| 检查项 | 检查方法 | 修正标准 |
|--------|----------|----------|
| 平台命名 | 全文搜索关键词 | 统一术语 |
| 缩写定义 | 首次出现检查 | 首次定义后续统一 |
| 数据术语 | 方法章节定义 | 全文一致使用 |

---

### C. 格式统一检查

| 检查项 | 标准 |
|--------|------|
| Figure引用 | `Figure~\ref{}` 或 `Figures~\ref{},\ref{}` |
| Table引用 | `Table~\ref{}` |
| 章节引用 | `Section~\ref{}` |
| 公式编号 | 自动编号、正确引用 |
| 列表格式 | 统一使用itemize/enumerate |

---

### D. PDF完整性验证（必须执行）

> **⚠️ 关键要求**：Step 11必须执行完整的PDF验证流程，确保最终版PDF所有内容正确无误
> 
> **常见问题**：
> - 参考文献显示为数字，无实际内容（.bbl文件缺失）
> - 引用显示为"[?]"或问号（bibtex未运行）
> - 交叉引用显示为"??"（pdflatex只运行一次）
> - 图片显示为空白框（图片路径错误或文件缺失）

#### D.1 LaTeX完整编译流程（必须执行）

**标准编译流程**（必须按顺序执行4步）：

```bash
# 进入工作目录
cd /path/to/paper/directory

# Step 1: 首次pdflatex编译（生成.aux文件）
pdflatex -interaction=nonstopmode paper.tex

# Step 2: bibtex编译（生成.bbl文件，关键步骤！）
bibtex paper

# Step 3: 第二次pdflatex编译（解析引用）
pdflatex -interaction=nonstopmode paper.tex

# Step 4: 第三次pdflatex编译（确保交叉引用正确）
pdflatex -interaction=nonstopmode paper.tex

# 验证.bbl文件已生成
ls -lh paper.bbl
```

**为什么需要4步编译？**
1. `pdflatex` 第1次：生成 `.aux` 文件，记录所有 `\cite{}` 引用
2. `bibtex`：读取 `.aux` 和 `.bib`，生成 `.bbl` 文件（参考文献内容）
3. `pdflatex` 第2次：读取 `.bbl`，在PDF中渲染参考文献
4. `pdflatex` 第3次：确保所有交叉引用（Figure/Table引用）正确

**如果只运行pdflatex会出现什么问题？**
- ❌ 参考文献显示为数字，无文献内容
- ❌ 引用显示为"[?]"或问号
- ❌ 参考文献页空白或只有标题

---

#### D.2 参考文献正确性检查（核心检查）

**检查项目**：

| 检查项 | 检查方法 | 预期结果 | 异常处理 |
|--------|----------|----------|----------|
| **.bbl文件存在** | `ls paper.bbl` | 文件存在且大小>0 | 运行bibtex |
| **引用解析** | `pdftotext paper.pdf - \| grep "\[?\]"` | 无输出 | bibtex + pdflatex两次 |
| **文献内容渲染** | 打开PDF查看References章节 | 显示完整文献列表 | 检查references.bib格式 |
| **引用数量匹配** | 对比正文引用与参考文献数量 | 数量一致 | 检查未引用或缺失文献 |

**详细检查脚本**：

```bash
echo "========================================="
echo "   参考文献正确性检查"
echo "========================================="

# 1. 检查.bbl文件是否存在
echo -e "\n[1/5] 检查.bbl文件..."
if [ -f "paper.bbl" ]; then
  bbl_size=$(ls -lh paper.bbl | awk '{print $5}')
  bbl_lines=$(wc -l < paper.bbl)
  echo "  ✅ paper.bbl 存在 ($bbl_size, $bbl_lines 行)"
else
  echo "  ❌ paper.bbl 不存在！"
  echo "  → 解决方法：运行 'bibtex paper'"
fi

# 2. 检查PDF中是否有未解析的引用
echo -e "\n[2/5] 检查引用解析情况..."
unresolved=$(pdftotext paper.pdf - 2>/dev/null | grep -c "\[?\]" || echo "0")
if [ "$unresolved" -gt 0 ]; then
  echo "  ❌ 发现 $unresolved 个未解析引用（显示为[?]）"
  echo "  → 解决方法：检查\cite{}中的key是否在references.bib中存在"
  echo "  → 查看具体问题："
  pdftotext paper.pdf - 2>/dev/null | grep -n "\[?\]" | head -5
else
  echo "  ✅ 所有引用已正确解析"
fi

# 3. 检查参考文献章节内容
echo -e "\n[3/5] 检查参考文献内容..."
ref_content=$(pdftotext paper.pdf - 2>/dev/null | grep -A 50 "^References" | head -20)
if [ -z "$ref_content" ]; then
  echo "  ❌ 参考文献章节未找到或为空"
  echo "  → 解决方法：检查\bibliography{references}命令是否正确"
elif echo "$ref_content" | grep -q "^\[1\]"; then
  echo "  ✅ 参考文献内容正常渲染"
  ref_count=$(pdftotext paper.pdf - 2>/dev/null | grep -c "^\[[0-9]\+\]" || echo "0")
  echo "  参考文献数量: $ref_count"
else
  echo "  ⚠️ 参考文献格式可能异常"
  echo "  内容预览:"
  echo "$ref_content"
fi

# 4. 对比引用数量
echo -e "\n[4/5] 检查引用数量匹配..."
cited_keys=$(grep -o '\\cite[tp]*{[^}]*}' paper.tex | sed 's/\\cite[tp]*{//g; s/}//g' | tr ',' '\n' | sort -u | wc -l)
bib_keys=$(grep -E "^@\w+\{" references.bib | wc -l)
bbl_keys=$(grep -c "\\\\bibitem" paper.bbl 2>/dev/null || echo "0")
echo "  正文引用的不同文献数: $cited_keys"
echo "  references.bib中的文献数: $bib_keys"
echo "  paper.bbl中的文献数: $bbl_keys"
if [ "$cited_keys" -le "$bbl_keys" ]; then
  echo "  ✅ 引用数量正常"
else
  echo "  ⚠️ 正文引用的文献多于bbl中的文献，可能有未解析引用"
fi

# 5. 检查参考文献格式
echo -e "\n[5/5] 检查参考文献格式..."
if grep -q "\\\\bibliographystyle" paper.tex; then
  bibstyle=$(grep "\\\\bibliographystyle" paper.tex | head -1)
  echo "  参考文献样式: $bibstyle"
else
  echo "  ⚠️ 未找到\\bibliographystyle命令"
fi

echo -e "\n========================================="
```

---

#### D.3 图片嵌入正确性检查（核心检查）

**检查项目**：

| 检查项 | 检查方法 | 预期结果 | 异常处理 |
|--------|----------|----------|----------|
| **图片文件存在** | `ls figures/*.png` | 所有引用的图片存在 | 复制缺失图片 |
| **图片路径正确** | 检查`\includegraphics`路径 | 路径与实际文件匹配 | 修正路径 |
| **PDF中图片嵌入** | `pdfimages -list paper.pdf` | 显示所有图片 | 检查路径/格式 |
| **图片数量匹配** | 对比tex引用与PDF嵌入 | 数量一致 | 检查缺失图片 |

**详细检查脚本**：

```bash
echo "========================================="
echo "   图片嵌入正确性检查"
echo "========================================="

# 1. 检查figures目录
echo -e "\n[1/4] 检查figures目录..."
if [ -d "figures" ]; then
  img_count=$(ls figures/*.png figures/*.pdf figures/*.jpg 2>/dev/null | wc -l)
  echo "  ✅ figures目录存在，包含 $img_count 个图片文件"
  ls -la figures/ | head -10
else
  echo "  ❌ figures目录不存在！"
  echo "  → 解决方法：创建figures目录并复制图片文件"
fi

# 2. 提取tex中的图片引用
echo -e "\n[2/4] 检查tex中的图片引用..."
tex_images=$(grep -o '\\includegraphics\[[^]]*\]{[^}]*}' paper.tex | sed 's/.*{//; s/}//' | sort -u)
tex_img_count=$(echo "$tex_images" | grep -c "." || echo "0")
echo "  tex中引用的图片数量: $tex_img_count"
if [ $tex_img_count -gt 0 ]; then
  echo "  引用的图片列表:"
  echo "$tex_images" | head -10
fi

# 3. 检查引用的图片文件是否存在
echo -e "\n[3/4] 检查图片文件存在性..."
missing_count=0
for img in $tex_images; do
  if [ -f "$img" ]; then
    echo "  ✅ $img"
  else
    echo "  ❌ $img 缺失！"
    missing_count=$((missing_count + 1))
  fi
done
if [ $missing_count -eq 0 ]; then
  echo "  ✅ 所有图片文件都存在"
else
  echo "  ❌ 缺失 $missing_count 个图片文件"
  echo "  → 解决方法：复制缺失的图片到正确路径"
fi

# 4. 检查PDF中的图片嵌入
echo -e "\n[4/4] 检查PDF中的图片嵌入..."
if command -v pdfimages &> /dev/null; then
  pdf_img_count=$(pdfimages -list paper.pdf 2>/dev/null | grep -c "image" || echo "0")
  echo "  PDF中嵌入的图片数量: $pdf_img_count"
  if [ "$pdf_img_count" -ge "$tex_img_count" ] && [ "$pdf_img_count" -gt 0 ]; then
    echo "  ✅ 图片嵌入正常"
  elif [ "$tex_img_count" -eq 0 ]; then
    echo "  ⚠️ 论文无图片"
  else
    echo "  ❌ 警告：PDF图片数量($pdf_img_count)少于tex引用数量($tex_img_count)"
    echo "  → 解决方法：检查图片路径是否正确，重新编译"
  fi
  
  # 显示PDF中的图片详情
  echo -e "\n  PDF图片详情:"
  pdfimages -list paper.pdf 2>/dev/null | head -15
else
  echo "  ⚠️ pdfimages命令不可用，安装：apt-get install poppler-utils"
fi

echo -e "\n========================================="
```

---

#### D.4 交叉引用正确性检查（核心检查）

**检查项目**：

| 检查项 | 检查方法 | 预期结果 | 异常处理 |
|--------|----------|----------|----------|
| **Figure引用** | 检查`Figure~\ref{}` | 显示正确编号 | pdflatex编译两次 |
| **Table引用** | 检查`Table~\ref{}` | 显示正确编号 | pdflatex编译两次 |
| **Section引用** | 检查`Section~\ref{}` | 显示正确编号 | pdflatex编译两次 |
| **"??"标记** | `pdftotext paper.pdf - \| grep "??"` | 无输出 | pdflatex编译两次 |

**详细检查脚本**：

```bash
echo "========================================="
echo "   交叉引用正确性检查"
echo "========================================="

# 1. 检查未解析的交叉引用（"??"标记）
echo -e "\n[1/3] 检查未解析的交叉引用..."
double_question=$(pdftotext paper.pdf - 2>/dev/null | grep -c "??" || echo "0")
if [ "$double_question" -gt 0 ]; then
  echo "  ❌ 发现 $double_question 个未解析的交叉引用（显示为??）"
  echo "  → 解决方法：运行 'pdflatex paper.tex' 两次"
  echo "  → 查看具体位置："
  pdftotext paper.pdf - 2>/dev/null | grep -n "??" | head -5
else
  echo "  ✅ 所有交叉引用已正确解析"
fi

# 2. 检查Figure引用
echo -e "\n[2/3] 检查Figure引用..."
fig_refs=$(grep -o '\\ref{fig:[^}]*}' paper.tex | sort -u | wc -l)
fig_labels=$(grep -o '\\label{fig:[^}]*}' paper.tex | sort -u | wc -l)
echo "  Figure引用数: $fig_refs"
echo "  Figure标签数: $fig_labels"
if [ "$fig_refs" -gt "$fig_labels" ]; then
  echo "  ⚠️ 引用数多于标签数，可能有未定义的引用"
fi

# 3. 检查Table引用
echo -e "\n[3/3] 检查Table引用..."
tab_refs=$(grep -o '\\ref{tab:[^}]*}' paper.tex | sort -u | wc -l)
tab_labels=$(grep -o '\\label{tab:[^}]*}' paper.tex | sort -u | wc -l)
echo "  Table引用数: $tab_refs"
echo "  Table标签数: $tab_labels"
if [ "$tab_refs" -gt "$tab_labels" ]; then
  echo "  ⚠️ 引用数多于标签数，可能有未定义的引用"
fi

echo -e "\n========================================="
```

---

#### D.5 完整编译与验证流程（一键执行）

```bash
#!/bin/bash
# PDF完整编译与验证脚本
# 使用方法：./compile_and_verify.sh [paper]

PAPER="${1:-paper}"

echo "========================================="
echo "   LaTeX完整编译与验证"
echo "   论文: $PAPER"
echo "========================================="

# === Phase 1: 完整编译 ===
echo -e "\n[Phase 1] 完整编译流程..."

echo -e "\n  Step 1/4: pdflatex (第1次)..."
pdflatex -interaction=nonstopmode "$PAPER.tex" > /dev/null 2>&1
if [ $? -eq 0 ]; then
  echo "  ✅ pdflatex第1次成功"
else
  echo "  ❌ pdflatex第1次失败，查看日志："
  tail -20 "$PAPER.log"
  exit 1
fi

echo -e "\n  Step 2/4: bibtex..."
bibtex "$PAPER" 2>&1
if [ -f "$PAPER.bbl" ]; then
  bbl_size=$(ls -lh "$PAPER.bbl" | awk '{print $5}')
  echo "  ✅ bibtex成功，生成 $PAPER.bbl ($bbl_size)"
else
  echo "  ⚠️ bibtex完成但.bbl未生成，检查references.bib"
fi

echo -e "\n  Step 3/4: pdflatex (第2次)..."
pdflatex -interaction=nonstopmode "$PAPER.tex" > /dev/null 2>&1
echo "  ✅ pdflatex第2次成功"

echo -e "\n  Step 4/4: pdflatex (第3次)..."
pdflatex -interaction=nonstopmode "$PAPER.tex" > /dev/null 2>&1
echo "  ✅ pdflatex第3次成功"

# === Phase 2: 完整性验证 ===
echo -e "\n[Phase 2] 完整性验证..."

# 统计问题
issues=0

# 1. 参考文献检查
echo -e "\n  [1/4] 参考文献检查..."
unresolved=$(pdftotext "$PAPER.pdf" - 2>/dev/null | grep -c "\[?\]" || echo "0")
if [ "$unresolved" -gt 0 ]; then
  echo "  ❌ 发现 $unresolved 个未解析引用"
  issues=$((issues + 1))
else
  echo "  ✅ 引用解析正常"
fi

if [ ! -f "$PAPER.bbl" ]; then
  echo "  ❌ .bbl文件缺失"
  issues=$((issues + 1))
else
  echo "  ✅ .bbl文件存在"
fi

# 2. 图片嵌入检查
echo -e "\n  [2/4] 图片嵌入检查..."
tex_img=$(grep -o "includegraphics" "$PAPER.tex" 2>/dev/null | wc -l)
if [ $tex_img -gt 0 ]; then
  pdf_img=$(pdfimages -list "$PAPER.pdf" 2>/dev/null | grep -c "image" || echo "0")
  if [ "$pdf_img" -ge "$tex_img" ]; then
    echo "  ✅ 图片嵌入正常 ($pdf_img/$tex_img)"
  else
    echo "  ❌ 图片嵌入异常 (PDF: $pdf_img, TeX: $tex_img)"
    issues=$((issues + 1))
  fi
else
  echo "  ⚠️ 论文无图片"
fi

# 3. 交叉引用检查
echo -e "\n  [3/4] 交叉引用检查..."
double_q=$(pdftotext "$PAPER.pdf" - 2>/dev/null | grep -c "??" || echo "0")
if [ "$double_q" -gt 0 ]; then
  echo "  ❌ 发现 $double_q 个未解析交叉引用"
  issues=$((issues + 1))
else
  echo "  ✅ 交叉引用正常"
fi

# 4. 编译日志检查
echo -e "\n  [4/4] 编译日志检查..."
errors=$(grep -c "^!" "$PAPER.log" 2>/dev/null || echo "0")
warnings=$(grep -c "Warning:" "$PAPER.log" 2>/dev/null || echo "0")
if [ "$errors" -gt 0 ]; then
  echo "  ❌ 发现 $errors 个编译错误"
  issues=$((issues + 1))
else
  echo "  ✅ 无编译错误"
fi
echo "  编译警告数: $warnings"

# === Phase 3: 最终状态 ===
echo -e "\n[Phase 3] 最终状态..."
pages=$(pdfinfo "$PAPER.pdf" 2>/dev/null | grep "Pages:" | awk '{print $2}')
size=$(ls -lh "$PAPER.pdf" | awk '{print $5}')
echo "  PDF页数: $pages"
echo "  文件大小: $size"
echo "  发现问题数: $issues"

echo -e "\n========================================="
if [ $issues -eq 0 ]; then
  echo "   ✅ 验证通过，PDF可以使用"
else
  echo "   ❌ 发现 $issues 个问题，请修复后重新编译"
fi
echo "========================================="

exit $issues
```

---

### E. 清理检查清单

```
最终清理检查清单:
│
├── [ ] 参考文献清理
│   ├── [ ] 检测未引用文献
│   ├── [ ] 判断相关性
│   └── [ ] 执行删除或引用
│
├── [ ] 命名一致性
│   ├── [ ] 平台命名统一
│   ├── [ ] 缩写定义检查
│   └── [ ] 数据术语统一
│
├── [ ] 格式统一
│   ├── [ ] 图表引用格式
│   ├── [ ] 章节引用格式
│   └── [ ] 列表格式统一
│
├── [ ] PDF完整性验证（新增）
│   ├── [ ] 图片嵌入检查
│   ├── [ ] 参考文献渲染检查
│   ├── [ ] 交叉引用解析检查
│   ├── [ ] 文件完整性检查
│   └── [ ] 编译日志检查
│
└── [ ] 编译验证
    ├── [ ] LaTeX编译成功
    ├── [ ] BibTeX无警告
    └── [ ] PDF生成正常
```

---

## 📁 版本管理规范

### 文件夹结构

```
project/
├── v0/                          # Step 1: 期刊格式分析
├── v1/                          # Step 2: 数据核查
├── v2/                          # Step 4: 第一次修订
├── v3/                          # Step 6: 第二次修订
├── v4+/                         # Step 8: 最终优化
├── humanlike/                   # Step 10: Humanizer语言改写（新增）
│   ├── paper_humanized.tex
│   ├── paper_humanized.pdf
│   ├── references.bib
│   ├── figures/
│   ├── HUMANIZER_REPORT.md
│   └── reviews/                 # 改写版评审报告
├── v_final/                     # Step 11: 最终清理
└── reviews/                     # 评审报告
    ├── EvoScientist_round[N]_review.md
    ├── AutoResearchClaw_round[N]_review.md
    ├── AI-Research-SKILLs_round[N]_review.md
    ├── peer-reviewer_round[N]_review.md
    ├── CONSOLIDATED_round[N]_final.md
    └── data_verification_report.md
```

---

## ⚠️ 学术论文行文规范

### A. 因果推断措辞控制

#### ❌ 避免使用的因果语言

| 禁用词汇 | 问题 | 替代方案 |
|----------|------|----------|
| enabled | 暗示因果关系 | was observed alongside |
| caused | 直接因果声明 | coincided with |
| led to | 因果链条 | was associated with |
| resulted in | 因果结果 | followed |
| drove | 因果驱动 | accompanied |
| improved | 因果改善 | showed increase |

#### ✅ 推荐使用的关联语言

| 推荐词汇 | 适用场景 | 示例 |
|----------|----------|------|
| temporal correlation | 时间关联 | "Temporal correlation was observed between..." |
| coincided with | 时间重合 | "System upgrade coincided with..." |
| was associated with | 关联关系 | "Performance growth was associated with..." |
| was observed alongside | 同时观察 | "Changes in X were observed alongside Y" |
| followed | 时间顺序 | "Increase in X followed Y" |

---

### B. 理论贡献声称规范

#### ❌ 避免过度声称

| 禁用表述 | 问题 |
|----------|------|
| novel theoretical framework | 过度声称 |
| new theory | 过度声称 |
| groundbreaking framework | 过度声称 |
| first of its kind | 需要全面文献支持 |

#### ✅ 推荐谨慎表述

| 推荐表述 | 适用场景 |
|----------|----------|
| descriptive conceptual model | 描述性框架 |
| framework describing | 描述性框架 |
| roadmap for | 实践路线图 |
| guidelines for | 实践指南 |
| contributes to understanding of | 渐进贡献 |

---

### C. 学术论文结构规范

#### 章节结构

```
学术论文标准结构:
│
├── Abstract (150-300词)
│   ├── 背景 (1-2句)
│   ├── 问题 (1句)
│   ├── 方法 (1-2句)
│   ├── 主要发现 (2-3句)
│   └── 贡献/意义 (1-2句)
│
├── Introduction (10-15%篇幅)
│   ├── 研究背景
│   ├── 问题陈述
│   ├── 研究挑战
│   ├── 研究问题
│   ├── 贡献概述
│   └── 本文章节结构
│
├── Background/Related Work (10-15%篇幅)
│   ├── 核心概念
│   ├── 相关工作
│   └── 与本文关系
│
├── Approach/Method (15-25%篇幅)
│   ├── 技术框架
│   ├── 核心技术点
│   ├── 技术方法
│   └── 术语定义（重要！）
│
├── Results (15-25%篇幅)
│   ├── 实验设置和数据描述
│   ├── 主要发现
│   └── 详细分析
│
├── Discussion (15-20%篇幅)
│   ├── 结果解释
│   ├── 理论贡献
│   ├── 实践意义
│   └── 与文献对话
│
├── Limitations (5-10%篇幅)
│   ├── 方法学局限
│   ├── 数据局限
│   └── 推广限制
│
└── Conclusion (3-5%篇幅，约1页)
    ├── 研究总结
    ├── 核心贡献
    └── 未来方向
```

---

### D. 避免序号化表述

#### ❌ 避免的序号化表述

```
本研究有以下贡献：
(1) 实证贡献：提供了纵向数据...
(2) 理论贡献：提出了框架...
(3) 实践贡献：给出了建议...
```

#### ✅ 推荐的连贯表述

```
本研究做出三项主要贡献。从实证角度，本研究提供了纵向数据...从理论角度，本研究提出了渐进融合框架...从实践角度，本研究给出了设计原则...
```

---

### E. 数值表述规范

#### 数值格式

```
✅ 正确格式:
├── 大数：1,234,567（千位分隔符）
├── 百分比：40.2%（无空格）
├── 范围：2022-2025（半角连字符）
├── 倍数：3.5-fold
└── 置信区间：[2.05, 2.11]

❌ 错误格式:
├── 1234567（缺少分隔符）
├── 40.2 %（多余空格）
├── 2022~2025（错误连字符）
└── 3.5倍（中英文混用）
```

---

### F. 图表规范

#### 图表标题
- ✅ Figure标题在图下方
- ✅ Table标题在表上方
- ✅ 标题简洁但完整，包含关键信息

#### 图表引用

```latex
% 单图引用
Figure~\ref{fig:example} shows...

% 多图引用
Figures~\ref{fig:a} and \ref{fig:b} present...

% 单表引用
Table~\ref{tab:results} summarizes...

% 范围引用
Tables~\ref{tab:1}--\ref{tab:3} present...
```

---

## 📊 打分标准

| 评分 | 质量等级 | 录用概率 |
|:----:|---------|---------|
| 9-10 | 优秀 | 90%+ |
| 7-8 | 良好 | 70-85% |
| 5-6 | 中等 | 50-65% |
| 3-4 | 需大修 | 30-45% |
| 1-2 | 不建议投稿 | <30% |

---

## 🔗 参考资源

### 相关技能
- `EvoScientist` - 自进化AI科学家系统（`/usr/local/bin/EvoScientist`）
- `AutoResearchClaw` - 自主研究流程（`/usr/local/bin/researchclaw`）
- `peer-reviewer` - 多代理学术论文评审（`~/.openclaw/workspace/skills/peer-reviewer/`）
- `AI-Research-SKILLs` - 92个研究技能集合（`~/.openclaw/workspace/skills/AI-Research-SKILLs/`）

### 外部资源
- [CCF推荐目录（第七版）](https://www.ccf.org.cn/Academic_Evaluation/By_category/)
- [Neel Nanda: How to Write ML Papers](https://www.alignmentforum.org/posts/eJGptPbbFPZGLpjsp/)
- [Sebastian Farquhar: 5-Sentence Abstract](https://sebastianfarquhar.com/on-research/)
- [Gopen & Swan: The Science of Scientific Writing](https://cseweb.ucsd.edu/~swanson/papers/science-of-writing.pdf)
- [EvoScientist GitHub](https://github.com/EvoScientist/EvoScientist)
- [AutoResearchClaw GitHub](https://github.com/aiming-lab/AutoResearchClaw)

---

## Step 12: 批判性终审与修改建议

### 目的

在论文完成所有修订和优化后，从**拒稿视角**进行最后一轮全面审视，以最严苛的标准发现潜在问题，确保论文在投稿前达到最高质量。

### 核心原则

```
┌─────────────────────────────────────────────────────────────────────┐
│                    批判性终审核心原则                                 │
├─────────────────────────────────────────────────────────────────────┤
│  🎯 评审视角：假设你是审稿人，正在寻找拒稿理由                       │
│                                                                      │
│  ❌ 不要：                                                           │
│     ├── 客套话、表扬性评价                                           │
│     ├── 泛泛而谈的修改建议                                           │
│     ├── 忽略细节问题                                                 │
│     └── 过度宽容                                                     │
│                                                                      │
│  ✅ 要：                                                             │
│     ├── 直击要害，指出致命问题                                       │
│     ├── 与现有SOTA方法逐一对比                                       │
│     ├── 质疑每一个创新点                                             │
│     ├── 挑战实验设计的合理性                                         │
│     └── 深挖数据支撑的不足                                           │
└─────────────────────────────────────────────────────────────────────┘
```

### 评审执行流程

```
批判性终审执行流程:
│
├── [1] EvoScientist 终审
│   ├── 命令: EvoScientist --prompt "Critical final review from rejection perspective..." --mode run --auto-approve
│   ├── ⏳ 等待: 评审完成
│   └── ✅ 输出: reviews/EvoScientist_final_critical_review.md
│
├── [2] AutoResearchClaw 终审
│   ├── 命令: researchclaw run --config config.arc.yaml --stage 18 --mode critical
│   ├── ⏳ 等待: 评审完成
│   └── ✅ 输出: reviews/AutoResearchClaw_final_critical_review.md
│
├── [3] AI-Research-SKILLs 终审
│   ├── 操作: 加载 SKILL.md 执行批判性评审
│   ├── ⏳ 等待: 评审完成
│   └── ✅ 输出: reviews/AI-Research-SKILLs_final_critical_review.md
│
├── [4] peer-reviewer 终审
│   ├── 命令: node dist/index.js [paper_path] --mode reject
│   ├── ⏳ 等待: 评审完成
│   └── ✅ 输出: reviews/peer-reviewer_final_critical_review.md
│
└── [5] 综合整理
    ├── 整合四工具审稿意见
    ├── 分类整理所有问题
    ├── 形成修改建议清单
    └── ✅ 输出: reviews/FINAL_CRITICAL_REVIEW.md
```

### 评审维度与要点

#### A. 创新性质疑

| 质疑点 | 检查方法 | 潜在问题 |
|--------|----------|----------|
| **创新是否真实？** | 对比近3年SOTA论文 | 声称的创新可能已被他人解决 |
| **创新是否重要？** | 评估问题影响力 | 解决的问题可能不重要 |
| **创新是否显著？** | 量化改进幅度 | 改进幅度可能不足以支撑论文 |
| **创新是否通用？** | 测试场景覆盖 | 可能只在特定场景有效 |

#### B. 方法论批判

| 批判点 | 检查方法 | 潜在问题 |
|--------|----------|----------|
| **实验设计是否合理？** | 对照组设置、变量控制 | 可能存在混淆变量 |
| **数据集是否充分？** | 数据量、多样性、代表性 | 可能存在数据偏差 |
| **评估指标是否恰当？** | 指标选择、统计方法 | 可能存在指标选择偏差 |
| **对比是否公平？** | 对比方法版本、参数设置 | 可能存在不公平对比 |

#### C. 技术细节深挖

| 深挖点 | 检查方法 | 潜在问题 |
|--------|----------|----------|
| **超参数敏感性？** | 参数敏感性分析 | 方法可能对超参数过度敏感 |
| **计算复杂度？** | 时间/空间复杂度分析 | 实际可用性可能受限 |
| **可复现性？** | 代码、数据、环境说明 | 他人可能无法复现结果 |
| **失败案例？** | 错误案例分析 | 可能隐藏大量失败案例 |

#### D. 与SOTA对比不足

| 对比维度 | 检查方法 | 潜在问题 |
|----------|----------|----------|
| **覆盖广度** | 是否覆盖主流SOTA方法 | 可能遗漏重要对比方法 |
| **对比深度** | 是否深入分析差异 | 可能流于表面的数值对比 |
| **失败承认** | 是否承认方法不足 | 可能隐瞒方法劣势场景 |
| **公平性** | 是否使用相同条件 | 可能存在不公平对比 |

#### E. 写作与表达问题

| 问题类型 | 检查方法 | 潜在问题 |
|----------|----------|----------|
| **逻辑漏洞** | 逐段逻辑检查 | 推理可能存在跳跃 |
| **术语混乱** | 术语一致性检查 | 可能存在定义不清 |
| **过度声称** | 声称与证据对照 | 声称可能超出证据支撑 |
| **引用问题** | 引用完整性检查 | 可能存在选择性引用 |

### 评审报告模板

```markdown
# 批判性终审报告

## 基本信息
- 论文标题: [标题]
- 评审日期: YYYY-MM-DD
- 目标期刊: [期刊名]

---

## 一、拒稿风险评估

### 🔴 高风险拒稿理由（必须修改）

| 序号 | 问题 | 严重程度 | 页码/位置 | 修改建议 |
|:----:|------|:--------:|:---------:|----------|
| 1 | [具体问题描述] | 致命 | X页Y行 | [具体修改方案] |
| 2 | ... | ... | ... | ... |

### 🟡 中等风险问题（强烈建议修改）

| 序号 | 问题 | 严重程度 | 页码/位置 | 修改建议 |
|:----:|------|:--------:|:---------:|----------|
| 1 | [具体问题描述] | 重要 | X页Y行 | [具体修改方案] |
| 2 | ... | ... | ... | ... |

### 🟢 低风险问题（建议完善）

| 序号 | 问题 | 严重程度 | 页码/位置 | 修改建议 |
|:----:|------|:--------:|:---------:|----------|
| 1 | [具体问题描述] | 次要 | X页Y行 | [具体修改方案] |
| 2 | ... | ... | ... | ... |

---

## 二、与现有技术方法对比不足之处

### 2.1 遗漏的重要对比方法

| 方法名 | 发表信息 | 为何重要 | 未对比的影响 |
|--------|----------|----------|-------------|
| [方法A] | [期刊/会议, 年份] | [重要原因] | [影响分析] |
| [方法B] | ... | ... | ... |

### 2.2 对比不充分的方法

| 对比方法 | 不足之处 | 建议补充 |
|----------|----------|----------|
| [方法C] | [具体不足] | [补充内容] |
| [方法D] | ... | ... |

### 2.3 方法劣势场景未充分展示

| 场景 | 本方法表现 | SOTA表现 | 是否已展示 |
|------|:----------:|:--------:|:----------:|
| [场景A] | 较差 | 较好 | ❌ 未展示 |
| [场景B] | ... | ... | ... |

---

## 三、四工具评审意见汇总

### 3.1 EvoScientist 终审意见

**评分**: X/10

**主要问题**:
1. [问题1]
2. [问题2]
...

**修改建议**:
- [建议1]
- [建议2]
...

### 3.2 AutoResearchClaw 终审意见

**评分**: X/10

**主要问题**:
1. [问题1]
2. [问题2]
...

**修改建议**:
- [建议1]
- [建议2]
...

### 3.3 AI-Research-SKILLs 终审意见

**评分**: X/10

**主要问题**:
1. [问题1]
2. [问题2]
...

**修改建议**:
- [建议1]
- [建议2]
...

### 3.4 peer-reviewer 终审意见

**Merit Score**: X/10
**Logic Score**: X/10
**Novelty Score**: X/10

**主要问题**:
1. [问题1]
2. [问题2]
...

**修改建议**:
- [建议1]
- [建议2]
...

---

## 四、核心创新点质疑

### 创新点1: [创新点名称]

**论文声称**: [论文中的声称]

**质疑理由**:
- [质疑1]
- [质疑2]
...

**证据支撑不足之处**:
- [不足1]
- [不足2]
...

**修改建议**: [具体建议]

### 创新点2: [创新点名称]

...

---

## 五、实验设计问题深挖

### 5.1 数据集问题

| 问题类型 | 具体问题 | 影响评估 |
|----------|----------|----------|
| 数据量 | [具体问题] | [影响] |
| 数据偏差 | [具体问题] | [影响] |
| 数据来源 | [具体问题] | [影响] |

### 5.2 评估指标问题

| 问题类型 | 具体问题 | 影响评估 |
|----------|----------|----------|
| 指标选择 | [具体问题] | [影响] |
| 统计方法 | [具体问题] | [影响] |
| 显著性检验 | [具体问题] | [影响] |

### 5.3 对比实验问题

| 问题类型 | 具体问题 | 影响评估 |
|----------|----------|----------|
| 基线选择 | [具体问题] | [影响] |
| 参数设置 | [具体问题] | [影响] |
| 运行环境 | [具体问题] | [影响] |

---

## 六、写作问题清单

### 6.1 逻辑漏洞

| 位置 | 问题描述 | 修改建议 |
|------|----------|----------|
| X页Y段 | [问题] | [建议] |
| ... | ... | ... |

### 6.2 过度声称

| 位置 | 原文 | 问题 | 修改建议 |
|------|------|------|----------|
| X页Y行 | "[原文]" | [问题] | [建议] |
| ... | ... | ... | ... |

### 6.3 表达问题

| 位置 | 问题描述 | 修改建议 |
|------|----------|----------|
| X页Y段 | [问题] | [建议] |
| ... | ... | ... |

---

## 七、综合评估与建议

### 录用概率评估

| 评审工具 | 评分 | 录用概率预估 |
|----------|:----:|:------------:|
| EvoScientist | X/10 | X% |
| AutoResearchClaw | X/10 | X% |
| AI-Research-SKILLs | X/10 | X% |
| peer-reviewer | X/10 | X% |
| **综合评估** | **X/10** | **X%** |

### 必须修改项（P0）

- [ ] [修改项1]
- [ ] [修改项2]
...

### 强烈建议修改项（P1）

- [ ] [修改项1]
- [ ] [修改项2]
...

### 建议完善项（P2）

- [ ] [修改项1]
- [ ] [修改项2]
...

---

## 八、结论

**总体评价**: [简要总结论文质量]

**主要风险**: [列出最大的拒稿风险]

**核心建议**: [列出最重要的修改建议]

**是否建议投稿**: ✅ 建议投稿 / ⚠️ 修改后投稿 / ❌ 不建议投稿
```

### 输出文件

```
final/
├── paper_final.tex                    # 最终版论文
├── paper_final.pdf                    # 最终版PDF
├── references.bib                     # 参考文献
├── figures/                           # 图片文件夹
└── reviews/
    ├── EvoScientist_final_critical_review.md
    ├── AutoResearchClaw_final_critical_review.md
    ├── AI-Research-SKILLs_final_critical_review.md
    ├── peer-reviewer_final_critical_review.md
    └── FINAL_CRITICAL_REVIEW.md         # 综合终审报告
```

### 注意事项

```
⚠️ Step 12 执行注意事项:

1. 评审态度
   ├── 保持批判性思维
   ├── 不留情面地指出问题
   ├── 从审稿人视角审视
   └── 宁可严苛，不可宽容

2. 问题覆盖
   ├── 必须覆盖所有章节
   ├── 必须与SOTA逐一对比
   ├── 必须质疑每个创新点
   └── 必须深挖技术细节

3. 修改建议
   ├── 建议必须具体可操作
   ├── 指出问题位置（页码/行号）
   ├── 提供修改示例
   └── 区分优先级

4. 后续处理
   ├── 根据P0问题决定是否需要新一轮修订
   ├── 整理修改清单
   ├── 必要时返回Step 4/6进行修订
   └── 最终确认投稿准备完成
```

---

## 📝 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| 1.0.0 | 2026-03-31 | 初始版本 |
| 2.0.0 | 2026-04-01 | 双模块架构：评审器 + 修订器 |
| 3.0.0 | 2026-04-01 | 8步骤工作流程 |
| 4.0.0 | 2026-04-01 | 添加EvoScientist技能文件 |
| 5.0.0 | 2026-04-01 | 四工具评审机制 |
| 5.1.0 | 2026-04-01 | 双工具修订+合并机制 |
| 6.0.0 | 2026-04-01 | 全面梳理整理：结构优化、要点明确 |
| 6.0.1 | 2026-04-01 | 完善依赖项说明 |
| 7.0.0 | 2026-04-02 | **重大更新**：新增Step 9/10、细化数据核查、完善参考文献管理、扩充行文规范、多维度收敛判断 |
| 7.0.1 | 2026-04-02 | **通用化处理**：移除具体论文相关示例词汇（HPC/AI/GPU等），改用通用抽象名词 |
| 7.0.2 | 2026-04-02 | **新增PDF完整性验证**：Step 11新增D节"PDF完整性验证"，包括图片嵌入检查、参考文献渲染检查、交叉引用检查、一键验证脚本 |
| 7.1.0 | 2026-04-02 | **新增Step 9.5 Humanizer语言改写**：降低AI生成检测概率，包含过渡词替换表、句式变换策略、结构调整策略、完整执行流程 |
| 7.2.0 | 2026-04-03 | **重大更新**：①新增Step 12批判性终审与修改建议（从拒稿视角评审）；②调整步骤编号：原Step 9.5→Step 10，原Step 10→Step 11，形成完整12步骤流程 |
| 7.3.0 | 2026-04-03 | **批判性评审全面升级**：①Step 3/5/7评审流程改为批判性拒稿视角评审；②新增五大评审维度（创新性质疑、方法论批判、技术细节深挖、与SOTA对比不足、写作问题）；③新增批判性评审报告模板；④Step 4/6修订流程增加Phase 0问题提取与优先级排序；⑤新增修订后验证清单 |
| 7.4.0 | 2026-04-03 | **强制执行要求**：新增"强制执行要求"章节，明确禁止跳过步骤、禁止提前终止、禁止省略输出，规定完整输出目录结构要求 |
| **7.5.0** | **2026-04-04** | **Step 11 PDF完整性验证大幅增强**：①新增D.1 LaTeX完整编译流程（解释为什么需要4步编译）；②新增D.2 参考文献正确性检查（5项核心检查）；③新增D.3 图片嵌入正确性检查（4项核心检查）；④新增D.4 交叉引用正确性检查（3项核心检查）；⑤新增D.5 完整编译与验证脚本（一键执行）；⑥所有检查都提供完整的shell脚本 |
