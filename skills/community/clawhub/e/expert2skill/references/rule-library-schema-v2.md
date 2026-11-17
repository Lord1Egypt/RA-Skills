# rule_library Schema v2 设计（泛化稿）

> 状态：设计稿。v1 为股票样例（value-investor.rules.json，固定阈值 + 无对象画像）。
> 触发：营养师样例验证暴露三个 v1 装不下的缺口。
> 目标：让 schema 从"股票专用"走向"通用专家方法"。

---

## v1 缺口 → v2 能力映射

| # | v1 缺口（营养师样例暴露） | v2 新增能力 | 状态 |
|---|--------------------------|------------|------|
| ① | 判定阈值无法引用对象属性（"蛋白质 g/kg 体重"） | `judge.threshold` 增加 `per`/`reference` 相对阈值 | 本稿设计 |
| ② | 无对象画像采集层（评估前需知道体重/年龄/性别/活动量） | 顶层新增 `subject_profile` | 本稿设计 |
| ③ | 权重固定，无法随对象条件变化（肾病→蛋白质项权重升高） | item 增加 `weight_conditions` 条件权重 | 本稿设计 |

---

## v2 完整结构

```json
{
  "rule_library": {
    "id": "...",
    "version": "0.2.0",
    "library_type": "expert",
    "title": "...",
    "author": "...",
    "authority": "...",
    "scoring": { ... },
    "question_types_supported": ["binary", "scale", "numeric", "text", "conditional", "self_check", "multi_select"],

    "subject_profile": {
      "description": "评估前需采集的对象属性（决定判定基准）",
      "fields": [
        {
          "key": "体重",
          "type": "numeric",
          "unit": "kg",
          "required": true,
          "question": "评估对象当前体重是多少？"
        },
        {
          "key": "年龄",
          "type": "numeric",
          "unit": "岁",
          "required": true,
          "question": "评估对象年龄？"
        },
        {
          "key": "活动量",
          "type": "scale",
          "options": { "1": "久坐", "2": "轻度", "3": "中度", "4": "高强度" },
          "required": false,
          "question": "评估对象的日常活动量？"
        },
        {
          "key": "疾病史",
          "type": "multi_select",
          "options": ["无", "肾病", "糖尿病", "高血压", "其他慢性病"],
          "required": false,
          "question": "是否有以下疾病史？"
        }
      ]
    }
  },

  "categories": [
    {
      "id": "A",
      "name": "...",
      "weight": 1.0,
      "items": [
        {
          "id": "b1",
          "name": "...",
          "question": "...",
          "type": "numeric",
          "pass_condition": "蛋白质摄入 >= 1.2 g/kg体重",
          "partial_condition": "1.0 <= 摄入 < 1.2 g/kg体重",
          "fail_condition": "摄入 < 1.0 g/kg体重",
          "score_if_pass": 1.0,
          "score_if_fail": 0.0,
          "weight": 1.5,

          "weight_conditions": [
            { "when": "profile.疾病史 contains '肾病'", "weight": 2.5, "note": "肾病患者蛋白质管理是关键" },
            { "when": "profile.活动量 in ['3','4']", "weight": 2.0, "note": "高活动量者蛋白质需求高" }
          ],

          "severity": "high",
          "applies_when": null,
          "evidence_required": true,
          "judge": {
            "mode": "threshold",
            "field": "蛋白质摄入",
            "unit": "g/kg体重",
            "reference": "subject_profile.体重",
            "computation": "actual = 蛋白质摄入(g) / profile.体重(kg)",
            "pass": { "gte": 1.2 },
            "partial": { "gte": 1.0 },
            "fail": { "lt": 1.0 }
          }
        }
      ]
    }
  ]
}
```

---

## 三个新增能力的语义

### ① 相对阈值 `judge.reference`

- `judge.reference`: 引用 `subject_profile` 里的一个属性（如 `"subject_profile.体重"`）。
- `judge.computation`: 说明实际值如何计算（skill 端执行，如 `蛋白质摄入(g) / 体重(kg)`）。
- `judge.pass/partial/fail`: 仍是固定数值区间，但**比较的是计算后的实际值**。
- skill 端执行步骤：
  1. 先采集 `subject_profile` 字段
  2. 按 `computation` 计算实际值
  3. 与 pass/partial/fail 比较 → passed/partial/fail
  4. 提交 evaluate（引擎只看到 passed 结果，零改动）

> 兼容性：`reference` 缺省时行为与 v1 完全一致（固定阈值直接比较），旧样例不受影响。

### ② 对象画像 `subject_profile`

- 顶层字段，定义"评估前需要采集的对象属性"。
- 每个 field 有 `key/type/unit/required/question`。
- skill 端在正式提问前先采集画像，并缓存到上下文供所有 `judge.reference` 和 `weight_conditions` 引用。
- 无画像需求的方法（如股票样例）可省略该字段 → 向后兼容。

### ③ 条件权重 `weight_conditions`

- item 的 `weight` 是默认权重；`weight_conditions` 是可选列表，按 `when` 表达式命中时覆盖权重。
- `when` 表达式引用 profile 或前序 item 结果：
  - `"profile.疾病史 contains '肾病'"`
  - `"profile.活动量 in ['3','4']"`
  - `"b3_result == 'fail'"`
- 多条命中时取**最高权重**（避免叠加歧义）。
- skill 端在汇总评分前解析并替换 item 的 weight。

---

## 对 evaluate 引擎的影响

**零改动。** 所有 v2 能力在 skill 端翻译完毕，evaluate 仍只接收 `items[] + passed`。这保持了与现有 20+ 合规 skill 的引擎完全兼容。

---

## 未决问题（待确认）

1. **profile 是否参与评分**：对象画像本身是否算"评估对象"的一部分？还是纯判定基准？当前设计：**纯判定基准，不参与评分**（体重 90kg 不代表营养好或差）。若未来需要"对象属性也是评估维度"，再升级。
2. **`when` 表达式语法**：当前用自然语言式（`contains` / `in`）。建议收敛为固定模式集（`==` / `!=` / `>` / `<` / `contains` / `in`），skill 端只解析这几种，避免写成任意表达式。
3. **多层依赖**：profile 字段能否依赖其他 profile 字段？（如"BMI = 体重/身高²"需要体重和身高两个字段，computation 引两个。）当前支持，`computation` 可写表达式。但复杂计算是否值得？建议 v2 只支持"单字段基准 + 简单四则"。
