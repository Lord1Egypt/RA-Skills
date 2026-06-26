# ListPullAssignees

## 原始 Swagger
https://api.cnb.cool/#/operations/ListPullAssignees

## 接口描述
查询指定合并请求的处理人。List repository pull request assignees.
## 接口权限
repo-pr:r
## 请求信息

**请求方法：** GET

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/pulls/{number}/assignees

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
## 响应信息


**响应类型：** 数组[api.UserInfo]

**响应结构（数组元素）：**
```json
[
{
    "avatar": "string", // 用户头像。
    "email": "string", // 用户邮箱。
    "freeze": false, // 是否冻结。
    "is_npc": false, // 是否是 NPC。
    "nickname": "string", // 昵称。
    "username": "string" // 用户名。
  }
]
```
## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/{repo}/-/pulls/{number}/assignees" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
```
