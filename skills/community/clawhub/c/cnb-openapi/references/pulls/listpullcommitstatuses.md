# ListPullCommitStatuses

## 原始 Swagger
https://api.cnb.cool/#/operations/ListPullCommitStatuses

## 接口描述
查询 Pull Request 的状态检查
## 接口权限
repo-pr:r
## 请求信息

**请求方法：** GET

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/pulls/{number}/commit-statuses

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


**响应类型：** api.CommitStatuses

**响应结构：**
```json
{
  "sha": "string", // 提交的哈希值。
  "state": "string", // 整体提交状态。
  "statuses": [{
    "context": "string", // 状态检查的上下文标识符。
    "created_at": "string", // 创建时间。
    "description": "string", // 状态检查的描述信息。
    "state": "string", // 状态检查结果。
    "target_url": "string", // 状态检查的详细信息链接地址。
    "updated_at": "string" // 最后更新时间。
  }] // 具体的提交状态检查列表。
}
```
## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/{repo}/-/pulls/{number}/commit-statuses" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
```
