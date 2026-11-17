---
name: cross-model-knowledge-extraction
version: 1.0.0
description: |
  跨模型蒸馏工程化的第一环：从 WorkBuddy 内部教师技能的 SKILL.md（或任意技能正文）
  中结构化提取能力签名——工作流步骤、触发场景、已知限制/坑、工具脚本、以及可被
  蒸馏的决策规则（if/when-then/必须）。输出 JSON 能力画像，直接喂给 model-distillation
  的签名合成与对抗验证。纯标准库、零依赖、可本地实跑（--selftest 自带样例）。
agent_created: true
visibility: public
---

# cross-model-knowledge-extraction（跨模型知识提取）

> 跨模型蒸馏工程化与可信代理域的核心子能力之一。意图：把教师技能里"散落的能力"
> 抽成结构化签名，让蒸馏从"读一整篇 SKILL.md 凭感觉"变成"对照签名做程序化合成"。

## 何时用
- 跨模型蒸馏前，先对教师做能力结构化（替代人工通读整篇 SKILL.md）。
- 批量盘点生态技能的"真实能力边界"，支撑教师能力探针（teacher-capability-probe）与蒸馏质量对抗验证。
- 任何需要"把一段专家知识变成机器可消费的结构"的场景。

## 提取维度（能力签名 schema）
1. **workflow_steps**：编号列表里的显性步骤（正则 `^\s*\d+\.\s+(.+)$`）。
2. **headings**：标题层级（`#`~`####`）——能力轮廓。
3. **triggers**：触发/使用场景行（含 触发/trigger/when/使用场景/使用时机 关键词）。
4. **limits**：已知限制/坑/失败模式（限制/注意/坑/风险/失败模式 段）。
5. **scripts**：scripts/ 下脚本清单（可复用的工具）。
6. **decision_rules**：可蒸馏的决策规则——含 若/如果/当...时/则/必须/should/must/if...then 的句子，蒸馏时最该"继承+对抗验证"的部分。

## 用法
```bash
# 对某个教师技能提取签名
python scripts/extract_signature.py <教师技能目录>

# 自带样例自检（无需外部依赖）
python scripts/extract_signature.py --selftest
```

输出 JSON：
```json
{
  "name": "teacher-skill",
  "workflow_steps": ["步骤1", "步骤2"],
  "headings": ["概述", "用法"],
  "triggers": ["触发：用户要求做 X 时"],
  "limits": ["注意：Y 场景会失败"],
  "scripts": ["do.py"],
  "decision_rules": ["若输入为空则直接返回"],
  "body_size": 1234
}
```

## 与其他蒸馏子能力的关系
- ← `teacher-capability-probe`：探针量化边界后，本技能把边界落成结构化签名。
- → `model-distillation`：签名直接进 synthesize_student 的工作流/限制/工具字段。
- → `distillation-adversarial-verify`：decision_rules 是下一步对抗验证的靶子。

## 已知限制
- 仅基于文本正则抽取，无法理解隐式知识；对教师"未写出来的经验"覆盖不到，需用探针+对抗验证补强。
- decision_rules 是启发式命中，可能漏掉非标准表述的规则；首用请对照原 SKILL.md 核验。

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
