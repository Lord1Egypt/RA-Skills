# GetFollowersByUserID

## 原始 Swagger
https://api.cnb.cool/#/operations/GetFollowersByUserID

## 接口描述
获取指定用户的粉丝列表。Get the followers list of specified user.
## 接口权限
account-engage:r
## 请求信息

**请求方法：** GET

**请求地址：** ${CNB_API_ENDPOINT}/users/{username}/followers

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| username | 字符串 | 是 | Username|

### 查询参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| page | 整数 | 否| Pagination page number|
| page_size | 整数 | 否| Pagination page size|
## 响应信息


**响应类型：** 数组[dto.UserFollowResult]

**响应结构（数组元素）：**
```json
[
{
    "freeze": false,
    "is_following": false, // 查询人是否follow了此用户
    "locked": false,
    "nickname": "string",
    "username": "string"
  }
]
```
## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/users/{username}/followers" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-G \
-d "page=<page>" \
-d "page_size=<page_size>" \
```
