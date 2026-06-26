# PostPullComment

## 原始 Swagger
https://api.cnb.cool/#/operations/PostPullComment

## 接口描述
新增一个合并请求评论。Create a pull comment.
## 接口权限
repo-notes:rw
## 请求信息

**请求方法：** POST

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/pulls/{number}/comments

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| repo | 字符串 | 是 | 不带.git后缀的仓库名称。格式：`组织名称/仓库名称`|
| number | 字符串 | 是 | Pull唯一标识编号。|

### 请求体参数


**请求体结构：**

```json
{
  "body": "string" // 评论内容。
}
```
## 响应信息


**响应类型：** api.PullRequestComment

**响应结构：**
```json
{
  "author": {
    "avatar": "string", // 用户头像。
    "email": "string", // 用户邮箱。
    "freeze": false, // 是否冻结。
    "is_npc": false, // 是否是 NPC。
    "nickname": "string", // 昵称。
    "username": "string" // 用户名。
  }, // 评论作者信息。
  "body": "string", // 评论内容。
  "created_at": "string", // 创建时间。
  "id": "string", // 合并请求评论的唯一标识符。
  "reactions": [{
    "count": 0, // 该表情的数量。
    "has_reacted": false, // 当前用户是否已使用该 Reaction。
    "reaction": "string", // Reaction 表情类型。
    "top_users": [{
      "avatar": "string", // 用户头像。
      "email": "string", // 用户邮箱。
      "freeze": false, // 是否冻结。
      "is_npc": false, // 是否是 NPC。
      "nickname": "string", // 昵称。
      "username": "string" // 用户名。
    }] // 最近使用该 Reaction 的用户列表。
  }], // Reaction 数量列表。
  "updated_at": "string" // 最后更新时间。
}
```
## 请求示例

### cURL 示例

```bash
curl -X POST \
  "${CNB_API_ENDPOINT}/{repo}/-/pulls/{number}/comments" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-H "Content-Type: application/json" \
  -d '{
  "body": "string"
}'
```
