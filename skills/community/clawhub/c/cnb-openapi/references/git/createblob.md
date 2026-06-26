# CreateBlob

## 原始 Swagger
https://api.cnb.cool/#/operations/CreateBlob

## 接口描述
创建一个 blob。Create a blob.
## 接口权限
repo-code:rw
## 请求信息

**请求方法：** POST

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/git/blobs

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| repo | 字符串 | 是 | 不带.git后缀的仓库名称。格式：`组织名称/仓库名称`|

### 请求体参数


**请求体结构：**

```json
{
  "content": "string", // Blob的内容。
  "encoding": "string" // 内容的编码格式。可选值：`utf-8`,`base64`
}
```
## 响应信息


**响应类型：** api.Blob

**响应结构：**
```json
{
  "sha": "string" // 提交的哈希值。
}
```
## 请求示例

### cURL 示例

```bash
curl -X POST \
  "${CNB_API_ENDPOINT}/{repo}/-/git/blobs" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-H "Content-Type: application/json" \
  -d '{
  "content": "string",
  "encoding": "string"
}'
```
