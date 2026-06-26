# ListForksRepos

## 原始 Swagger
https://api.cnb.cool/#/operations/ListForksRepos

## 接口描述
获取指定仓库的 fork 列表。Get fork list for specified repository.
## 接口权限
repo-base-info:r
## 请求信息

**请求方法：** GET

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/forks

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| repo | 字符串 | 是 | 仓库路径。Repository path.|

### 查询参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| start_from_root | 布尔值 | 否| 是否从fork根节点开始展示。Whether to start from the root node of the fork.|
| page | 整数 | 否| 页码。Pagination page number.|
| page_size | 整数 | 否| 每页大小。Pagination page size.|
## 响应信息


**响应类型：** dto.ListForks

**响应结构：**
```json
{
  "fork_tree_count": 0,
  "forks": [{
    "created_at": "string",
    "fork_count": 0,
    "freeze": false,
    "nickname": "string",
    "path": "string",
    "user_freeze": false,
    "user_lock": false,
    "username": "string"
  }]
}
```
## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/{repo}/-/forks" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-G \
-d "start_from_root=<start_from_root>" \
-d "page=<page>" \
-d "page_size=<page_size>" \
```
