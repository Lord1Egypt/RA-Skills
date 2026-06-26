# Output Patterns

## Route decision response

只返回一个 JSON 对象：

```json
{
  "decisions": [
    {
      "file_id": "file_abc123",
      "route": "text",
      "reason": null
    }
  ]
}
```

约束：

- 每个输入文件必须正好返回一条 decision。
- `route` 只允许：
  - `text`
  - `parser_lite`
  - `parser_export`
  - `ocr`
  - `vlm`
  - `skip`
- 如果 `route = "skip"`，`reason` 不能为空。
- 除 `skip` 外，`reason` 优先 `null`；只有确实需要解释 override 时才写短语。
- 默认优先采用 `suggested_route`，除非输入里已有明确冲突信号。
