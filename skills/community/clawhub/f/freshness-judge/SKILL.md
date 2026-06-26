---
name: freshness-judge
description: LLM通用证据新鲜度判断技能。根据时间窗和证据时间信息，判断每条证据属于current/background/stale/undated/malformed哪一类。在搜索结果标准化之后、需要区分当前证据与背景证据时使用。触发条件：现实问题/新闻/政策/市场分析、需要降低"把旧材料当新材料"风险、时间敏感型任务。
---

# Freshness Judge — 证据新鲜度判断技能

## 核心职责

根据时间窗（time window）和证据中的时间信息，为每条证据打上精确的时间语义标签。

**做什么：**
- 提取证据中的时间信息（发布日期、事件时间、数据时间范围等）
- 将每条证据分类到 5 个新鲜度等级之一
- 生成整体新鲜度画像（freshness profile），供下游流程使用

**不做什么：**
- ❌ 不改写证据内容
- ❌ 不做搜索或补充信息
- ❌ 不生成最终判断或结论
- ❌ 不做证据清洗（交给 evidence-cleaner）
- ❌ 不移除任何证据（即使标记为 stale，仍保留在分类结果中）

## 最小输入

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `normalized_evidence[]` | array | ✅ | 已标准化证据条目，每条应含 `source_url`、`title`、`snippet`、`publish_date`（可选） |
| `canonical_time_frame` | object | ✅ | `{start, end, granularity}` 本次任务的标准时间框架 |
| `freshness_policy` | object | ❌ | 覆盖默认行为的策略参数（见下文） |

### freshness_policy 参数

```json
{
  "conservatism_level": "high",
  "stale_threshold_months": 6,
  "undated_handling": "downrank",
  "cross_window_rule": "background",
  "require_precise_date": false
}
```

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `conservatism_level` | `"high"` | 保守程度：`high`（不轻易标记为current）/ `standard` / `lenient` |
| `stale_threshold_months` | 视场景 | stale 阈值月数，默认由场景决定 |
| `undated_handling` | `"downrank"` | 无日期证据处理：`downrank` / `flag_only` / `drop` |
| `cross_window_rule` | `"background"` | 跨时间窗证据规则：`background` / `stale` |
| `require_precise_date` | `false` | 是否要求精确日期（否则接受月份/年份级精度） |

## 输出格式

```json
{
  "current_evidence": [],
  "background_evidence": [],
  "stale_evidence": [],
  "undated_evidence": [],
  "malformed_evidence": [],
  "freshness_profile": {
    "total_evidence": 20,
    "current_ratio": 0.35,
    "background_ratio": 0.30,
    "stale_ratio": 0.15,
    "undated_ratio": 0.15,
    "malformed_ratio": 0.05,
    "time_coverage": {
      "earliest": "2022-03-15",
      "latest": "2024-05-15",
      "median_date": "2024-01-20"
    },
    "overall_assessment": "证据库时间覆盖良好，35%为当前有效证据，15%为无日期证据需谨慎使用",
    "risk_flags": [
      "15%证据无时间标注，可能引入旧材料误判风险"
    ],
    "compensation_queries": [
      {
        "query": "AI芯片 2025年Q3 Q4 市场格局变化",
        "rationale": "补充2025年H2背景数据，平衡时间分布偏差",
        "target_period": "2025-07 至 2025-12",
        "priority": "recommended"
      }
    ]
  }
}
```

## 5 级分类体系

| 等级 | 标签 | 含义 | 下游处理建议 |
|------|------|------|-------------|
| 1 | **current** | 在 canonical time frame 内，可直接使用 | 优先使用，作为主证据 |
| 2 | **background** | 时间框架外，但有参考价值 | 辅助证据，需标注"背景信息" |
| 3 | **stale** | 明显过时、已被推翻或替代 | 谨慎使用或忽略，需标注"已过时" |
| 4 | **undated** | 缺乏时间信息，无法判断 | 建议降权，避免当作 current 使用 |
| 5 | **malformed** | 时间格式损坏或自相矛盾 | 建议忽略，需人工审查 |

## 核心原则：保守原则

1. **不默认当 current**：在保守模式下，只有明确落在时间窗内的证据才标记为 current
2. **时间不足标记 undated**：无法从证据中提取时间信息时，不猜测，标记为 undated
3. **格式损坏标记 malformed**：时间信息存在但自相矛盾或格式无法解析时，标记为 malformed
4. **宁可错标 background，不可错标 current**：对时间边界模糊的证据，降级处理

## 判定流程

```
证据进入新鲜度判断
        │
        ▼
┌─────────────────────────┐
│ 提取时间信息              │
│ publish_date?            │
│ snippet中的日期?          │
│ 事件隐含时间?             │
└────┬──────┬──────┬──────┘
     │      │      │
   有时间  无时间  时间矛盾
     │      │      │
     ▼      ▼      ▼
  继续    [UNDATED] [MALFORMED]
     │
     ▼
┌─────────────────────────┐
│ 比对 canonical_time_frame │
│ evidence_date vs window   │
└────┬──────┬──────┬──────┘
     │      │      │
   在窗内   窗外近期  窗外久远
     │      │      │
     ▼      ▼      ▼
  [CURRENT] [BACKGROUND] 判断是否被推翻
                         │
                    ┌────┴────┐
                    │         │
                  未推翻     已推翻/替代
                    │         │
                    ▼         ▼
               [BACKGROUND] [STALE]
```

## 时间偏差自动补偿

当 freshness_profile 检测到时间分布异常时，自动生成 `compensation_queries` 供编排器决定是否触发补搜。

### 触发条件

| 条件 | 补偿级别 | 说明 |
|------|---------|------|
| `current_ratio > 0.8` 且时间跨度 < 时间窗50% | `recommended` | 证据过度集中在近期，建议补充历史背景 |
| 某维度证据全部为 stale/undated | `required` | 关键维度无新鲜证据，必须补充 |
| `background_ratio = 0` 且 `goal_mode = strategic` | `recommended` | 战略分析缺乏背景深度 |
| `undated_ratio > 0.3` | `required` | 大量无日期证据，必须尝试补充日期信息 |

### 补偿查询格式

```json
{
  "compensation_queries": [
    {
      "query": "string — 补充搜索查询",
      "rationale": "string — 为什么需要这条补充",
      "target_period": "string — 目标补充时间段",
      "priority": "required | recommended | optional"
    }
  ]
}
```

### 与编排器的协作

- `required` 级补偿：编排器应自动触发回溯到 query-planner 追加查询
- `recommended` 级补偿：编排器可根据预算决定是否补搜
- `optional` 级补偿：仅在预算充裕时执行

## 参考文档

- [新鲜度判定规则](references/freshness-rules.md) — 5 级分类详细定义与判定标准
- [时间窗场景示例](references/time-window-examples.md) — 不同场景的典型时间窗与边界案例
- [判定用例集](references/examples.md) — 3 个完整用例演示

## 与 evidence-cleaner 的协作

```
raw_evidence_items
      │
      ▼
 evidence-cleaner (清洗)
      │
      ▼
normalized_evidence  ──→  freshness-judge (本技能)
      │
      ▼
timestamped_evidence (带新鲜度标签)
```

**建议执行顺序**：先执行 evidence-cleaner 完成去噪去重，再执行 freshness-judge 判断新鲜度。避免在噪声证据上浪费时间判定。
