---
name: emergent-collective-intelligence
description: 涌现集体智能编排——编排一个多样化 agent 群体（偏置/策略各异），通过相互纠错加多样性加权稳健聚合，涌现出超越任一个体的集体解（群体智慧的可验证工程化）。内置涌现判定：当集体误差小于最好单体误差即量化确认群体超越个体。适用于多专家估计融合、集成决策、降低单模型系统性偏置与盲区、稳健预测等场景。
metadata:
  agent_created: true
  version: 1.0.0
  domain: 涌现超智能与自主科学发现(元之三阶)
  capability: 涌现集体智能编排
---

# emergent-collective-intelligence · 涌现集体智能编排

> 元之三阶能力：单个大模型 = 单一先验 + 单点盲区。本技能把**多样化群体的独立判断**
> 聚合成超越任一个体的集体智能，并给出"是否真的涌现"的可测证据——这是从"更强的单体"
> 走向"群体超越单体"的关键一跃。

## 何时使用
- 多个专家/模型/策略对同一问题各有估计，想融合出比任何单个都更准的结论。
- 想主动消除单模型的系统性偏置与盲区（多样性抵消误差）。
- 需要稳健预测：对离群/异常成员自动抑制。

## 核心机制（群体智慧的可验证工程化）
1. **多样性 Diversity**：成员偏置各异且独立 → 误差方向相消（Diversity Prediction Theorem）。
2. **相互纠错 Peer-correction**：每轮把估计朝群体共识拉近，降方差、不移无偏共识。
3. **稳健聚合 Aggregation**：去极值 + 多样性/逆偏离加权，抑制离群、放大共识。
4. **涌现判定 Emergence**：`集体误差 < 最好单体误差` → 量化确认涌现（可反例证伪）。

## 用法
```bash
python scripts/collective.py --selftest   # 5 场景：涌现/胜平均/抑离群/降方差/无多样性不涌现
python scripts/collective.py --demo
```

编程调用：
```python
from collective import Agent, collective_solve
agents = [Agent("optimist", +12), Agent("pessimist", -11), Agent("hawk", +15),
          Agent("dove", -13), Agent("outlier", +40)]
r = collective_solve(agents, signal=100.0, truth=100.0)
# r['collective'], r['emergent'](集体是否优于最好单体), r['collective_error'] ...
```

## 边界
- 涌现依赖**多样性**：同质群体（同偏置）不会涌现（selftest 场景[5]验证），需保证成员策略/偏置独立多样。
- 当前聚合面向数值估计；分类/序列结论可扩展为多数投票 + 置信加权。

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
