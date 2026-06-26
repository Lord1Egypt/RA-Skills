# GetPullRequestSettings

## 原始 Swagger
https://api.cnb.cool/#/operations/GetPullRequestSettings

## 接口描述
查询仓库合并请求设置。List pull request settings.
## 接口权限
repo-manage:r
## 请求信息

**请求方法：** GET

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/settings/pull-request

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| repo | 字符串 | 是 | 不带.git后缀的仓库名称。格式：`组织名称/仓库名称`|
## 响应信息


**响应类型：** api.PullRequestSettings

**响应结构：**
```json
{
  "allow_merge_commit_merge": false, // 是否允许直接提交合并。
  "allow_rebase_merge": false, // 是否允许变基合并。
  "allow_squash_merge": false, // 是否允许压缩合并。
  "master_auto_as_reviewer": false, // 是否允许自动添加仓库管理员为评审者。
  "merge_commit_message_style": "string", // 直接提交合并操作时默认生成的提交信息内容。可选值：`default`,`pull_request_title`,`pull_request_title_with_body`
  "squash_commit_message_style": "string" // 压缩合并操作时默认生成的提交信息内容。可选值：`default`,`pull_request_title`,`pull_request_title_with_body`
}
```
## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/{repo}/-/settings/pull-request" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
```
