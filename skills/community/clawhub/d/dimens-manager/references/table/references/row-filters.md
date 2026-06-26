# dimens-manager 多维表格章节 行数据筛选与排序

## 1. 文档目标

这份文档专门补充 `row/page` 的真实查询口径，重点说明：

1. 行数据不是只按分页读取，而是按字段搜索、筛选、排序来读取。
2. `viewId` 不是独立于字段过滤的另一套逻辑，而是会和 `filters / filterMatchType / sortRule` 共同生效。
3. 字段设计如果不提前考虑筛选与排序，后续 `row/page` 会很难用。
4. 用户要从接口获取数据做分析时，必须先查询字段信息，再按真实字段 ID 组装 `row page` 查询条件。

---

## 0. 技能取数流程重点

当用户提出“搜索数据、筛选数据、按条件取数、导出分析、统计分析、报表预检、根据接口拿数据分析”这类需求时，技能必须把 `row/page` 当成核心取数入口处理，推荐流程是：

1. 先执行 `dimens-cli column list --team-id TEAM_ID --project-id PROJECT_ID --sheet-id SHEET_ID --output json`。
2. 从字段列表确认字段 ID、字段类型、选项值、是否适合搜索或排序。
3. 再执行 `dimens-cli row page`，用字段 ID 组装 `search-field-ids`、`filters`、`sort-rule`。
4. 拿到 `data.list` 后再进入分析、汇总、报表预览或下一步处理。

不要直接用中文字段名、展示名或猜测字段 ID 拼过滤条件。`row/page` 的筛选、搜索、排序都应基于 `column list` 返回的真实字段信息。

CLI 参数名采用命令行风格：

| 请求体字段 | CLI 参数 |
| --- | --- |
| `viewId` | `--view-id` |
| `searchFieldIds` | `--search-field-ids` |
| `filterMatchType` | `--filter-match-type` |
| `sortRule` | `--sort-rule` |

示例：

```bash
dimens-cli column list \
  --team-id TEAM_ID \
  --project-id PROJECT_ID \
  --sheet-id SHEET_ID \
  --output json

dimens-cli row page \
  --team-id TEAM_ID \
  --project-id PROJECT_ID \
  --sheet-id SHEET_ID \
  --page 1 \
  --size 50 \
  --keyword 华东 \
  --search-field-ids fld_customerName,fld_owner \
  --filters '[{"fieldId":"fld_status","operator":"equals","value":"成交"}]' \
  --filter-match-type and \
  --sort-rule '{"fieldId":"fld_amount","direction":"desc"}' \
  --output json
```

## 2. 快速索引

| 查询需求 | 核心参数 | 说明 |
| --- | --- | --- |
| 普通分页 | `page`, `size` | 基础分页 |
| 关键词搜索 | `keyword`, `searchFieldIds` | 指定参与搜索的字段 |
| 单字段筛选 | `filters` | 常见于状态、等级、负责人 |
| 多条件组合 | `filters`, `filterMatchType` | `and` / `or` |
| 排序 | `sortRule` | 常见于时间、金额、优先级 |
| 继承视图 | `viewId` | 基于视图预设的过滤与排序 |

---

## 3. `row/page` 请求体结构

当前前端真实口径已确认支持以下请求体：

```json
{
  "page": 1,
  "size": 20,
  "viewId": "view_xxx",
  "keyword": "华东",
  "searchFieldIds": ["fld_customerName", "fld_customerCode"],
  "filters": [
    {
      "columnId": "fld_customerLevel",
      "operator": "equals",
      "value": "A"
    }
  ],
  "filterMatchType": "and",
  "sortRule": {
    "columnId": "fld_lastFollowTime",
    "direction": "desc"
  }
}
```

关键字段说明：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `page` | `number` | 页码 |
| `size` | `number` | 每页条数 |
| `viewId` | `string` | 视图 ID，可继承视图预设 |
| `keyword` | `string` | 关键词搜索 |
| `searchFieldIds` | `string[]` | 指定参与关键词搜索的字段 |
| `filters` | `array` | 字段过滤条件列表 |
| `filterMatchType` | `'and' \| 'or'` | 多条件组合关系 |
| `sortRule` | `object \| null` | 排序规则 |

---

## 4. 关键词搜索

### 4.1 只搜主展示字段

适合按客户名称、联系人姓名、商机名称直接查。

```json
{
  "page": 1,
  "size": 20,
  "keyword": "华东",
  "searchFieldIds": ["fld_customerName"]
}
```

### 4.2 同时搜名称和编号

适合 CRM、项目、工单等既按名称搜，也按编号搜的场景。

```json
{
  "page": 1,
  "size": 20,
  "keyword": "KH-2026",
  "searchFieldIds": ["fld_customerName", "fld_customerCode"],
  "filters": [],
  "filterMatchType": "and"
}
```

设计建议：

- 主展示字段通常要参与搜索。
- 编号类字段如果会被人工输入查找，也建议参与搜索。
- 长备注类字段一般不建议默认纳入全局搜索，否则噪声很大。

---

## 5. 单字段筛选

### 5.1 枚举状态筛选

```json
{
  "page": 1,
  "size": 20,
  "filters": [
    {
      "columnId": "fld_customerStatus",
      "operator": "equals",
      "value": "跟进中"
    }
  ],
  "filterMatchType": "and"
}
```

### 5.2 负责人筛选

```json
{
  "page": 1,
  "size": 20,
  "filters": [
    {
      "columnId": "fld_owner",
      "operator": "equals",
      "value": "user_001"
    }
  ],
  "filterMatchType": "and"
}
```

### 5.3 空值筛选

适合查“还没有负责人”或“还没填预计成交日期”的数据。

```json
{
  "page": 1,
  "size": 20,
  "filters": [
    {
      "columnId": "fld_nextFollowTime",
      "operator": "is_empty",
      "value": null
    }
  ],
  "filterMatchType": "and"
}
```

---

## 6. 多条件组合筛选

### 6.1 `and` 组合

查“A 级客户且未流失”：

```json
{
  "page": 1,
  "size": 20,
  "filters": [
    {
      "columnId": "fld_customerLevel",
      "operator": "equals",
      "value": "A"
    },
    {
      "columnId": "fld_customerStatus",
      "operator": "not_equals",
      "value": "已流失"
    }
  ],
  "filterMatchType": "and"
}
```

### 6.2 `or` 组合

查“高价值客户或重点跟进客户”：

```json
{
  "page": 1,
  "size": 20,
  "filters": [
    {
      "columnId": "fld_customerLevel",
      "operator": "equals",
      "value": "A"
    },
    {
      "columnId": "fld_customerTag",
      "operator": "contains",
      "value": "重点跟进"
    }
  ],
  "filterMatchType": "or"
}
```

设计建议：

- 默认优先使用 `and`，用户更容易理解。
- `or` 适合做宽松召回，但必须解释清楚命中逻辑。

---

## 7. 时间范围筛选

### 7.1 最近 30 天有跟进

```json
{
  "page": 1,
  "size": 20,
  "filters": [
    {
      "columnId": "fld_lastFollowTime",
      "operator": "between",
      "value": ["2026-03-20 00:00:00", "2026-04-19 23:59:59"]
    }
  ],
  "filterMatchType": "and"
}
```

### 7.2 已过期商机

```json
{
  "page": 1,
  "size": 20,
  "filters": [
    {
      "columnId": "fld_expectedDealDate",
      "operator": "lt",
      "value": "2026-04-19"
    }
  ],
  "filterMatchType": "and"
}
```

设计建议：

- 时间字段最好单独保留，不要把时间信息揉进文本字段。
- 需要排序的时间字段建议统一格式，避免前后端解释差异。

---

## 8. relation 字段筛选

### 8.1 按目标行 ID 筛选

查“属于某客户的全部联系人”：

```json
{
  "page": 1,
  "size": 20,
  "filters": [
    {
      "columnId": "fld_customerRelation",
      "operator": "contains",
      "value": "28f202a6-b32d-47da-8d44-46914fff99b1"
    }
  ],
  "filterMatchType": "and"
}
```

### 8.2 按多个关联对象筛选

查“属于多个重点客户池的商机”：

```json
{
  "page": 1,
  "size": 20,
  "filters": [
    {
      "columnId": "fld_customerRelation",
      "operator": "in",
      "value": [
        "28f202a6-b32d-47da-8d44-46914fff99b1",
        "7f09d0e1-9408-4527-9661-f2d6f07e1234"
      ]
    }
  ],
  "filterMatchType": "and"
}
```

设计建议：

- relation 字段筛选通常依赖目标行 ID，不是直接按展示文本筛。
- 如果用户要按展示字段查找，通常要先用关键词搜索或先查目标表。

---

## 9. 排序

### 9.1 按时间倒序

```json
{
  "page": 1,
  "size": 20,
  "filters": [],
  "filterMatchType": "and",
  "sortRule": {
    "columnId": "fld_lastFollowTime",
    "direction": "desc"
  }
}
```

### 9.2 按金额升序

```json
{
  "page": 1,
  "size": 20,
  "filters": [],
  "filterMatchType": "and",
  "sortRule": {
    "columnId": "fld_expectedAmount",
    "direction": "asc"
  }
}
```

设计建议：

- `sortRule` 最适合数值和时间字段。
- 文本排序可以做，但业务意义通常弱于状态筛选和时间排序。

---

## 10. `viewId` 与字段过滤的关系

如果前端先配置了一个“最近 30 天未跟进客户”视图，读取时可以只传：

```json
{
  "page": 1,
  "size": 20,
  "viewId": "view_recent_unfollowed"
}
```

但这不代表 `viewId` 与字段过滤无关。实际说明时应明确：

- `viewId` 代表一套预配置视图。
- 视图里本身通常已经带了 `filters / filterMatchType / sortRule`。
- 如果当前请求还额外补充筛选或排序，应按“视图预设 + 当前查询”的组合口径理解。

因此，不要把“视图筛选”和“字段筛选”拆成两套完全无关的解释。

---

## 11. 常见 operator 示例

当前 Skill 文档里建议优先使用下列表达方式来举例：

| operator | 典型场景 |
| --- | --- |
| `equals` | 状态、等级、负责人精确匹配 |
| `not_equals` | 排除某个状态 |
| `contains` | relation、多值字段、模糊命中 |
| `in` | 多目标集合命中 |
| `between` | 时间区间 |
| `lt` | 截止日期、小于某个时间 |
| `gt` | 大于某个数值或时间 |
| `is_empty` | 查空值 |

如果后续 server 有更精确的 operator 枚举，以 server 真实实现为准；当前这里的职责是把查询表达方式讲清楚。

---

## 12. 与其他 references 的关系

建议按下面顺序使用：

1. 先看 `field-design-patterns.md`，确认哪些字段应该支持搜索、筛选、排序。
2. 再看本文件，把查询案例写成 `row/page` 的真实结构。
3. 最后看 `examples.md`，确认接口路径、CLI 命令、返回结构与实测数据。
