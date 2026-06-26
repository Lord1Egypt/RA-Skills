# SetPinnedRepoByGroup

## 原始 Swagger
https://api.cnb.cool/#/operations/SetPinnedRepoByGroup

## 接口描述
更新指定组织仓库墙。Update the pinned repositories of a group.
## 接口权限
group-manage:rw
## 请求信息

**请求方法：** PUT

**请求地址：** ${CNB_API_ENDPOINT}/{slug}/-/pinned-repos

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| slug | 字符串 | 是 | slug|

### 请求体参数


**参数类型：** 数组[字符串]


**描述：** repo path
## 响应信息


**响应类型：** 数组[dto.Repos4UserBase]

**响应结构（数组元素）：**
```json
[
{
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
    "second_languages": {
      "color": "string",
      "language": "string"
    }, // 第二语言
    "site": "string",
    "star_count": 0,
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
curl -X PUT \
  "${CNB_API_ENDPOINT}/{slug}/-/pinned-repos" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-H "Content-Type: application/json" \
  -d '{"request": "<request>"}'
```
