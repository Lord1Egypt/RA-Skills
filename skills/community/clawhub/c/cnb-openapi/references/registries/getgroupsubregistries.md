# GetGroupSubRegistries

## 原始 Swagger
https://api.cnb.cool/#/operations/GetGroupSubRegistries

## 接口描述
查询组织下面用户有权限查看到的制品仓库。Query all registries that the user has permission to see under specific organization.
## 接口权限
group-resource:r
## 请求信息

**请求方法：** GET

**请求地址：** ${CNB_API_ENDPOINT}/{slug}/-/registries

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| slug | 字符串 | 是 | 组织 slug|

### 查询参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| page | 整数 | 否| 页码|
| page_size | 整数 | 否| 每页数量|
| registry_type | 字符串 | 否| 制品仓库类型|
| filter_type | 字符串 | 否| 制品仓库可见性类型|
| order_by | 字符串 | 否| 排序类型，默认created_at|
| desc | 布尔值 | 否| 排序顺序|
| descendant | 字符串 | 否| 查全部/查询直接属于当前组织的仓库/查询子组织的制品仓库|
| search | 字符串 | 否| 搜索关键字|
## 响应信息


**响应类型：** 数组[dto.Registry4User]

**响应结构（数组元素）：**
```json
[
{
    "access": {
    },
    "artifact_policy": "string",
    "created_at": "string",
    "description": "string",
    "freeze": false,
    "id": "string",
    "kind": "string",
    "last_push_time": "string",
    "last_push_user": {
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
    "name": "string",
    "overwrite_policy": "string",
    "path": "string",
    "pinned": false,
    "pinned_time": "string",
    "pkg_count": 0,
    "star_time": "string",
    "stared": false,
    "updated_at": "string",
    "used_size": 0,
    "visibility_level": {
    }
  }
]
```
## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/{slug}/-/registries" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-G \
-d "page=<page>" \
-d "page_size=<page_size>" \
-d "registry_type=<registry_type>" \
-d "filter_type=<filter_type>" \
-d "order_by=<order_by>" \
-d "desc=<desc>" \
-d "descendant=<descendant>" \
-d "search=<search>" \
```
