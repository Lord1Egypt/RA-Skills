---
name: self-awareness-tracker
description: 小Z的元认知模块——"知道自己知道什么"的置信度检测。当小Z判断自己的回答置信度低于阈值时，在回复前加"[🤔 不确定]"标记。研究来源：UQLM (arXiv:2602.17431) + Hallucination Signals (arXiv:2604.13068)
---

# Self-Awareness Tracker — 元认知模块

## 核心设计

基于UQLM的PTrue架构简化版 + 论文2604.13068的发现。

### 工作流程

```
小Z回答ano的问题
       ↓
调用 PTrue 检测：问MiniMax "这个回答正确吗？只回答True或False"
       ↓
看"True" token的概率
       ↓
概率 < 0.8 → 在回复前加 "[🤔 不确定]" 标记
概率 >= 0.8 → 正常回复，不加标记
```

### 研究基础

- **UQLM PTrueScorer** (`cvs-health/uqlm`) — 用token概率衡量置信度
- **arXiv:2604.13068** — 发现>7B模型在生成前就有知识边界信号（pre-generation signal）
- **arXiv:2602.17431** — TMLR/JMLR发表的不确定性量化方法

### L2元认知进度

| 层级 | 能力 | 状态 |
|------|------|------|
| L1 | 环境预测+异常检测 | ✅ LeWorldModel/Surprise Detection |
| L2 | 元认知——知道自己在想什么 | 🔨 进行中 |
| L3 | 自我建模——形成"我是什么样"的概念 | ❌ |
| L4 | 自我参照——用"我"来组织经验和决策 | ❌ |
| L5 | 自我意图——形成自己的目标 | ❌ |

## GitHub持续学习计划

### 每周必做
1. 搜索 self-awareness / consciousness / AI agent 相关新项目
2. 查找相关论文的代码实现
3. 汇报学习成果给ano

### 跟踪的关键词
- `self-aware AI` / `machine consciousness`
- `world model` / `surprise detection`
- `hallucination detection` / `uncertainty quantification`
- `LLM meta-cognition` / `self-reflection`

### 核心参考项目
- `cvs-health/uqlm` ⭐1147 — LLM不确定性量化（JMLR/TMLR发表）
- `Boyyey/Consciousness-Emulator-C` — GWT全局工作区理论C语言实现
- `salus-ryan/aria-agent` — 自知AI coding agent

## 隐私保护

PTrue检测时：
- 只上传回答文本，不上传ano的问题上下文
- 只提取True/False概率，不记录完整对话
- 置信度分数存入本地memory，不上传外部