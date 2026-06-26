# ListStarUsers

## 原始 Swagger
https://api.cnb.cool/#/operations/ListStarUsers

## 接口描述
获取指定仓库的star用户列表。Get the list of users who starred the specified repository.
## 接口权限
repo-basic-info:r
## 请求信息

**请求方法：** GET

**请求地址：** ${CNB_API_ENDPOINT}/{slug}/-/stars

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
| filter_type | 字符串 | 是| Filter type|
| page | 整数 | 否| page|
| page_size | 整数 | 否| page|
## 响应信息


**响应类型：** dto.RepoStarUsers

**响应结构：**
```json
{
  "my_follow_count": 0,
  "total": 0,
  "users": [{
    "avatar": "string",
    "created_at": "string",
    "email": "string",
    "freeze": false,
    "id": "string",
    "is_follow": false,
    "locked": false,
    "nickname": "string",
    "stared_at": "string",
    "type": {
    },
    "username": "string",
    "verified": 0, // 认证类型
    "verified_expire_in": "string" // 认证过期时间
  }]
}
```
## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/{slug}/-/stars" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-G \
-d "filter_type=<filter_type>" \
-d "page=<page>" \
-d "page_size=<page_size>" \
```
