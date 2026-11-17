---
name: active-causal-experiment
description: 因果世界模型主动实验（Active Causal Experiment Design）。面对多个候选因果结构时，不被动观察，而是主动设计干预 do-operation，用期望信息增益/最优实验设计挑选最能区分候选结构的实验，Bayesian 更新后验，以最少实验辨识真实因果结构。当需要主动做实验以最快弄清变量间因果关系、设计 A/B 或干预实验、在多个竞争因果假设中高效辨识时使用。
version: 1.0.0
agent_created: true
---

# active-causal-experiment · 因果世界模型主动实验

## 这是什么

一线大模型能「读懂」因果图，却缺少「为了辨别因果结构，下一步该做哪个干预实验最划算」的
**主动实验设计**闭环。本技能把它工程化：给定一族竞争的候选因果结构，自动选出信息量最大的
干预（do-operation），执行、观测、Bayesian 更新后验，直至以最少实验辨识出真实因果结构。

## 核心机制

```
候选结构族 H  →  对每个候选预测 do(X=x) 下的结果分布
→  期望信息增益 EIG(a)=I(H;O|a)=H(prior)-E_o[H(post|o)]
→  选 argmax EIG 的干预（最优实验设计，避开零信息干预）
→  对真实世界执行该干预、观测、Bayesian 更新后验
→  重复直到某结构后验≥阈值（辨识收敛）
```

关键优势：**主动避开零信息干预**。例如链结构 X→Y→Z 与叉结构 X→(Y,Z) 在 do(X) 下预测完全相同，
do(X) 信息增益为 0；本技能自动改选 do(Y) / do(Z) 这类能区分候选的干预，比朴素「按顺序都试一遍」
更快收敛。

## 使用

```bash
python scripts/active_causal.py --selftest   # 自检（5 场景全 PASS）
python scripts/active_causal.py --demo       # 演示：3 变量因果结构主动辨识
```

编程接口：
- `CausalHypothesis(name, edges, variables)`：一个候选因果结构（有向边 + 前向传播语义）。
- `expected_information_gain(hyps, belief, do_var, do_val)`：某干预的期望信息增益。
- `rank_interventions(hyps, belief)`：按信息增益给所有候选干预排序（最优实验设计）。
- `active_experiment_loop(hyps, true_hyp, threshold)`：完整主动实验辨识闭环，返回 trace。
- `bayesian_update(...)`：观测后的后验更新。

## selftest 覆盖

1. 零信息干预 do(X) 的 EIG 精确为 0，可区分干预 do(Y)/do(Z) 高信息。
2. 最优实验排序首选 do(Y)/do(Z)、do(X) 垫底。
3. 真实结构辨识收敛（后验≥0.85）且全程不浪费在零信息干预。
4. 主动 vs 朴素基线：主动实验数不劣于朴素（常更少）。
5. 信息增益递减：决定性实验后剩余不确定性下降。

## 设计要点

- 观测带 eps 噪声地板，避免后验塌缩为精确 0，保证鲁棒。
- 干预语义严格遵守 do-calculus：切断被干预变量入边，效应只向下游传播。
- 纯标准库，零依赖，确定性可复现。

---

## 自进化学习系统（越用越好用、越用越高效）

本技能内置通用学习模块 `scripts/learner.py`。每次使用后自动复盘、积累经验，逐步提升输出质量与执行效率，无需人工维护。

### 记忆文件
`learned_patterns.json`（位于本技能目录）记录：操作总数、各能力使用频次、错误模式、用户偏好、改进建议。

### 使用后请调用（Bash）

```bash
# 记录一次成功使用（--capability 填本次主要能力名，如「简历优化」「比价」）
python scripts/learner.py record <本技能目录> --capability 简历优化
# 记录一次失败/异常
python scripts/learner.py record <本技能目录> --capability 简历优化 --fail --error 格式识别失败 --note "用户上传了非标准文件"
# 记录用户偏好（下次直接使用）
python scripts/learner.py prefer <本技能目录> --key 输出语言 --val 中文
# 查看累计洞察（高频能力 / 反复错误）
python scripts/learner.py insight <本技能目录>
# 自动复盘（错误≥3次 或 操作≥10次 时给出改进建议）
python scripts/learner.py reflect <本技能目录>
```

### 迭代规则
- **错误累计 ≥3 次** → 主动增加预检/兜底步骤，并将经验回写本 SKILL.md。
- **操作数 ≥10 次** → 分析高频能力优先打磨示例与质量，低频能力评估精简或合并。
- **重要用户偏好** → 写入 `learned_patterns.json`，下次调用直接采用，减少重复询问。

> 越用越懂你：第一次用是通用能力，第十次用已沉淀为你专属的最佳实践。
