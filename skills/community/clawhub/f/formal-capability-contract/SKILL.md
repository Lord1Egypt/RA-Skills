---
name: formal-capability-contract
version: 1.0.0
description: |
  形式化能力契约与可证正确：给 agent 的每个能力（动作/函数/规划步骤）定义前置条件/后置条件/不变量，
  用契约校验器对一次真实执行轨迹做可机器验证的"该能力这次是否真的正确"判定，而非启发式信任。
  这是把能力信任从话术升级为可证明的元能力。当用户要求形式化验证、可证正确、能力契约、前置后置不变量时使用。
agent_created: true
visibility: public
---

# formal-capability-contract —— 形式化能力契约与可证正确

目标：把"能力信任"从**启发式/话术**升级为**可机器验证**——给每个能力定义
`pre`（前置）/ `post`（后置）/ `invariant`（不变量），对一次真实执行轨迹做确定性判定。

## 为什么需要

- **reason-verify** 是文本可靠性（模糊打分）；
- 本技能是**结构化契约**（输入/输出/状态的可执行断言），给出"该能力这次执行是否满足其形式化规约"的
  **确定性结论**，是"可信地超越"的硬保证层。

## 契约与校验（scripts/contract.py，真实可跑）

`Contract(name, pre, post, invariant)` + `verify_capability(contract, traces)`：

1. **PRE（前置条件）**：执行前必须成立（如 除数 != 0）。
2. **POST（后置条件）**：执行后必须成立（如 `output * b == a`）。
3. **INVARIANT（不变量）**：全程不得破坏（如 状态长度守恒）。
4. 校验器对每条轨迹逐一评估三子句，返回 `{satisfied, failed_clause, verdict}`；
   `verify_capability` 汇总一组轨迹的可证正确率 `provable_score`。

## 用法

```bash
python scripts/contract.py --selftest
python scripts/contract.py --demo
```

## 输出

`verify_capability` 返回：`capability` / `total` / `passed` / `provable_score` /
`verdict`（"可证明正确" / "存在契约违反"）/ `results[]`(每条轨迹的违反子句)。

## 设计要点

- **真能跑**：`contract.py --selftest` 用 安全除法 / 列表排序 两个契约，断言：
  good 通过、除数为0 精准定位 `pre` 违反、错误商定位 `post` 违反、
  排序长度丢失同时破 `post`+`invariant`、全绿套件判"可证明正确"。
- **确定性**：返回违反的是哪一子句（pre/post/invariant），可定位、可审计。
- **可被度量**：`provable_score` 量化"该能力在轨迹套件上的可证正确率"。

## 自进化学习系统

本技能自身也遵循自进化：每次使用 `record` 回写成败、用户偏好，并据错误模式自动复盘改进。
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
