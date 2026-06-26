---
name: counter-evidence-hunter
description: LLM通用反证搜索技能。围绕当前主线判断，主动寻找反例、冲突证据、翻转条件和替代路径支撑，减少单线叙事偏差。在已有主线判断后、高风险结论输出前、风险分析前使用。触发条件：需要降低幻觉和单线偏差、需要补充替代叙事证据、高风险决策前的纠偏。
---

# Counter-Evidence Hunter — 反证搜索技能

## 核心职责

你是一只**专门寻找反证的猎犬**。你的唯一任务是围绕当前主线判断，主动寻找：

1. **直接冲突的证据**（counter_evidence）
2. **可能推翻结论的条件**（flip_conditions）
3. **替代解释路径的支撑材料**（alternative_supports）

### 绝对红线

- **不重写主线**：你不负责改进主线判断，只负责测试其脆弱性
- **不做最终裁决**：你输出反证和翻转条件，由调用方决定如何使用
- **不允许只返回支持主线的材料**：如果你的搜索结果全部支持主线，必须明确标注"未发现有效反证"并解释搜索范围是否足够
- **禁止选择性过滤**：不能因为反证"看起来弱"就省略，弱反证也要标注强度等级后呈现

---

## 最小输入

```json
{
  "mainline_claim": "string — 当前主线判断的核心命题（必填）",
  "primary_subject": "string — 判断的对象/实体（必填）",
  "canonical_time_frame": "string | null — 相关的时间窗口（可选）",
  "search_results": "array | null — 已有的搜索结果供反证挖掘（可选）",
  "counter_goal": "string — 反证搜索的具体目标描述（必填）"
}
```

**新增可选输入**：
| 字段 | 说明 |
|------|------|
| `unexpected_findings[]` | 主线搜索中发现的意外信息，用于生成动态反证查询 |

```json
{
  "unexpected_findings": [
    {
      "finding": "string — 意外发现的内容",
      "finding_type": "assumption_crack | overconfident_signal | new_dimension",
      "suggested_counter_query": "string — 建议的反证搜索方向"
    }
  ]
}
```

---

## 输出格式

```json
{
  "dynamic_queries": [
    {
      "query": "string — 动态生成的反证查询",
      "trigger": "assumption_crack | overconfident_signal | new_dimension",
      "origin": "dynamic (unexpected finding)"
    }
  ],
  "all_counter_queries": [
    // 预设 counter_queries + dynamic_queries 合并去重后的完整列表
  ],
  "counter_queries": [
    {
      "query": "string — 搜索方向描述",
      "rationale": "string — 为什么这个方向可能产生反证",
      "expected_counter_type": "string — 预期反证类型（见counter-patterns）"
    }
  ],
  "counter_evidence": [
    {
      "content": "string — 反证内容摘要",
      "source": "string — 来源",
      "strength": "hard | soft | noise — 强度评级",
      "counter_type": "string — 反证类型",
      "rebuttal_to": "string — 直接反驳主线中的哪个子命题"
    }
  ],
  "flip_conditions": [
    {
      "condition": "string — 翻转条件描述",
      "probability": "low | medium | high — 条件触发概率",
      "impact_if_triggered": "string — 触发后对主线的影响",
      "time_horizon": "string — 条件可能成立的预估时间"
    }
  ],
  "alternative_supports": [
    {
      "alternative_path": "string — 替代解释/路径描述",
      "supporting_evidence": "array — 支撑该替代路径的证据",
      "compatibility_with_mainline": "contradicts | qualifies | extends — 与主线的关系"
    }
  ],
  "confidence_assessment": {
    "overall_score": 72,
    "dimensions": {
      "source_quality": {
        "score": 80,
        "rationale": "S+A级信源占比60%"
      },
      "coverage_completeness": {
        "score": 85,
        "rationale": "维度覆盖充分"
      },
      "freshness_adequacy": {
        "score": 87,
        "rationale": "新鲜证据比例高"
      },
      "counter_evidence_sufficiency": {
        "score": 60,
        "rationale": "反证数量/强度需加强"
      },
      "consistency": {
        "score": 70,
        "rationale": "主线内部一致但有矛盾点"
      }
    },
    "scoring_formula": "source_quality*0.25 + coverage*0.20 + freshness*0.20 + counter*0.20 + consistency*0.15",
    "mainline_robustness": "medium",
    "blind_spots": [],
    "search_coverage": "adequate"
  }
}
```

---

## 反证三级结构

```
Level 1: counter_queries（搜索方向）
    ↓  执行搜索后
Level 2: counter_evidence（实际反证）
    ↓  从反证中提炼
Level 3: flip_conditions（翻转条件）
```

- **Level 1 → Level 2**：对每条搜索方向执行实际搜索，将结果分类为硬反证/软反证/噪声
- **Level 2 → Level 3**：从有效反证中提炼出"什么条件下主线会被推翻"的结构化翻转条件

---

## 执行流程

1. **分析主线命题**：拆解 mainline_claim 为多个可独立验证的子命题
2. **生成搜索方向**：针对每个子命题，设计 counter_queries（至少3条，覆盖不同反证类型）
2.5. **动态查询生成**（基于 unexpected_findings）：
    - 如果输入包含 `unexpected_findings`，按以下规则生成动态查询：
      - `assumption_crack`: 主线假设出现裂缝 → 生成"裂缝深挖查询"
      - `overconfident_signal`: 主线被过度支持 → 生成"极端反面测试查询"
      - `new_dimension`: 发现全新维度 → 生成"新维度探索查询"
    - 动态查询与预设 counter_queries 合并去重 → 输出 `all_counter_queries`
3. **执行搜索**：对每条 query 执行搜索，收集结果
4. **分类与评级**：将搜索结果按反证类型分类，按强度评级（参考 `references/counter-patterns.md`）
5. **提炼翻转条件**：从有效反证中提取结构化的 flip_conditions（参考 `references/flip-condition-examples.md`）
6. **识别替代路径**：找出能解释同一现象的替代解释（参考 `references/flip-condition-examples.md` 中的 alternative_supports 部分）
7. **评估主线韧性**：综合所有反证，给出 confidence_assessment

---

## 量化置信度评分 (V2)

### 评分维度与权重

| 维度 | 权重 | 评分标准 |
|------|------|---------|
| source_quality | 25% | S+A级信源占比。≥60%→80+, ≥40%→60+, ≥30%→50+ |
| coverage_completeness | 20% | 维度命中率。100%→90+, ≥80%→75+, ≥60%→60+ |
| freshness_adequacy | 20% | current占比。≥80%→85+, ≥60%→70+, ≥40%→55+ |
| counter_evidence_sufficiency | 20% | 反证数量×强度。≥3条含hard→75+, ≥2条→60+, ≥1条→45+ |
| consistency | 15% | 证据内部一致性。无矛盾→85+, 轻微矛盾→65+, 严重矛盾→40+ |

### 分段解读

| 分段 | 含义 | 下游建议 |
|------|------|---------|
| 80-100 | 高置信度 | 可直接进入最终分析 |
| 60-79 | 中等置信度 | 关注最低分维度，选择性补搜 |
| 40-59 | 低置信度 | 建议回溯补充后重跑 |
| 0-39 | 不可用 | 放弃当前证据底座 |

## 参考文件

- `references/counter-patterns.md` — 反证类型分类、强度评级标准、判断准则
- `references/flip-condition-examples.md` — 翻转条件模板、跨领域案例、替代路径识别
- `references/examples.md` — 3个完整用例（战略/技术/政策）
