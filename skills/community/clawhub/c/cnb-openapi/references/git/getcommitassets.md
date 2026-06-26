# GetCommitAssets

## 原始 Swagger
https://api.cnb.cool/#/operations/GetCommitAssets

## 接口描述
发起一个获取 commits 附件的请求， 302到有一定效期的下载地址。Get a request to fetch a commit assets and returns 302 redirect to the assets URL with specific valid time.
## 接口权限
repo-contents:r
## 请求信息

**请求方法：** GET

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/commit-assets/download/{commit_id}/{filename}

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| repo | 字符串 | 是 | 不带.git后缀的仓库名称。格式：`组织名称/仓库名称`|
| commit_id | 字符串 | 是 | 提交的哈希值。|
| filename | 字符串 | 是 | 文件名称。示例：`test.png`|

### 查询参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| share | 布尔值 | 否| 是否可以下载，true表示302的下载地址有效期12小时，最多下载10次。|
## 响应信息


**响应类型：** 无特定格式
## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/{repo}/-/commit-assets/download/{commit_id}/{filename}" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-G \
-d "share=<share>" \
```
