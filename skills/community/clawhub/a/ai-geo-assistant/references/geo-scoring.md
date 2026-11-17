# GEO Score 评分模型（geo-scoring）

`scripts/geo_audit.py` 的 `analyze_html()` 输出 0–100 的 **GEO Score** 与 **十维度分**（满分合计 100）。评分采用**扣分制**（每维从满分起扣，扣满为止）+ **Grade 等级** + **AI 可见度** + **GEO 六维评分**。

## 十维度配置（满分 100）

| 维度 key | 维度名 | 满分 | 维度 key | 维度名 | 满分 |
| --- | --- | --- | --- | --- | --- |
| `crawlability` | 可抓取性 | 12 | `entity` | 实体清晰度 | 10 |
| `metadata` | 元数据/结构化 | 12 | `discoverability` | 站内可发现性 | 8 |
| `readability` | 机器可读性 | 12 | `answerability` | 可回答性 | 12 |
| `trust` | 信任信号 | 8 | `citation` | 可引用性 | 8 |
| `freshness` | 内容新鲜度 | 8 | `content` | 内容质量 | 10 |

**维度扣分规则**：每个维度从 `maxScore` 起算，命中该维度的规则按其 `scoreImpact`（P1/P2 不同权重）扣分，扣分上限为 `maxScore`，最终 `score = max(0, maxScore − Σimpact)`。

## Grade 等级

| 分数 | 等级 | 含义 |
| --- | --- | --- |
| ≥ 85 | A | 生成式引擎友好，易被识别/引用/复述 |
| 70–84 | B | 基本达标，少数维度待补 |
| 55–69 | C | 中等，结构化/可信度常为短板 |
| 40–54 | D | 偏弱，需系统补齐实体/结构化/内容 |
| < 40 | F | 严重不足 |

## AI 可见度（AI Visibility）

由 `discoverability`、`citation`、`answerability` 三维度**百分制均值**合成：

- `score = round((discoverability% + citation% + answerability%) / 3)`
- 等级：`≥85` high / `≥60` medium / 其余 low
- 文案：`high`=“AI 可见度较强…”；`medium`=“AI 可见度中等…”；`low`=“AI 可见度偏弱…”

## GEO 六维评分（geo_score_block）

把十维聚合为更直观的六块（满分均为 100）：

| key | 标签 | 来源维度（均值） |
| --- | --- | --- |
| `content` | 内容结构 | `content` + `readability` |
| `metadata` | 结构化数据 | `metadata` |
| `ai_visibility` | AI 可见度 | `discoverability` + `citation` |
| `freshness` | 内容新鲜度 | `freshness` |
| `brand_consistency` | 品牌一致性 | `entity` + `trust` |
| `answerability` | 问答覆盖度 | `answerability` |

## 报告结构（analyze 输出）

```
geo_score:
  geo_score: 0-100
  grade: A/B/C/D/F
  max_score: 100
  dimensions: [ {key,label,label_cn,score,maxScore,percentScore,issueCount,status} ×10 ]
  dimension_scores: { key: score ×10 }
  weights: { key: maxScore ×10 }
  ai_visibility: { score, level, summary, signals:[...] }
  geo_score_block: { title, dimensions:[ {key,label,score} ×6 ] }
suggestions: [ {dimension,impact(high/medium),ruleKey,issue,recommendation,fix,estimatedGain} ]
```

## 复检对比

`validate --baseline A.json --current B.json` 对比两份 `geo_score`：

- `delta.geo_score`：总分差值。
- `delta.dimensions`：十维度各自差值。
- `baseline/current_suggestions`、`resolved`：建议条数变化与已解决数。
- `verdict`：improved / unchanged / regressed。

> 注意：分数提升依赖**真实内容补齐**，而非仅追加空 schema。若只注入占位 JSON-LD，维度分可能虚高但生成式引擎不会真正引用——Agent 须确保 `optimize` 产出的占位内容被真实数据填充。
