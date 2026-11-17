# academic-figures-mcp E2E transcript

## initialize
```json
{"server": "academic-figures", "in_memory": true}
```

## tools/list
```json
["doctor", "render_chart", "suggest_chart"]
```

## tools/call render_chart
```json
{"status": "ok", "files": [{"format": "png", "path": "/tmp/af_mcp_out/bar_150dpi.png"}], "preview_bytes": 26696}
```

## tools/call suggest_chart
```json
{"status": "ok"}
```

## tools/call doctor
```json
{"exit_code": 0}
```

## resources/read capability://matrix
```json
{"count": 27, "journals": ["cell", "cma", "cn-core", "ieee", "jama", "lancet", "nature", "nejm", "science"]}
```

## resources/read capability://changelog
```json
{"head_ok": true}
```

## prompts/get chart_picker
```json
{"messages": 1}
```

## tools/call render_chart 未知图型（预期错误）
```json
{"error_type": "ToolError"}
```
