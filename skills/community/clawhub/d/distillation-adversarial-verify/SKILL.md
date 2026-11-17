---
name: distillation-adversarial-verify
version: 1.0.0
description: |
  跨模型蒸馏工程化的对抗验证环：对蒸馏出的关键决策规则 / 学生技能做反例测试，量化"学到了真能力
  还是只学到表面话术"。给定一组规则(可调用函数或规则 dict)与对抗用例集，输出每条规则的健壮性
  评分与整体蒸馏质量分，并标记需回炉的规则。纯标准库、零依赖、可本地实跑(--selftest 自带样例)。
agent_created: true
visibility: public
---

# distillation-adversarial-verify（蒸馏质量对抗验证）

> 跨模型蒸馏工程化与可信代理域的核心子能力之一。意图：蒸馏不是"读一遍教师就完事"——
> 必须用能戳穿幻觉的反例，验证蒸馏出的决策规则真的成立，否则学生只是话术复读机。

## 何时用
- 蒸馏出 `meta-*` 学生技能后，验证其继承的决策规则在对抗用例上是否仍成立。
- 给 `cross-model-knowledge-extraction` 抽出的 decision_rules 做健壮性体检。
- 任何"声称学会了某条规则"的自动化，上线前先跑对抗验证。

## 核心概念
- **规则(rule)**：一个可调用 `rule(input) -> bool/输出` 的对象，或 `(判定函数, 描述)` 元组。
- **对抗用例(case)**：`(input, 期望通过/失败)`。期望"通过"的用例若被规则拒，算翻转(flip)；期望"失败"的用例若被放行，也算翻转。翻转即暴露脆弱点。
- **健壮分(robustness)** = 1 - 翻转数 / 总用例数，区间 [0,1]。
- **蒸馏质量分(quality)** = 各规则健壮分的加权平均（权重按规则重要度）。

## 用法
```bash
# 对某个学生技能跑对抗验证（规则与用例在技能内定义或外部传入）
python scripts/adversarial_verify.py <学生技能目录> [--cases cases.json]

# 自带样例自检
python scripts/adversarial_verify.py --selftest
```

## 输出
```json
{
  "rules": [{"name": "规则A", "robustness": 1.0, "flips": 0}, ...],
  "overall_quality": 0.9,
  "verdict": "PASS | NEEDS_REWORK",
  "weak_rules": ["规则B"]
}
```
`verdict=NEEDS_REWORK` 的规则需回炉重蒸馏（回到 model-distillation 重写签名）。

## 与其他蒸馏子能力的关系
- ← `cross-model-knowledge-extraction`：抽出的 decision_rules 是这里要验的靶子。
- → `model-distillation`：验证不过的规则触发重蒸馏。
- ← `teacher-capability-probe`：探针的失败模式可直接转成对抗用例。

## 已知限制
- 健壮性完全取决于对抗用例质量；用例覆盖不到的边界，验证分仍会虚高（建议结合 teacher-capability-probe 自动扩用例）。
- 仅验证"决策规则"层面，不验证教师隐式知识的完整性。

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
