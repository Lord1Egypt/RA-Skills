# ListAllMembers

## 原始 Swagger
https://api.cnb.cool/#/operations/ListAllMembers

## 接口描述
获取指定仓库内的有效成员列表，包含继承成员。List active members in specified repository including inherited members.
## 接口权限
repo-manage:r
## 请求信息

**请求方法：** GET

**请求地址：** ${CNB_API_ENDPOINT}/{slug}/-/list-members

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| slug | 字符串 | 是 | slug|

### 查询参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| page | 整数 | 否| Pagination page number|
| page_size | 整数 | 否| Pagination page size|
| role | 字符串 | 否| Role|
| search | 字符串 | 否| 过滤成员。Filter by member|
| names | 字符串 | 否| 精准匹配用户名,多个用户名用逗号间隔。Exact username matching, multiple usernames separated by commas.|
| order_by | 字符串 | 否| Order field|
| desc | 布尔值 | 否| Ordering|
## 响应信息


**响应类型：** 数组[dto.UsersWithAccessLevelInSlug]

**响应结构（数组元素）：**
```json
[
{
    "access_level": {
    },
    "avatar": "string",
    "created_at": "string",
    "email": "string",
    "email_verification": "string",
    "freeze": false,
    "id": "string",
    "inviter": {
      "avatar": "string",
      "created_at": "string",
      "email": "string",
      "freeze": false,
      "id": "string",
      "locked": false,
      "nickname": "string",
      "type": {
      },
      "username": "string",
      "verified": 0, // 认证类型
      "verified_expire_in": "string" // 认证过期时间
    },
    "join_time": "string",
    "locked": false,
    "nickname": "string",
    "type": {
    },
    "username": "string",
    "verified": 0, // 认证类型
    "verified_expire_in": "string" // 认证过期时间
  }
]
```
## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/{slug}/-/list-members" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-G \
-d "page=<page>" \
-d "page_size=<page_size>" \
-d "role=<role>" \
-d "search=<search>" \
-d "names=<names>" \
-d "order_by=<order_by>" \
-d "desc=<desc>" \
```
