# 飞书 Bitable Filter 语法参考

来源: 飞书官方文档《记录筛选参数填写说明》

## JSON 结构体 (POST Search API)

```json
{
  "filter": {
    "conjunction": "and",
    "conditions": [
      {"field_name": "字段名", "operator": "is", "value": ["值"]}
    ]
  }
}
```

### Operator

- is / isNot / contains / doesNotContain
- isEmpty / isNotEmpty
- isGreater / isGreaterEqual / isLess / isLessEqual

### 日期字段 value

- `["ExactDate", "毫秒时间戳"]` — 精确日期
- `["Today"]` / `["Tomorrow"]` / `["Yesterday"]`
- `["CurrentWeek"]` / `["LastWeek"]` (operator 仅支持 is)
- `["CurrentMonth"]` / `["LastMonth"]` (operator 仅支持 is)
- `["TheLastWeek"]` — 过去七天 (operator 仅支持 is)
- `["TheNextWeek"]` — 未来七天 (operator 仅支持 is)
- `["TheLastMonth"]` — 过去三十天 (operator 仅支持 is)
- `["TheNextMonth"]` — 未来三十天 (operator 仅支持 is)

### 嵌套 (一层 children)

```json
{
  "conjunction": "and",
  "children": [
    {"conjunction": "or", "conditions": [...]},
    {"conjunction": "or", "conditions": [...]}
  ]
}
```

### 人员字段

value 填 open_id: `["ou_xxx"]`

### 注意

- Search API 的 DuplexLink 字段不返回 text，只返回 link_record_ids
- value 为空时必须写 `"value": []`
- 日期字段 operator 仅支持 is/isEmpty/isNotEmpty/isGreater/isLess
