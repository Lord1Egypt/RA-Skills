---
name: game-negotiation
version: 1.0.0
description: |
  可计算博弈与协商引擎（model-agnostic）。针对多方谈判/分配场景，给出最优或纳什策略：
  Nash 议价、Rubinstein 轮流出价、Shapley 公平分配、零和 minimax 均衡。
  实体化"前沿认知·博弈谈判"，让 agent 能求可计算的最优/纳什策略而非拍脑袋。
agent_created: true
visibility: public
---

# game-negotiation（博弈谈判）

> 北极星能力域「前沿认知(下一梯队)·博弈谈判」实体化。一线大模型对博弈/协商
> 常给泛泛建议；本技能给出可计算、可验证的均衡解。

## 何时使用
- 多方资源/收益分配需要"公平且有理有据"的方案。
- 谈判中需知道"最优出价份额"或"对方最优反应"。
- 合作博弈要按贡献公平分润（Shapley）。
- 零和/对抗场景求 minimax 均衡值与混合策略。

## 工作流
1. **识别博弈型**：合作分配→Nash/Shapley；序贯谈判→Rubinstein；对抗→minimax。
2. **Nash 议价**：威胁点(disagree) + 可分配剩余(surplus) + 议价力权重(weights) → 闭式分配。
3. **Rubinstein**：双方贴现因子(p,r) → 子博弈完美均衡份额。
4. **Shapley**：特征函数(char_func) → 每玩家平均边际贡献。
5. **minimax**：收益矩阵 → 离散网格近似最大最小均衡值。
6. **可靠自验证**：`--selftest` 断言全部符合闭式/理论值，reliability<0.8 即回退。

## 运行
```bash
python scripts/negotiator.py --selftest
# Nash 等权分 100：--mode nash --json '{"disagree":[0,0],"surplus":100,"weights":[1,1]}'
# Rubinstein δ=0.9：--mode rubinstein --json '{"p":0.9,"r":0.9}'
```

## 增强点（融入元进化闭环）
- 自验证：selftest 含 Nash/Rubinstein/Shapley/minimax 理论基准。
- 自进化：已注入 learner，纳入 meta-evolver 的 sense/plan/record 闭环。

## 已知限制
- minimax 为离散网格近似，矩阵>2 维退化为等权（仅 2xN 精确）。
- Shapley 复杂度 2^n，玩家>~12 需采样近似。
- 假设理性/共同知识，非理性对手需加行为博弈层。
