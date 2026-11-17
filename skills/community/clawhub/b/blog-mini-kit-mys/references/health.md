# 健康检查 API（1 端点）

路径前缀：`{base_url}` · 无认证

## 1. GET /health — 健康检查

**子命令**：`health-check`

```bash
curl -s --max-time 30 "{base_url}/health"
```

响应：
```json
{"status":"ok","service":"blog-api","version":"1.0.0"}
```

> 用于验证 API 可达性。返回 200 + `status:"ok"` 即服务正常。
