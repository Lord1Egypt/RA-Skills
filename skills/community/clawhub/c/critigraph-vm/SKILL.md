---
name: critigraph-vm
description: 对抗式推理虚拟机 — 纯数学 MCTS 博弈树搜索。不是给答案，是找出所有反驳你的路径，然后告诉你哪条路能赢。
version: 0.2.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
    homepage: https://github.com/lybang972314/critigraph-vm
    emoji: ⚔️
---

# CritiGraph VM ⚔️

**不是回答问题。是找出所有反驳你的路径，然后告诉你哪条路能赢。**

一个领域无关的对抗式推理虚拟机。它不读你的文本，不懂你的领域，不调任何 LLM。

## 只做三件事

1. **推理** — 纯数学 MCTS 树搜索，探索所有可能路径
2. **对抗** — 非对称多智能体博弈，自动生成反方视角
3. **决策** — 输出最优路径 + 期望胜率 + 完整搜索树

## 核心引擎

```
V = 1 / (1 + e^(-k * (X - θ))) * (1 - Ω)
```

这就是全部。没有 prompt，没有 embedding，没有 API 调用。三个参数：状态标量 X、非对称阈值 θ、刚性约束 Ω。

## 为什么不是又一个 LLM 包装器

```
LLM:      "这个证据应该有效"          → 一个回答
CoT:      "因为A所以B所以C"           → 一条思路  
CritiGraph:                            → 一棵树
                    ROOT
                   /    \
             提交证据    质证
             /      \
          通过     非法证据排除(Ω=1→剪枝)
```

LLM 告诉你答案。CritiGraph 告诉你**对手会怎么反驳，以及你被反驳后赢的几率还剩多少。**

## 竞品全景

| | 推理 | 对抗 | 决策 | 领域无关 | 纯数学 | 开源 |
|------|:---:|:---:|:---:|:---:|:---:|:---:|
| ChatGPT/Claude | ✅链 | ❌ | ❌ | ✅ | ❌ | ❌ |
| o1/o3 | ✅深链 | ❌ | ⚠️ | ✅ | ❌ | ❌ |
| AlphaGo/MuZero | ✅树 | ✅游戏 | ✅游戏 | ❌ | ✅ | ❌ |
| **CritiGraph** | **✅树** | **✅通用** | **✅排名** | **✅** | **✅** | **✅MIT** |

## 任何领域，~20行适配器

```python
# ⚖️ 法律
class EvidenceAdapter(BaseAdapter):
    def generate_ops(self, X, agent_id):
        if agent_id == 0: return [(min(1.0, X+0.15), 1, "提交证据", False, False)]
        return [(max(0.0, X-0.20), 0, "质证", False, False)]

# 📊 量化
class SignalAdapter(BaseAdapter):
    def generate_ops(self, X, agent_id):
        if agent_id == 0: return [(min(1.0, X+0.10), 1, "加仓", False, False)]
        return [(max(0.0, X-0.15), 0, "止损", False, False)]
```

## v0.2 新增：数据训练引擎

数据越多 → 参数越精确 → 推理越强。不是黑盒，每个参数都有物理含义。50-500 条标注案例即可训练。

## 生产验证

- ✅ 50 基准测试全通过
- ✅ Hermes 多 Agent 系统运行
- ✅ 4 领域适配器（法律/量化/代码审查/安全审计）

---

**[GitHub](https://github.com/lybang972314/critigraph-vm)** · MIT License · **Enterprise → [Contact](https://github.com/lybang972314)**
