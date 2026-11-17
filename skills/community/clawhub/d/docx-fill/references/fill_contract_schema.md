# Fill Contract Schema

Fill Contract 是 docx-fill 的核心契约，由 STRUCTURE_AGENT 产出，CONTENT_AGENT 与 EVALUATOR 消费。本文件定义其字段规范。

## 顶层结构

```json
{
  "template_id": "string",
  "template_path": "string",
  "placeholders": [...],
  "static_texts": [...],
  "content_structure_guidance": "string",
  "conflicts": [...]
}
```

### template_id
- 类型：string
- 说明：模板的唯一标识，建议用模板文件名或自定义 ID

### template_path
- 类型：string
- 说明：模板文件的绝对路径

### placeholders
占位符数组，每个占位符代表模板中需要填充内容的位置。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | string | 是 | 占位符唯一标识，格式 `p1`, `p2`... |
| type | enum | 是 | `paragraph` / `table_cell` / `heading` / `list_item` |
| location | object | 是 | 定位信息，见下 |
| original_text | string | 是 | 模板原文，作为约束追溯依据 |
| is_placeholder | bool | 是 | `true` 表示需填充 |
| is_static | bool | 是 | `true` 表示静态文本不可改 |
| content_constraint | string | 否 | 内容要求（来自原文显式文字或表头派生） |
| required_keywords | string[] | 否 | 必须包含的关键词 |
| min_words | int | 否 | 最小字数 |
| max_words | int | 否 | 最大字数 |
| header_text | string | 否 | 仅 `table_cell`：该单元格所属表头的文本（用于无显式标记时从表头派生约束） |
| header_location | object | 否 | 仅 `table_cell`：表头所在 location，便于校验对齐 |
| expected_value_type | string | 否 | 期望值类型提示，枚举如 `enum:男,女` / `int:0-150` / `date` / `money` / `email` / `text` |

### location

不同 type 的 location 字段不同：

**paragraph / heading / list_item**
```json
{"para_index": 12}
```

**table_cell**
```json
{
  "table_index": 0,
  "row": 2,
  "col": 1
}
```

**嵌套表格中的 cell**（如表格单元格内嵌套的表格）
```json
{
  "table_index": "0.2.1",
  "row": 0,
  "col": 1
}
```
其中 `table_index` 为字符串，层级用 `.` 分隔。

### static_texts
静态文本数组，渲染时原样保留。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | string | 是 | 格式 `s1`, `s2`... |
| location | object | 是 | 同 placeholders 的 location |
| text | string | 是 | 原文 |
| note | string | 否 | 标注用途（如"标题"） |

### content_structure_guidance
- 类型：string
- 说明：对整篇文档的内容结构提示，由 STRUCTURE_AGENT 根据模板整体观察总结

### conflicts
冲突列表，初始为空 `[]`。CONFLICT_CHECKER 检测到冲突后，宿主智能体将用户选择写入此字段。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| placeholder_id | string | 是 | 关联的占位符 id |
| description | string | 是 | 冲突描述 |
| options | object[] | 是 | 候选选项 |
| resolved_value | string | 否 | 用户选择后的最终值 |

## 表格密集型模板的特殊处理

### 表头单元格
模板中作为表头的单元格（如"项目名称"、"金额"、"备注"），默认标记为 `is_static=true`。判断依据：
- 单元格文本是名词性短语
- 同列其他单元格是数据填充位
- 模板原文未显式要求填写表头

### 表头-数据单元格绑定（强制）
为避免数据填错列，每个 `table_cell` 类型的占位符**必须**回溯所属表头并填写：
- `header_text`：表头单元格的文本（如"性别"、"年龄"）
- `header_location`：表头所在 location
- `content_constraint`：若 `original_text` 为空或无显式约束，则由 `header_text` 派生（如 `header_text="性别"` → `content_constraint="填写性别"`）
- `expected_value_type`：STRUCTURE_AGENT 根据表头语义识别值类型，便于代码层语义校验。常见映射：
  - `性别` → `enum:男,女`
  - `年龄` / `岁数` → `int:0-150`
  - `金额` / `经费` / `预算` / `费用` / `价格` → `money`
  - `日期` / `时间` / `出生日期` / `开始日期` / `结束日期` → `date`
  - `邮箱` / `电子邮件` / `Email` → `email`
  - `电话` / `手机` / `联系方式` → `phone`
  - `编号` / `工号` / `学号` → `id`
  - 其他/无法识别 → `text`

**回溯规则**：
- 优先从同列上一行（`row-1, col`）的静态单元格文本作为表头
- 若上一行也是数据单元格，继续向上回溯直到找到静态单元格
- 若整列无静态表头，从同行上一列（`row, col-1`）查找
- 若均无表头，`header_text` 留空，`expected_value_type="text"`

### 合并单元格
`extract_structure.py` 输出 `merged_cells` 列表标识合并区域。Fill Contract 中：
- 合并单元格的起始位置作为占位符 location
- `span` 字段可选，标记跨行/跨列范围

```json
{
  "location": {"table_index": 0, "row": 3, "col": 0},
  "span": {"row_span": 3, "col_span": 2}
}
```

### 嵌套表格
项目申报书常见"表格内嵌套表格"结构。处理时：
- 外层表格 cell 中的嵌套表格在 `nested_tables` 中
- 占位符若位于嵌套表格内，`table_index` 使用点分路径（如 `"0.1.0"`）

## 约束来源规则（强制）

1. **约束仅来自模板原文的显式文字**：如原文写"本部分要以毕业要求为依据"→ `content_constraint: "撰写内容需符合毕业要求"` + `required_keywords: ["毕业要求"]`
2. **结构硬约束来自结构本身**：如表格有 3 列 → 隐含内容需适配 3 列
3. **不自行生成约束**：模板没有要求的，不添加。LLM 不得推断发挥

## 示例：项目申报书片段

```json
{
  "placeholders": [
    {
      "id": "p1",
      "type": "table_cell",
      "location": {"table_index": 0, "row": 0, "col": 1},
      "original_text": "（请填写项目名称）",
      "is_placeholder": true,
      "is_static": false,
      "content_constraint": "填写项目名称",
      "header_text": "项目名称",
      "header_location": {"table_index": 0, "row": 0, "col": 0},
      "expected_value_type": "text",
      "min_words": 2,
      "max_words": 30
    },
    {
      "id": "p2",
      "type": "table_cell",
      "location": {"table_index": 0, "row": 1, "col": 1},
      "original_text": "（请填写项目简介，不超过500字）",
      "is_placeholder": true,
      "is_static": false,
      "content_constraint": "撰写项目简介，不超过500字",
      "header_text": "项目简介",
      "header_location": {"table_index": 0, "row": 1, "col": 0},
      "expected_value_type": "text",
      "min_words": 50,
      "max_words": 500
    },
    {
      "id": "p3",
      "type": "table_cell",
      "location": {"table_index": 1, "row": 0, "col": 1},
      "original_text": "（请填写申请经费，单位万元）",
      "is_placeholder": true,
      "is_static": false,
      "content_constraint": "填写申请经费金额，单位万元",
      "header_text": "申请经费（万元）",
      "header_location": {"table_index": 1, "row": 0, "col": 0},
      "expected_value_type": "money",
      "min_words": 1,
      "max_words": 10
    }
  ],
  "static_texts": [
    {"id": "s1", "location": {"table_index": 0, "row": 0, "col": 0}, "text": "项目名称", "note": "表头"},
    {"id": "s2", "location": {"table_index": 0, "row": 1, "col": 0}, "text": "项目简介", "note": "表头"},
    {"id": "s3", "location": {"table_index": 1, "row": 0, "col": 0}, "text": "申请经费（万元）", "note": "表头"}
  ]
}
```
