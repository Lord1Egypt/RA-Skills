# JSON Schema 模板规格

> 适用场景：3 SQL 生成（API 输出校验）/ 5 批量分类标注（标签树结构）
> 配套方法论：M3（80/20 协作）+ M5（两级标签体系）

## 触发场景

| 场景 | 用途 | 与 Prompt 的关系 |
|------|------|----------------|
| 3 SQL | API 响应数据格式规范 | Prompt 输出格式说明引用此 schema |
| 5 标注 | 标签树结构定义（见 [tag-tree-template-spec.md](tag-tree-template-spec.md)） | 标注输出格式 = 此 schema |

## 模板结构（JSON Schema Draft 07）

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "{Schema 名称}",
  "description": "{Schema 用途说明}",
  "type": "object",
  "required": ["{必填字段1}", "{必填字段2}"],
  "properties": {
    "{字段名}": {
      "type": "string|number|integer|boolean|array|object",
      "description": "{字段说明}",
      "enum": ["{可选值1}", "{可选值2}"],
      "pattern": "{正则表达式}",
      "minimum": 0,
      "maximum": 999999,
      "items": {
        "type": "object",
        "properties": {}
      },
      "default": "{默认值}"
    }
  },
  "additionalProperties": false
}
```

## 生成规则

### Step 1: 从访谈快照提取字段

读取 SKILL.md Step A2 的 5 要素完备快照：
- 字段清单（来自 ddl-analyzer 或访谈）
- 字段类型（SQL 类型 → JSON 类型映射）
- 必填字段（来自访谈）
- 枚举值（来自访谈）
- 业务口径待确认项（来自 DDL 草稿）

### Step 2: SQL 类型到 JSON 类型映射

| SQL 类型 | JSON Schema type | 说明 |
|---------|----------------|------|
| BIGINT, INT, TINYINT | integer | 整数 |
| DECIMAL, FLOAT, DOUBLE | number | 浮点数 |
| VARCHAR, CHAR, TEXT | string | 字符串 |
| DATE, DATETIME, TIMESTAMP | string (format: date-time) | ISO 8601 格式 |
| BOOLEAN | boolean | 布尔值 |
| JSON | object | 嵌套对象 |

### Step 3: 注入防幻觉元素

每个 JSON Schema 必须包含：
1. **`required` 数组**：明确必填字段
2. **`additionalProperties: false`**：拒绝未定义字段（防幻觉）
3. **`description`**：每个字段必须有人类可读说明
4. **`enum`**：枚举字段必须列出所有可选值
5. **`pattern`**：格式化字段必须用正则约束（如手机号、邮箱）

### Step 4: 与 DDL 草稿联动

JSON Schema 应与 DDL 草稿的字段一一对应：
- DDL 表 → JSON object
- DDL 字段 → JSON properties
- DDL 约束 → JSON required/pattern
- DDL 注释 → JSON description

## 示例输出（场景 3 活跃学员统计 API 响应）

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ActiveStudentStatistics",
  "description": "活跃学员按城市分组的统计结果",
  "type": "object",
  "required": ["city", "active_count", "total_count", "active_rate", "statistics_time"],
  "properties": {
    "city": {
      "type": "string",
      "description": "所在城市",
      "minLength": 1,
      "maxLength": 32
    },
    "active_count": {
      "type": "integer",
      "description": "活跃学员数",
      "minimum": 0
    },
    "total_count": {
      "type": "integer",
      "description": "该城市总学员数",
      "minimum": 0
    },
    "active_rate": {
      "type": "number",
      "description": "活跃率 = active_count / total_count",
      "minimum": 0,
      "maximum": 1,
      "note": "业务口径待确认：活跃定义"
    },
    "statistics_time": {
      "type": "string",
      "format": "date-time",
      "description": "统计时间（ISO 8601）"
    },
    "time_range": {
      "type": "object",
      "description": "统计时间范围",
      "properties": {
        "start": {"type": "string", "format": "date"},
        "end": {"type": "string", "format": "date"}
      },
      "required": ["start", "end"]
    }
  },
  "additionalProperties": false
}
```

## 示例输出（场景 5 批量标注响应）

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "BatchClassificationResult",
  "description": "批量分类标注单条结果",
  "type": "object",
  "required": ["id", "content", "primary_tag", "confidence", "reason"],
  "properties": {
    "id": {
      "type": "integer",
      "description": "原始数据 ID"
    },
    "content": {
      "type": "string",
      "description": "原始内容"
    },
    "primary_tag": {
      "type": "string",
      "description": "一级标签",
      "enum": ["{一级标签1}", "{一级标签2}"]
    },
    "secondary_tags": {
      "type": "array",
      "description": "二级标签（可多选）",
      "items": {
        "type": "string",
        "enum": ["{二级标签1}", "{二级标签2}"]
      }
    },
    "confidence": {
      "type": "number",
      "description": "置信度 0-1",
      "minimum": 0,
      "maximum": 1
    },
    "reason": {
      "type": "string",
      "description": "标注理由（必填，禁止空）"
    },
    "uncertain": {
      "type": "boolean",
      "description": "是否不确定（true 时进入待人工审核）",
      "default": false
    }
  },
  "additionalProperties": false
}
```

## 与其他模块的接口

| 接口 | 调用方 | 依赖 |
|------|--------|------|
| 上游 | ddl-template-spec.md | 字段定义同步 |
| 上游 | tag-tree-template-spec.md | 标签树作为 enum 来源 |
| 下游 | verify-template-spec.md | 验真脚本用此 schema 校验输出 |
| 关联方法论 | M3 80/20 协作 | AI 出 schema 草稿 + 人审业务字段 |
| 关联方法论 | M5 两级标签体系 | 场景 5 标签树结构 |
| 关联方法论 | M2 防幻觉三招 | required + additionalProperties: false |
