# 标签 API（2 端点）

路径前缀：`{base_url}` · 无认证

> ⚠️ API 实际路径为 `/api/lables`（原系统拼写），子命令使用正确拼写 `labels`，脚本内部请求用 `lables`。

## 1. GET /api/lables — 获取所有标签

**子命令**：`list-labels`

```bash
curl -s --max-time 30 "{base_url}/api/lables"
```

响应：
```json
{"code":200,"data":[{"id":1,"lname":"技术"},{"id":2,"lname":"生活"},{"id":3,"lname":"随笔"},{"id":4,"lname":"教程"}]}
```

## 2. POST /api/lables — 创建标签

**子命令**：`create-label`

Body（JSON，`LableCreate`）：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| lname | string | 是 | 标签名称 |

```bash
curl -s --max-time 30 -X POST -H "Content-Type: application/json" \
  -d '{"lname":"新标签"}' "{base_url}/api/lables"
```

响应：`{"code":200,"data":{"id":5,"lname":"新标签"}}`
