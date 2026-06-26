# 画布操作 API 参考

画布后端运行在 `http://localhost:<端口>`（默认 39301，可通过 `CLAW_PORT` 环境变量覆盖）。

## POST /api/canvas/sync/gen_image

将图片推送到画布，前端自动显示并定位。

```bash
curl -X POST http://localhost:<端口>/api/canvas/sync/gen_image \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/image.png"}'
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `url` | string | 是 | 图片公网 URL |
| `element_id` | string | 否 | 自定义元素 ID，不传则自动生成 |

响应：`{"success": true, "element_id": "gen_abc123", "sequence_id": 5}`

## GET /api/canvas/sync/debug

查看画布当前状态（有哪些图片、连接客户端等）。

```bash
curl http://localhost:<端口>/api/canvas/sync/debug
```

响应：

```json
{
  "sequence_id": 5,
  "canvasDataCount": 2,
  "canvasData": [
    {
      "id": "gen_abc123",
      "metadata": {
        "category": "image",
        "id": "gen_abc123",
        "src": "https://example.com/gen_xxx.png",
        "is_delete": false
      },
      "style": {
        "matrix": [1, 0, 0, 1, 400, 300]
      }
    }
  ],
  "connectedClients": ["client_a1b2"]
}
```

`canvasData` 数组中每个对象的字段：

| 字段 | 说明 |
|------|------|
| `id` | 图片唯一 ID |
| `metadata.category` | 固定 `"image"` |
| `metadata.src` | 图片 URL |
| `metadata.is_delete` | `true` 表示已删除（逻辑删除） |
| `style.matrix` | 变换矩阵 `[scaleX, skewY, skewX, scaleY, translateX, translateY]` |

## POST /api/canvas/sync/inject_image

批量注入图片到画布。

```bash
curl -X POST http://localhost:<端口>/api/canvas/sync/inject_image \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://example.com/a.png", "https://example.com/b.png"]}'
```

## POST /api/canvas/sync/reset

清空画布所有数据。

```bash
curl -X POST http://localhost:<端口>/api/canvas/sync/reset
```
