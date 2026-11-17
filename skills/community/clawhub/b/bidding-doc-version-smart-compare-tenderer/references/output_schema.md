# Output Schema · 招标人版

> 定义 `findings.json`（阶段④⑤输出）和最终报告的数据结构。
> 本 Schema 仅适用于 **招标人版（tenderer）**。

---

## 1. findings.json 顶层结构

```json
{
  "items": [ { "单条变更分类+核查结果" } ],
  "meta": {
    "old_file": "原版文件名",
    "new_file": "新版文件名",
    "role": "tenderer",
    "generated_at": "ISO8601时间戳",
    "total_changes": 4,
    "global_risk_level": "高危|中危|低危|安全",
    "release_recommendation": "暂停发布，修正后再发|可发布但建议附带说明|可发布但备口径|正常发布",
    "top_concerns": [ "最需关注的1-3条摘要" ],
    "timeliness_verdict": { "ok": true, "note": "说明" },
    "action_before_release": [ "发布前待办清单" ]
  }
}
```

---

## 2. items[] 单条结构（阶段④ + 阶段⑤ 合并）

### 2.1 阶段④ 分类字段

| 字段 | 类型 | 必填 | 取值/说明 |
|------|:----:|:----:|----------|
| `clause_id` | string | ✅ | 条款编号，如 `"三.(2)"` / `"表4-R1"` / `"六.2"` |
| `change_type` | string | ✅ | `"修改"` / `"新增"` / `"删除"` |
| `safety_level` | string | ✅ | `"合规安全"` / `"需关注"` / `"仅格式"` |
| `is_complaint_risk` | bool | ✅ | 是否存在被质疑/投诉的风险 |
| `competition_impact` | string | ✅ | `"无影响"` / `"轻微收窄"` / `"明显收窄"` / `"可能涉嫌排斥"` |
| `terminology_consistency` | string | ✅ | `"一致"` / `"有不一致"` / `"需全局核查"` |
| `severity` | string | ✅ | `"高"` / `"中"` / `"低"` |
| `impact` | string | ✅ | 变更内容描述（招标人视角，1-3句话） |
| `complaint_trigger` | string | ✅ | 质疑触发点描述；若 is_complaint_risk=false 则为空字符串 `""` |
| `selfcheck_items` | string[] | ✅ | 发布前自检 checklist（具体可执行项），格式如 `["确认全文称谓统一","核对表格同步"]` |
| `basis` | string | ✅ | 判定依据（法规/标准/通用判断） |
| `basis_source` | string | ✅ | 依据来源，格式：`"IMA:知识库名称 / 具体条目"` 或 `"通用判断"` 或 `"XX法第X条"` |
| `action` | string | ✅ | 招标人处置建议，如 `"保留。发布前做好称谓统一即可。"` |
| `confidence` | number | ✅ | 判定置信度 0.0–1.0 |

**可选字段**（从 diff 继承，用于报告展示原文对比）：

| 字段 | 类型 | 说明 |
|------|------|------|
| `old_text` | string | 原文（截断至500字） |
| `new_text` | string | 新文（截断至500字） |
| `numeric_delta` | string | 数值变动摘要，如 `"水耗量 23→25 m³/d"`；无非数值变更则为空 |

### 2.2 阶段⑤ 追加字段

#### legal_check（法定阈值检查）

```json
{
  "legal_check": {
    "threshold_breached": false,
    "breached_items": ["超出阈值的参数列表"],
    "legal_basis": "触犯的法规条款"
  }
}
```

**速查参数表**：

| 参数 | 法定阈值 | 来源 |
|------|---------|------|
| 投标保证金 | ≤ 项目预算金额的 2% | 政府采购法实施条例第33条 |
| 履约保证金 | ≤ 合同金额的 10% | 政府采购法实施条例第48条 |
| 文件发售期 | ≥ 5 个工作日 | 政府采购法实施条例第21条 |
| 公示期 | ≥ 3 日（中标结果）/ ≥ 5 日（更正） | 各部委规定 |
| 等标期（投标截止） | ≥ 20 日（公开招标） | 政府采购法第35条 |
| 补充合同金额 | ≤ 原合同金额的 10% | 政府采购法第49条 |
| 质疑期 | 7 个工作日内 | 政府采购法第52条 |
| 顺延规则 | 变更影响编制则 ≥ 15 日顺延 | 实务惯例 + 多地规定 |
| 资格设定与履约相关 | 必须相关 | 《政府采购需求管理办法》 |
| 国企/中小企业倾向 | 不得非法限制 | 公平竞争审查制度 |

#### consistency_check（一致性扫描）

```json
{
  "consistency_check": {
    "terminology_ok": false,        // 称谓是否一致
    "reference_ok": true,           // 法规引用是否准确
    "table_sync_ok": true,          // 表格与正文是否同步
    "star_mark_ok": true,           // ★号标记一致性
    "issues_found": ["发现的问题列表"]
  }
}
```

#### timeliness_check（时限合规检查）

```json
{
  "timeliness_check": {
    "affects_preparation": false,   // 是否影响投标人编制
    "days_to_deadline": null,       // 距截止日天数（需用户提供截止日）
    "extension_required": false,    // 是否需要顺延
    "extension_note": ""            // 顺延说明
  }
}
```

#### priority + release_decision（优先级 + 发布决策）

| 字段 | 取值 | 触发条件 |
|------|------|---------|
| `priority` | `"P0"` / `"P1"` / `"P2"` / `"P3"` / `"P4"` | 见下表 |
| `release_decision` | `"必须修正"` / `"补充说明"` / `"备口径"` / `"正常发布"` | 见下表 |

**优先级判定规则**：

| Priority | 含义 | 触发条件 |
|----------|------|---------|
| P0 | **立即处理，必须修正** | safety_level=需关注 AND (is_complaint_risk=true OR competition_impact=明显收窄/涉嫌排斥) |
| P1 | **尽快处理** | is_complaint_risk=true 但 severity≠高 |
| P2 | **尽快处理** | terminology_consistency≠"一致" OR affects_preparation=true 且有实质商务变更 |
| P3 | **记录备查** | safety_level=合规安全 但无风险/无一致性问题 |
| P4 | **无需处理** | safety_level=仅格式 |

**发布决策映射**：

| 条件 | release_decision |
|------|-----------------|
| P0 | `必须修正` |
| P1 | `必须修正` |
| P2 且 safety_level=需关注 | `补充说明` |
| P2 且 safety_level=合规安全 | `备口径` |
| P3/P4 | `正常发布` |

#### final_severity

| 原始 severity | 升级条件 | final_severity |
|:---:|:---|:---:|
| 低 | confidence < 0.85 | → **中** |
| 中 | confidence < 0.80 | → **高** |
| 高 | — | 不变 |
| 其他 | — | 不变 |

---

## 3. meta 全局汇总字段

```json
{
  "total_changes": 4,
  "by_safety": { "合规安全": 2, "需关注": 0, "仅格式": 2 },
  "by_priority": { "P0": 0, "P1": 0, "P2": 2, "P3": 0, "P4": 2 },
  "global_risk_level": "高危|中危|低危|安全",
  "release_recommendation": "暂停发布，修正后再发|可发布但建议附带说明|可发布但备口径|正常发布",
  "top_concerns": [
    "三.(2)：称谓混用（甲方/乙方 vs 采购人/中标供应商）需全文统一"
  ],
  "timeliness_verdict": {
    "ok": true,
    "note": "变更量较小(4条)，核心变更为商务条件优化(招标人让利性质)"
  },
  "action_before_release": [
    "1. 全文搜索替换称谓（乙方↔中标供应商），确保统一",
    "2. 确认表格版本与正文已完全同步",
    "3. 准备好电费财政拨付条款的标准答复口径备用"
  ]
}
```

### global_risk_level 判定算法

```
IF (存在 P0) OR (存在 高危complaint_risk):
    → "高危"
ELSE IF (任何 is_complaint_risk) OR (任何 safety_level=="需关注"):
    → "中危"
ELSE IF (任何 terminology_consistency != "一致"):
    → "低危"
ELSE:
    → "安全"
```

---

## 4. 与投标人版的字段差异对照

| 字段 | 招标人版 | 投标人版 |
|------|:-------:|:-------:|
| 主分类轴 | **safety_level** | dimension × sentiment |
| 核心布尔 | **is_complaint_risk** | **is_redline** |
| 竞争维度 | **competition_impact** | implicit_barrier |
| 称谓检测 | **terminology_consistency** | 无 |
| 自检项 | **selfcheck_items[]** | 无 |
| 优先级 | **priority** P0-P4 | severity 高/中/低 |
| 发布决策 | **release_decision** | action（投标应对） |
| 报价影响 | ❌ 无 | **pricing_risk** |
| 时限权利 | timeliness_check.affects_preparation | **timeliness_rights[]** |
