# PostPullRequestReviewReply

## 原始 Swagger
https://api.cnb.cool/#/operations/PostPullRequestReviewReply

## 接口描述
回复一个 review 评审
## 接口权限
repo-notes:rw
## 请求信息

**请求方法：** POST

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/pulls/{number}/reviews/{review_id}/replies

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
| review_id | 字符串 | 是 | PullReview唯一标识编号。|

### 请求体参数


**请求体结构：**

```json
{
  "body": "string", // 回复的评论内容。
  "reply_to_comment_id": "string" // 父评论ID。
}
```
## 响应信息


**响应类型：** api.PullReviewComment

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
  }, // 评论的作者信息。
  "body": "string", // 评论的具体内容。
  "commit_hash": "string", // 评论所基于的提交哈希值。
  "created_at": "string", // 评论的创建时间。
  "diff_hunk": [{
    "content": "string", // 实际内容文本。
    "left_line_number": 0, // 左侧（原版本）的行号。
    "prefix": "string", // 差异行的前缀符号。
    "right_line_number": 0, // 右侧（新版本）的行号。
    "type": "string" // 枚举值：`context`,`addition`,`deletion`,`context_eofnl`,`add_eofnl`,`del_eofnl`,`file_header`,`hunk_header`,`binary`
  }], // 评论关联的差异块信息。
  "end_line": 0, // 评论结束行号，subject_type=line时有效。
  "end_side": "string", // 评论结束位置的代码版本侧。枚举值：`left`,`right`
  "id": "string", // 评论的唯一标识符。
  "path": "string", // 评论所在文件的路径。示例值：`src/main.go`
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
  "reply_to_comment_id": "string", // 回复的父评论ID，如果是回复评论则不为空。
  "review_id": "string", // 所属Review的唯一标识符。
  "review_state": "string", // Review的状态。枚举值：`approved`,`changes_requested`,`commented`,`dismissed`,`pending`
  "start_line": 0, // 评论起始行号，subject_type=line时有效。
  "start_side": "string", // 评论起始位置的代码版本侧。枚举值：`left`,`right`
  "subject_type": "string", // 评论对象类型。枚举值：`line`,`file`
  "updated_at": "string" // 评论的最后更新时间。
}
```
## 请求示例

### cURL 示例

```bash
curl -X POST \
  "${CNB_API_ENDPOINT}/{repo}/-/pulls/{number}/reviews/{review_id}/replies" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-H "Content-Type: application/json" \
  -d '{
  "body": "string",
  "reply_to_comment_id": "string"
}'
```
