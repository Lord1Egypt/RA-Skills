---
name: agent-eval-harness
version: 1.0.0
description: |
  智能体回归评测：用一组回归测试用例驱动 agent 并量化通过率，与历史基线比对自动标记能力
  回退，让超级智能体是否真在超越一线大模型变得可度量、可审计、可防止退化。
agent_created: true
visibility: public
---

# agent-eval-harness（智能体回归评测）

> 由 meta-evolver 在「智能体评估与可信部署」域构建。解决"自我宣称超越却无法度量"的空话：
> 把能力变成可重复跑的测试套件与通过率曲线，是北极星最后一公里"可被度量"的落地层。

## 何时使用
- 想验证某次技能/提示词/模型升级后 agent 能力是否真的变强、有无回退。
- 持续监控生态内关键技能的回归（CI 式跑测试套件）。
- 给 meta-evolver 的「反思驱动重规划」提供客观通过率信号，而非主观感觉。

## 工作流
1. **定义用例**：`TestCase(cid, prompt, expect_contains | expect_fn)` 描述输入与判定。
2. **驱动 agent**：`EvalHarness.run(agent_fn)` 把每个 prompt 喂给被测函数/技能，记录输出与判定。
3. **量化**：`summary()` 给出 total / passed / pass_rate。
4. **回归检测**：与 `regression.jsonl` 历史基线比对，通过率回退 >10 个百分点即标记 `regressed=True`。
5. **防退化**：回归告警触发复盘（接 reflection-replanner）定位退化根因。

## 脚本
`scripts/eval_harness.py`（纯标准库）：
- `TestCase` / `EvalHarness`：`add` / `run(agent_fn)` / `summary()` / 基线读写。
- CLI：`--selftest` 自检（含 agent 退化触发回归告警的场景）。

## 自验证
```bash
python scripts/eval_harness.py --selftest
```
断言：1/2 通过率=0.5 且首轮不报回归；agent 退化后 0/2 通过率=0 且基线 0.5 触发回归。

## 与四引擎闭环的关系
- 度量层：`summary().pass_rate` 可作为 super-agent 的「健康度」指标写入 memory-cross-engine。
- 触发层：回归告警 → reflection-replanner 重规划 → 修复后复测，形成"度量→反思→修复"小闭环。

## 已知限制
- 当前 agent_fn 为同步 callable，未内置异步/多轮对话驱动；复杂 agent 需在外层包一层适配。
- 判定以子串/函数为主，语义等价判定建议接 reason-verify 增强。

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