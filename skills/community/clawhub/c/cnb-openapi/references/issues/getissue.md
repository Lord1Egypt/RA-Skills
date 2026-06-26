# GetIssue

## 原始 Swagger
https://api.cnb.cool/#/operations/GetIssue

## 接口描述
查询指定的 Issues。Get an issue.
## 接口权限
repo-issue:r
## 请求信息

**请求方法：** GET

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/issues/{number}

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| repo | 字符串 | 是 | 不带.git后缀的仓库名称。格式：`组织名称/仓库名称`|
| number | 字符串 | 是 | Issue唯一标识编号。|
## 响应信息


**响应类型：** api.IssueDetail

**响应结构：**
```json
{
  "assignees": [{
    "avatar": "string", // 用户头像。
    "email": "string", // 用户邮箱。
    "freeze": false, // 是否冻结。
    "is_npc": false, // 是否是 NPC。
    "nickname": "string", // 昵称。
    "username": "string" // 用户名。
  }], // Issue处理人列表，最多支持8个处理人。
  "author": {
    "avatar": "string", // 用户头像。
    "email": "string", // 用户邮箱。
    "freeze": false, // 是否冻结。
    "is_npc": false, // 是否是 NPC。
    "nickname": "string", // 昵称。
    "username": "string" // 用户名。
  }, // Issue创建者信息。
  "body": "string", // Issue内容正文。
  "comment_count": 0, // Issue评论数量。
  "created_at": "string", // Issue创建时间。
  "ended_at": "string", // Issue结束日期。
  "invisible": false, // Issue是否可见。
  "labels": [{
    "applied_by": {
      "avatar": "string", // 用户头像。
      "email": "string", // 用户邮箱。
      "freeze": false, // 是否冻结。
      "is_npc": false, // 是否是 NPC。
      "nickname": "string", // 昵称。
      "username": "string" // 用户名。
    }, // 贴标者信息。
    "color": "string", // 标签颜色。
    "creator": {
      "avatar": "string", // 用户头像。
      "email": "string", // 用户邮箱。
      "freeze": false, // 是否冻结。
      "is_npc": false, // 是否是 NPC。
      "nickname": "string", // 昵称。
      "username": "string" // 用户名。
    }, // 标签创建者信息。
    "description": "string", // 标签描述。
    "id": "string", // 标签ID。
    "name": "string" // 标签名称。
  }], // Issue标签列表（含创建者和贴标者信息）。
  "last_acted_at": "string", // Issue最后活动时间。
  "number": "string", // Issue的唯一标识编号。
  "priority": "string", // Issue优先级。枚举值：`-2P`,`-1P`,`P0`,`P1`,`P2`,`P3`
  "started_at": "string", // Issue开始日期。
  "state": "string", // Issue状态。枚举值：`open`,`closed`
  "state_reason": "string", // 状态变更原因。枚举值：`open`,`completed`,`not_planned`,`reopened`
  "title": "string", // Issue标题，长度限制2-255字符。
  "updated_at": "string" // Issue最后更新时间。
}
```
## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/{repo}/-/issues/{number}" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
```
