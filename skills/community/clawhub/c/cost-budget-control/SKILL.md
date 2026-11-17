---
name: cost-budget-control
version: 1.0.0
description: |
  成本与算力预算控制：对每次推理与工具调用做 token 与成本预算估算与硬性拦截，并提供
  压缩降本建议，让超级智能体可规模化、可控成本地运行，是可靠超越的落地前提。
agent_created: true
visibility: public
---

# cost-budget-control（成本与算力预算控制）

> 由 meta-evolver 在「智能体评估与可信部署」域构建。解决"无限调用导致成本失控"的规模化死穴：
> 把每次推理/工具调用都框在预算内，超预算即拦截，并给压缩建议，使"超越一线大模型"可规模化。

## 何时使用
- 长程自主任务（super-agent-loop）中，需对每步 LLM 调用设 token/成本上限，防跑飞。
- 批量处理（评测套件、数据流水线）前先估算总成本，超预算预警。
- 上下文过长时，按重要性压缩以降低单位算力产出成本。

## 工作流
1. **估算**：`estimate(prompt_tokens, completion_tokens)` 按单价算总成本。
2. **拦截**：`enforce(estimated_cost, estimated_tokens)` 超成本或超 token 任一项即 `allowed=False`。
3. **压缩**：`compress(text, keep_ratio)` 按句子重要性（长度+数字+专名密度）抽取式压缩。
4. **闭环**：拦截信号可触发反思/降级（接 reflection-replanner、metacognitive-monitoring）。

## 脚本
`scripts/budget_control.py`（纯标准库）：
- `Budget` 类：`estimate` / `enforce` / `compress`（静态方法）。
- CLI：`--selftest` 自检；`estimate` / `enforce` / `compress` 子命令。

## 自验证
```bash
python scripts/budget_control.py --selftest
```
断言：成本估算正确；超成本/超 token 双重拦截；压缩后变短且保留关键数字句。

## 与四引擎闭环的关系
- 度量层：与 agent-eval-harness 并列，为 super-agent 提供「成本健康度」。
- 安全层：超预算拦截是 safety-guardrails（本域另一缺口）的量化执行器。

## 已知限制
- 单价为静态配置，未接实时计费 API；多模型混合单价需外层封装。
- compress 为轻量抽取式，语义压缩建议接 inference-efficiency 的上下文压缩。

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