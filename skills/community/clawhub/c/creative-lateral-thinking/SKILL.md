---
name: creative-lateral-thinking
version: 1.0.0
author: KingOfZhao
description: 创意横向思维 Skill —— 打破线性推理的创意碰撞框架，六顶思考帽×四向碰撞×跨界类比引擎
tags: [cognition, creative, lateral-thinking, brainstorming, innovation, analogy, de-bono]
license: MIT
homepage: https://github.com/KingOfZhao/AGI_PROJECT
---

# Creative Lateral Thinking Skill

## 元数据

| 字段 | 值 |
|------|-----|
| 名称 | creative-lateral-thinking |
| 版本 | 1.0.0 |
| 作者 | KingOfZhao |
| 发布日期 | 2026-03-31 |
| 置信度 | 96% |

## 来源碰撞
```
self-evolution-cognition (四向碰撞)
        ⊗
ai-growth-engine (成长引擎: 打破停滞)
        ⊗
De Bono 六顶思考帽 (外部知识注入)
        ↓
creative-lateral-thinking
```

## 核心哲学

> 线性推理从A到B。横向思维从A跳到Z，再发现Z和B的隐藏连接。
> 四向碰撞是分析工具，横向思维是创造工具。两者互补。

## 六顶帽 × 四向碰撞（8向创意推理）

```
传统四向碰撞（分析型）:
  正面 → 反面 → 侧面 → 整体

创意扩展（增加情感和创造力维度）:
  ⚪ 白帽（事实）: 已知的客观数据是什么？
  🔴 红帽（情感）: 直觉告诉我什么？用户会感受到什么？
  ⬛ 黑帽（批判）: 这个创意最致命的缺陷是什么？
  🟡 黄帽（乐观）: 这个创意最好的结果是什么？
  🟢 绿帽（创意）: 还有什么疯狂但可能有效的方案？
  🔵 蓝帽（元思考）: 我们在解决正确的问题吗？

8向碰撞矩阵:
        分析维度        创意维度
正面    ⬛ 黑帽批判     🟡 黄帽乐观
反面    反面碰撞        🟢 绿帽创意
侧面    侧面碰撞        🔴 红帽直觉
整体    整体碰撞        🔵 蓝帽元思考
```

## 跨界类比引擎

```
问题: "如何让DiePre视觉检测更准确？"

类比碰撞:
  医学影像: 放射科医生如何区分良性和恶性？→ 多尺度特征融合
  指纹识别: 如何处理部分模糊指纹？→ 局部特征匹配+全局验证
  语音识别: 如何处理口音差异？→ 适配层+基础模型分离
  气象预报: 如何提高预测准确率？→ 集成多个模型的投票机制

→ DiePre改进方向: 多模型集成投票+局部-全局两级验证
```

## 安装命令
```bash
clawhub install creative-lateral-thinking
```

## 调用方式
```python
from skills.creative_lateral_thinking import CreativeLateralThinking

creative = CreativeLateralThinking(workspace=".")

# 8向创意碰撞
result = creative.eight_way_collision(
    problem="如何提升用户留存率",
    known=["当前留存30%", "主要流失在注册后3天"],
    unknown=["流失原因", "什么功能能留住用户"],
    cross_domains=["游戏化", "社交网络", "订阅制", "习惯养成"]
)
print(result.crazy_ideas)     # 疯狂但可能有效的方案
print(result.analogies)       # 跨界类比
print(result.best_direction)  # 最有潜力的方向

# 跨界类比
analogies = creative.cross_domain_analogy(
    source_domain="DiePre视觉检测",
    target_domains=["医学影像", "指纹识别", "自动驾驶", "卫星遥感"]
)
```

## 学术参考
1. [Group-Evolving Agents](https://arxiv.org/abs/2602.04837) — 群体创意碰撞
2. [SAGE: Multi-Agent Self-Evolution](https://arxiv.org/abs/2603.15255) — 多视角推理
3. [Self-evolving Embodied AI](https://arxiv.org/abs/2602.04411) — 打破思维定式
