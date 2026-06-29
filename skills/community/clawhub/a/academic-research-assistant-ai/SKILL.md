---
name: Academic Research & Paper Writing Assistant
slug: academic-research-assistant
description: >
  学术论文写作与科研全流程助手。覆盖文献检索/综述生成/实验设计/数据分析/
  论文撰写(IMRaD)/期刊匹配/审稿回复/基金申请。支持LaTeX/Word/Overleaf，
  内置SCI/EI/中文核心期刊数据库信息，含各学科写作规范和伦理指引。
version: 1.0.0
author: ai-gaoqian
tags:
  - academic
  - research
  - paper-writing
  - latex
  - literature-review
  - journal-matching
  - grant-writing
  - peer-review
metadata:
  openclaw:
    emoji: "📚"
    requires: "OpenClaw >= v2026.3.22"
---

# Academic Research & Paper Writing Assistant

## 核心能力

| 能力维度 | 覆盖范围 | 输出质量 |
|----------|----------|----------|
| 文献检索 | 100+ 数据库检索策略 | 含检索式 + 筛选标准 |
| 综述生成 | PRISMA框架 / 系统综述 / Meta分析 | 含文献筛选流程图 |
| 实验设计 | 对照设计/正交/响应面/DOE | 含统计功效计算 |
| 数据分析 | SPSS/R/Python/Stata/GraphPad | 含代码 + 结果解读 |
| 论文撰写 | IMRaD/LaTeX/各期刊模板 | 含语言润色 + 格式检查 |
| 期刊匹配 | 10000+ SCI/SSCI/EI期刊信息 | 含影响因子 + 审稿周期 |
| 基金申请 | NSFC/国家社科/Horizon Europe | 含申请书框架 + 预算 |
| 审稿回复 | 逐条回复策略 | 含礼貌措辞模板 |

## 触发场景

- "帮我做XX方向的文献综述"
- "这个实验设计有什么问题"
- "帮我写论文的Methods部分"
- "推荐适合投的SCI期刊（IF 5-10）"
- "审稿意见怎么逐条回复"
- "基金申请书框架怎么写"
- "帮我做Meta分析"
- "论文英文润色和语法检查"
- "如何写Cover Letter"
- "数据分析用SPSS还是R"

## 文献检索策略矩阵

### 数据库选择

| 数据库 | 学科覆盖 | 特色功能 | 访问方式 |
|--------|----------|----------|----------|
| Web of Science | 全学科 | JCR/ESI引文分析 | 机构订阅 |
| Scopus | 全学科（偏理工） | CiteScore/学者画像 | 机构订阅 |
| PubMed | 生物医学 | MeSH主题词/免费全文 | 免费 |
| IEEE Xplore | 电子/计算机/通信 | 标准/会议 | 机构订阅 |
| ACM DL | 计算机科学 | 会议/期刊 | 机构订阅 |
| ScienceDirect | 理工医 | 全文下载 | 机构订阅 |
| SpringerLink | 全学科 | 图书/期刊/丛书 | 机构订阅 |
| CNKI | 中文学术 | 学位论文/年鉴/专利 | 机构订阅 |
| Wanfang | 中文学术 | 标准/专利/成果 | 机构订阅 |
| arXiv | 物理/数学/CS/AI | 预印本/开放获取 | 免费 |
| ResearchGate | 全学科 | 学者网络/全文请求 | 免费 |
| Google Scholar | 全学科 | 引用追踪/全文链接 | 免费 |

### 检索式构建原则

```
PICO框架（临床/健康类）：
  P (Population/Problem): 研究对象/问题
  I (Intervention): 干预措施
  C (Comparison): 对照
  O (Outcome): 结局指标

PICOS框架（扩展）：
  上+ S (Study Design): 研究设计

SPIDER框架（定性研究）：
  S (Sample): 样本
  PI (Phenomenon of Interest): 感兴趣的现象
  D (Design): 研究设计
  E (Evaluation): 评估
  R (Research type): 研究类型

PEO框架（流行病学）：
  P (Population): 人群
  E (Exposure): 暴露因素
  O (Outcome): 结果
```

## PRISMA 2020 综述流程图

```
┌──────────────────────────────────────┐
│ 数据库检索获得记录 (n = ____)        │
│ WoS:___ Scopus:___ PubMed:___        │
│ 其他来源:___                          │
└──────────────┬───────────────────────┘
               │ 去重
               ▼
┌──────────────────────────────────────┐
│ 去重后记录 (n = ____)                │
└──────────────┬───────────────────────┘
               │ 标题/摘要筛选
               ▼
┌──────────────────────────────────────┐
│ 筛选后记录 (n = ____)                │
│ 排除记录 (n = ____)：                │
│   不相关主题: ___                    │
│   非英文: ___                        │
│   无法获取全文: ___                  │
└──────────────┬───────────────────────┘
               │ 全文阅读评估
               ▼
┌──────────────────────────────────────┐
│ 合格全文 (n = ____)                  │
│ 排除全文 (n = ____)，原因:          │
│   研究设计不合适: ___                │
│   数据不完整: ___                    │
│   重复发表: ___                      │
└──────────────┬───────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│ 纳入最终分析的研究 (n = ____)        │
└──────────────────────────────────────┘
```

## 实验设计指南

### 常用实验设计

| 设计 | 适用场景 | 优点 | 缺点 | 统计方法 |
|------|----------|------|------|----------|
| 完全随机 | 单因素/均匀实验材料 | 简单/稳健 | 效率低 | t检验/ANOVA |
| 随机区组 | 已知变异来源 | 降低误差 | 失灵活 | 双因素ANOVA |
| 拉丁方 | 控制2个阻塞因素 | 高效 | 假设严格 | 拉丁方ANOVA |
| 析因设计 | 多因素交互 | 交互分析 | 规模大 | 析因ANOVA |
| 正交设计 | 多因素/多水平 | 减少试验 | 失交互 | 极差/方差分析 |
| 响应面(CCD) | 优化工艺参数 | 曲面拟合 | 需中心点 | RSM/二阶回归 |
| Box-Behnken | 3水平优化 | 无极端点 | 因子数<5 | RSM |
| 裂区设计 | 因子有难易 | 经济 | 分析复杂 | 裂区ANOVA |
| 重复测量 | 时间序列/个体 | 控制个体差异 | 脱落风险 | 重复测量ANOVA |
| 交叉设计 | 自身对照 | 高效 | 洗脱期要求 | 交叉设计分析 |

### 样本量计算（常用规则）

| 分析方法 | 最小样本量建议 | 依据 |
|----------|---------------|------|
| 独立t检验 | 每组≥30 | CLT < 30 |
| 配对t检验 | ≥30对 | 同上 |
| 单因素ANOVA | 每组≥20 | 组间方差比 |
| 多元回归 | 10×变量数 | Green (1991) |
| 逻辑回归 | 10×事件数/变量 | Peduzzi (1996) |
| 因子分析 | 5-10×条目数 | 样本量规则 |
| SEM | 10-20×参数数 | Kline (2015) |
| Meta分析 | ≥10项研究 | 异质性评估 |

### 统计功效分析

```
G*Power 常用设置：
  α = 0.05 (类型I错误)
  Power = 0.80 (类型II错误 = β = 0.20)
  Effect size: d=0.2 (小), d=0.5 (中), d=0.8 (大)

Cohen's d 效应量解读：
  < 0.2: 可忽略
  0.2 - 0.5: 小
  0.5 - 0.8: 中
  > 0.8: 大
```

## LaTeX 论文模板

### 基础IMRaD结构

```latex
\documentclass[12pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amssymb}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{natbib}
\usepackage{hyperref}

\title{Your Title Here}
\author{Author One\textsuperscript{1}, Author Two\textsuperscript{2}}
\date{}

\begin{document}
\maketitle

\begin{abstract}
% 250-300 words
Background: ...
Methods: ...
Results: ...
Conclusions: ...
\end{abstract}

\section{Introduction}
% 背景 → 研究缺口 → 研究目的/假设

\section{Methods}
\subsection{Participants / Materials}
\subsection{Experimental Design}
\subsection{Statistical Analysis}

\section{Results}

\section{Discussion}
\subsection{Principal Findings}
\subsection{Comparison with Previous Studies}
\subsection{Limitations}
\subsection{Implications}

\section{Conclusions}

\bibliographystyle{plainnat}
\bibliography{references}

\end{document}
```

## SCI期刊匹配速查

### 计算机/AI领域

| 期刊 | IF (2024) | 审稿周期 | 接受率 | OA费用 |
|------|-----------|----------|--------|--------|
| IEEE TPAMI | 23.6 | 6-12月 | ~10% | $2195 |
| IJCV | 19.5 | 6-9月 | ~15% | 非强制 |
| IEEE TIP | 10.6 | 4-8月 | ~20% | $2195 |
| CVPR | N/A(顶会) | 3-4月 | ~22% | 注册费 |
| ICCV | N/A(顶会) | 3-4月 | ~22% | 注册费 |
| NeurIPS | N/A(顶会) | 3-4月 | ~26% | 注册费 |
| ICML | N/A(顶会) | 3-4月 | ~25% | 注册费 |
| ACM Computing Surveys | 23.8 | 3-6月 | 约稿 | 非强制 |

### 材料/化学

| 期刊 | IF | 审稿周期 | 接受率 |
|------|-----|----------|--------|
| Nature Materials | 41.2 | 3-6月 | ~8% |
| Advanced Materials | 29.4 | 2-4月 | ~15% |
| ACS Nano | 17.1 | 2-4月 | ~18% |
| Angew Chem Int Ed | 16.6 | 2-3月 | ~20% |
| Small | 13.3 | 2-4月 | ~25% |
| Chemical Engineering Journal | 15.1 | 1-3月 | ~30% |

### 生物医学

| 期刊 | IF | 审稿周期 | 接受率 |
|------|-----|----------|--------|
| Lancet | 168.9 | 2-4月 | ~5% |
| NEJM | 158.5 | 2-3月 | ~5% |
| Nature Medicine | 82.9 | 2-4月 | ~8% |
| BMJ | 93.6 | 2-3月 | ~8% |
| Cell | 64.5 | 2-4月 | ~10% |
| Science Transl Med | 17.1 | 2-4月 | ~15% |

## 审稿意见回复模板

### 通用结构

```
Dear Editor [Name],

We sincerely thank you and the reviewers for the constructive
comments and suggestions. We have carefully addressed each point
raised. Below, we provide a point-by-point response. All changes
in the manuscript are highlighted in red/tracked changes.

Reviewer 1
----------
Comment 1: [原文转述]
Response: [回应，先说做了什么修改，再解释原因]
Action: [说明在稿件中的具体位置，如 Page 5, Lines 120-135]

Comment 2: ...
Response: ...
Action: ...

Reviewer 2
----------
...

We hope the revised manuscript meets the standards of [Journal Name].

Sincerely,
[Corresponding Author]
```

### 常见审稿意见回应策略

| 审稿人反馈类型 | 回应策略 | 措辞示例 |
|----------------|----------|----------|
| 补充实验 | 能做就做；不能做说清楚为什么，并讨论局限性 | "We acknowledge this limitation and have added a discussion..." |
| 统计方法质疑 | 解释选择；或补充替代分析 | "We chose [method] because... We have also conducted [alternative] as suggested" |
| 文献遗漏 | 补充引用并致谢 | "We thank the reviewer for pointing this out. We have now cited..." |
| 写作/语法 | 全面修改并注明 | "We have thoroughly revised the manuscript for language" |
| 结果过度解读 | 弱化措辞 | "We have toned down our claims as suggested" |
| 结构/组织问题 | 重新组织 | "We have restructured Section X as recommended" |

## 基金申请书框架

### NSFC面上项目

```
一、立项依据与研究内容
  1.1 立项依据（研究意义、国内外现状分析）
  1.2 研究目标
  1.3 研究内容
  1.4 关键科学问题
  1.5 技术路线（含流程图）

二、研究方案与可行性分析
  2.1 研究方案（分阶段详细描述）
  2.2 可行性分析
  2.3 创新点

三、研究基础与工作条件
  3.1 前期研究基础
  3.2 实验条件
  3.3 团队介绍

四、预期成果
  4.1 论文/专利/人才培养
  4.2 科学/应用价值

五、经费预算
  5.1 各科目预算及说明
```

## 学术伦理检查清单

- [ ] 数据真实性：原始数据可追溯
- [ ] 图像处理：未篡改（仅允许整体亮度/对比度调整）
- [ ] 引用完整：所有引用来源已标注
- [ ] 作者贡献：所有作者满足ICMJE标准
- [ ] 利益冲突：已声明
- [ ] 伦理审批：涉及人/动物的研究已获批
- [ ] 数据共享：遵循FAIR原则
- [ ] 未一稿多投
- [ ] AI辅助声明：如使用AI工具，已按期刊要求声明

## 注意事项

1. 系统综述必须遵循PRISMA 2020声明
2. 涉及人类受试者的研究需提供伦理委员会批准号
3. 临床试验需在公开注册平台预注册（如ClinicalTrials.gov）
4. 生成式AI在论文中的使用需按期刊要求披露（如Elsevier/Wiley/Nature均已发布AI使用政策）
5. 论文查重建议控制在15%以下（整体相似度）
6. 基金申请中的预算编制需遵循当年《国家自然科学基金资助项目资金管理办法》

## 定价

¥0.50/次，使用支付宝AI收协议。每次调用提供完整的文献检索/综述框架/实验设计/论文撰写指导/期刊匹配/审稿回复方案。
