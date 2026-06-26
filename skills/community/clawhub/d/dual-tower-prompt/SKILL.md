---
name: dual-tower-prompt
version: v1.0.0
description: 双塔足球预测 Prompt — 仅需比赛特征文本(fet_txt), 一次 LLM 调用完成基本面+市场双塔分析+融合决策, 输出 ranking_score 排名和 Top-K 推荐
disable-model-invocation: false
---

# 双塔足球预测 Prompt

## 简介

本技能提供双塔足球预测的提示词框架。**仅依赖比赛特征文本（fet_txt）**，无需 API 访问，一次 LLM 调用即完成塔A基本面分析、塔B市场分析和融合决策。

## 架构

```
fet_txt (比赛特征文本)
    │
    ├─→ 阶段一: 塔A基本面分析 (10条规则 + 价值分估算)
    │     → fundamental_score + recommended_side + value_scores
    │
    ├─→ 阶段二: 塔B市场分析 (赔率变动/热度/异常信号)
    │     → market_score + recommended_side
    │
    └─→ 阶段三: 融合决策 (方向裁决 + 置信度 + 排名分)
          → ranking_score + final recommended_side
```

## 使用方式

1. 通过 `lota-football` 技能获取单场比赛的 `fet_txt`
2. 读取 `prompt.md`，将末尾的 `{fet_txt}` 替换为实际特征文本
3. 发送完整提示词给 LLM
4. 解析返回的 JSON，获取 `fusion.ranking_score` 用于跨比赛排序

## 批量预测

对多场比赛逐场调用后，按 `fusion.ranking_score` 降序排列，Top-K 即为推荐。

## 关键输出字段

| 字段 | 含义 | 范围 |
|------|------|------|
| `fusion.ranking_score` | 排名分（越高越值得关注） | 0+ |
| `fusion.combined_score` | 综合信号强度 | 0-1 |
| `fusion.confidence` | 置信度 | 0-1 |
| `fusion.recommended_side` | 推荐方向 | home/away/draw |
| `fusion.agreement` | 双塔一致/分歧 | both_agree / a_only / b_only / ... |
| `tower_a.fundamental_score` | 基本面价值信号强度 | 0-1 |
| `tower_b.market_score` | 市场异常信号强度 | 0-1 |

## 技术背景

- **双塔架构**: 塔A(Poisson/ELO公允概率+定性) + 塔B(赔率变动/离散/亚盘/必发+定性) → Stage2融合
- **排名公式**: `ranking_score = combined × (1 + max(0, value_score) / 8.0)`
- **方向裁决**: 双塔一致→共识加成; 分歧→高分主导或Claude接管
- **回测验证**: 2416场6个月数据, 3阶段时间切分迭代, 跨期迁移CLV -1.52→+0.24→+0.93
- **仅依赖**: fet_txt (无API密钥, 无网络请求)
