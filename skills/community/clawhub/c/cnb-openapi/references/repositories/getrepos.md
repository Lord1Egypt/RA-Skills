# GetRepos

## 原始 Swagger
https://api.cnb.cool/#/operations/GetRepos

## 接口描述
获取当前用户拥有指定权限及其以上权限的仓库。List repositories owned by the current user with the specified permissions or higher.
## 接口权限
account-engage:r
## 请求信息

**请求方法：** GET

**请求地址：** ${CNB_API_ENDPOINT}/user/repos

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 查询参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| page | 整数 | 否| Pagination page number|
| page_size | 整数 | 否| Pagination page size|
| search | 字符串 | 否| Filter by repositories|
| filter_type | 字符串 | 否| RType|
| role | 字符串 | 否| 最小仓库权限，默认owner。Minima repository permissions|
| flags | 字符串 | 否| 仓库类型标记，逗号分隔。Repository type flags, comma separated|
| status | 字符串 | 否| 仓库状态。Repository status|
| order_by | 字符串 | 否| Order field|
| desc | 布尔值 | 否| 排序顺序。Ordering.|
## 响应信息


**响应类型：** 数组[dto.Repos4User]

**响应结构（数组元素）：**
```json
[
{
    "access": {
    },
    "created_at": "string",
    "description": "string",
    "display_module": {
      "activity": false, // 仓库动态
      "contributors": false, // 仓库贡献者
      "release": false // 仓库版本
    },
    "flags": {
    },
    "fork_count": 0,
    "forked_from_repo": {
      "created_at": "string",
      "freeze": false,
      "path": "string",
      "resource_id": 0,
      "resource_type": {
      },
      "root_freeze": false,
      "root_id": 0,
      "updated_at": "string"
    }, // 预留
    "freeze": false,
    "id": "string",
    "language": "string", // 仓库程序语言，预留
    "languages": {
      "color": "string",
      "language": "string"
    }, // 仓库语言
    "last_update_nickname": "string", // 最新代码更新人姓名
    "last_update_username": "string", // 最新代码更新人账户名
    "last_updated_at": {
      "time": "string",
      "valid": false // Valid is true if Time is not NULL
    }, // 最新代码更新时间
    "license": "string",
    "mark_count": 0,
    "name": "string",
    "open_issue_count": 0, // 开启的issue数
    "open_pull_request_count": 0, // 开启的pull request数
    "path": "string", // 完整仓库路径
    "pinned": false,
    "pinned_time": "string",
    "second_languages": {
      "color": "string",
      "language": "string"
    }, // 第二语言
    "site": "string",
    "star_count": 0,
    "star_time": "string",
    "stared": false,
    "status": {
    },
    "tags": ["<unknown>"],
    "topics": "string",
    "updated_at": "string",
    "visibility_level": {
    },
    "web_url": "string"
  }
]
```
## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/user/repos" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-G \
-d "page=<page>" \
-d "page_size=<page_size>" \
-d "search=<search>" \
-d "filter_type=<filter_type>" \
-d "role=<role>" \
-d "flags=<flags>" \
-d "status=<status>" \
-d "order_by=<order_by>" \
-d "desc=<desc>" \
```
