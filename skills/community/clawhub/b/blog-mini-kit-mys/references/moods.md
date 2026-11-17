# 说说 API（3 端点）

路径前缀：`{base_url}` · 无认证

## 1. GET /api/moods — 说说列表

**子命令**：`list-moods`

```bash
curl -s --max-time 30 "{base_url}/api/moods"
```

响应：
```json
{"code":200,"data":[{"id":1,"title":"今日心情","content":"阳光明媚","src":"","createtime":"2026-08-25T03:00:00"}]}
```

## 2. POST /api/moods — 发布说说

**子命令**：`create-mood`

Body（JSON，`MoodCreate`）：

| 字段 | 类型 | 必填 | 默认 | 说明 |
|------|------|------|------|------|
| content | string | 是 | - | 说说内容 |
| title | string | 否 | "" | 标题 |
| src | string | 否 | "" | 媒体 URL（图片/视频） |

```bash
curl -s --max-time 30 -X POST -H "Content-Type: application/json" \
  -d '{"content":"今天很开心","title":"日记"}' "{base_url}/api/moods"
```

响应：`{"code":200,"data":{"id":2}}`

## 3. DELETE /api/moods/{mood_id} — 删除说说

**子命令**：`delete-mood`

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| mood_id | path | int | 是 | 说说 ID |

> 硬删除（DELETE FROM mood），不可恢复。

响应：`{"code":200,"message":"说说已删除"}`
