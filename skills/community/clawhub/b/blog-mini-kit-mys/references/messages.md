# 留言 API（4 端点）

路径前缀：`{base_url}` · 无认证

## 1. GET /api/messages — 留言列表（含回复）

**子命令**：`list-messages`

```bash
curl -s --max-time 30 "{base_url}/api/messages"
```

响应：
```json
{"code":200,"data":[{"id":1,"uid":1,"content":"你好","deleted":0,"uname":"admin","img":"img/moren.jpg","createtime":"...","replies":[{"id":1,"uid":1,"mid":1,"content":"回复","uname":"admin","img":"..."}]}]}
```

> 每条留言含 `replies` 数组（留言回复列表）。

## 2. POST /api/messages — 发表留言

**子命令**：`create-message`

Body（JSON，`MessageCreate`）：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| uid | int | 是 | 用户 ID |
| content | string | 是 | 留言内容 |

响应：`{"code":200,"data":{"id":2}}`

## 3. POST /api/messages/reply — 回复留言

**子命令**：`reply-message`

Body（JSON，`Message2Create`）：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| uid | int | 是 | 用户 ID |
| mid | int | 是 | 留言 ID（被回复的留言） |
| content | string | 是 | 回复内容 |

```bash
curl -s --max-time 30 -X POST -H "Content-Type: application/json" \
  -d '{"uid":1,"mid":1,"content":"回复内容"}' "{base_url}/api/messages/reply"
```

响应：`{"code":200,"data":{"id":1}}`

## 4. DELETE /api/messages/{message_id} — 删除留言

**子命令**：`delete-message`

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| message_id | path | int | 是 | 留言 ID |

> 软删除（deleted=1）。

响应：`{"code":200,"message":"留言已删除"}`
