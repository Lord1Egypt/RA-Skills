> **说明**：本文为《drama-ai-studio》技能中单个 HTTP 接口的完整说明。

### 4.5 GET /openapi/drama/{play_id}/style-config
### 4.6 PUT /openapi/drama/{play_id}/style-config

获取/更新项目默认风格配置。

**路径参数（Path）：** 同 4.3。

**GET 响应（概要）：**

```json
{
  "code": 1,
  "msg": "success",
  "data": {
    "selected_style_key": "realistic",
    "styles": {
      "realistic": { "...": "..." },
      "custom": { "...": "..." }
    }
  }
}
```

**PUT 请求体（JSON）：**

需要至少提供 `selected_style_key` 或 `styles` 之一：

| 字段                | 必填 | 类型   | 说明                                   |
|---------------------|------|--------|----------------------------------------|
| `selected_style_key`| 否   | string | 当前选中的风格 key                     |
| `styles`            | 否   | object | 风格配置字典，各 key 为风格标识       |

`selected_style_key` 取值：

- `realistic` / `oriental_fantasy` / `western_fantasy` / `cyberpunk` / `pixar` / `ghibli` / `custom`

**PUT 成功响应：**

```json
{
  "code": 1,
  "msg": "success",
  "data": {
    "selected_style_key": "custom",
    "styles": {
      "custom": { "...": "..." }
    }
  }
}
```

若既未提供 `selected_style_key` 也未提供 `styles`，返回 400，`data.error` 为错误信息。
