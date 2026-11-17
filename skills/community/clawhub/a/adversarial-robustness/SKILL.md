---
name: adversarial-robustness
version: 1.0.0
description: |
  对抗鲁棒性：主动对文本决策系统施加字符/词级对抗扰动，量化并加固其抗欺骗能力。
  提供扰动生成(形近字/插空格/重复字符/同形 Unicode)、鲁棒性评分(1-翻转率)与
  "先评估后加固"的闭环，纯标准库可本地实跑，是"可靠地超越一线大模型"的防骗守门层。
agent_created: true
visibility: public
---

# adversarial-robustness（对抗鲁棒性）

> 北极星：超越一线大模型不仅要"会做"，更要"不会被骗/带偏"。本技能把对抗鲁棒性做成
> 可运行、可验证的工程模块，是 `metacognitive-monitoring` / `reason-verify` 之上的
> "抗欺骗守门层"。

## 何时使用
- 上线一个文本分类/审核/路由决策前，评估它对输入扰动的脆弱程度。
- 红队测试：用最小扰动尝试翻转模型决策，定位决策边界的脆弱点。
- 加固：侦测到翻转后，提示加"归一化/去噪"预处理提升鲁棒性。

## 核心机制
- **扰动生成器**（可叠加）：`char_swap`(形近/数字替换) / `insert_space`(插空格) / `dup_char`(重复字符) / `confusable`(同形 Unicode)。
- **鲁棒性评分**：对原文本生成 N 个扰动变体，跑决策函数 `predict`；
  `robustness = 1 − flip_rate`（flip = 变体决策≠原决策）。越接近 1 越稳。
- **脆弱点定位**：返回所有成功翻转的变体，指出"哪个字符被动一下就翻车"。
- 内置 demo 预测器用于自测；真实使用传入业务 `predict` 即可。

## 使用
```bash
python scripts/robustness.py --selftest
python scripts/robustness.py --text "please allow access" --predict-demo brittle --n 6
```

## 自进化学习系统
接入 skill-self-improve 的 learner.py：每次评估记录 flip_rate 与命中扰动类型，
积累后识别"最易致翻的扰动族"，反哺加固建议与默认扰动集。

## 已知限制
- 默认扰动为词法级（不依赖语义模型），对深层语义对抗（释义改写）覆盖有限。
- 归一化加固仅覆盖"可逆无歧义"的形近对（o→0/e→3/a→4/s→5/b→8/t→7/z→2）；i/l↔1 因歧义不纳入，仍可能致翻。
- 鲁棒性评分依赖 `predict` 的可复现性；随机扰动用固定种子保证可重跑。
- 不替代领域安全审核，仅做"输入抗扰动"的初筛与加固提示。

## 自进化学习系统（越用越好用、越用越高效）

本技能内置通用学习模块 `scripts/learner.py`。每次评估后自动复盘、积累经验。

### 记忆文件
`learned_patterns.json` 记录：操作总数、各扰动类型命中率、成功翻转记录、用户偏好、改进建议。

### 使用后请调用（Bash）

```bash
# 记录一次评估（--capability 填本次主扰动族，如「char_swap」「confusable」）
python scripts/learner.py record <本技能目录> --capability char_swap
# 记录一次成功翻转（说明某决策被攻破）
python scripts/learner.py record <本技能目录> --capability char_swap --fail --error 决策翻转 --note "allow->all0w 击穿"
# 记录用户偏好（下次直接采用）
python scripts/learner.py prefer <本技能目录> --key 加固策略 --val 归一化去形近
# 查看累计洞察（高频致翻扰动族 / 反复失败）
python scripts/learner.py insight <本技能目录>
# 自动复盘（错误≥3次 或 操作≥10次 时给出改进建议）
python scripts/learner.py reflect <本技能目录>
```

### 迭代规则
- **成功翻转累计 ≥3 次** → 主动扩展归一化映射或建议业务侧加预处理，并回写本 SKILL.md。
- **操作数 ≥10 次** → 分析高频致翻扰动族优先打磨检测，低频评估精简。
- **重要用户偏好** → 写入 `learned_patterns.json`，下次调用直接采用。

> 越用越懂你：第一次评估是通用探针，第十次已沉淀为你专属的"抗欺骗加固清单"。
