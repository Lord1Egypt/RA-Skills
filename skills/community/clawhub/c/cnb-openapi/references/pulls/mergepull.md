# MergePull

## 原始 Swagger
https://api.cnb.cool/#/operations/MergePull

## 接口描述
合并一个合并请求。Merge a pull request.
## 接口权限
repo-pr:rw
## 请求信息

**请求方法：** PUT

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/pulls/{number}/merge

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

### 请求体参数


**请求体结构：**

```json
{
  "commit_message": "string", // 合并提交的详细描述信息。
  "commit_title": "string", // 合并提交的标题。
  "merge_style": "string" // 合并提交方式。可选值：`merge`,`squash`,`rebase`
}
```
## 响应信息


**响应类型：** api.MergePullResponse

**响应结构：**
```json
{
  "merged": false, // 是否成功合并。
  "message": "string", // 合并操作的响应消息。
  "sha": "string" // 合并提交的哈希值。
}
```
## 请求示例

### cURL 示例

```bash
curl -X PUT \
  "${CNB_API_ENDPOINT}/{repo}/-/pulls/{number}/merge" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-H "Content-Type: application/json" \
  -d '{
  "commit_message": "string",
  "commit_title": "string",
  "merge_style": "string"
}'
```
