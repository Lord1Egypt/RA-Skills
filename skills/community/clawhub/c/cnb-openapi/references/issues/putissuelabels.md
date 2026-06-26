# PutIssueLabels

## 原始 Swagger
https://api.cnb.cool/#/operations/PutIssueLabels

## 接口描述
设置 issue 标签。 Set the new labels for an issue.
## 接口权限
repo-issue:rw
## 请求信息

**请求方法：** PUT

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/issues/{number}/labels

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| repo | 字符串 | 是 | 不带.git后缀的仓库名称。格式：`组织名称/仓库名称`|
| number | 字符串 | 是 | Issue唯一标识编号。|

### 请求体参数


**请求体结构：**

```json
{
  "labels": ["string"] // Issue标签列表，最大限制为10。示例：`["标签1","标签2"]`
}
```
## 响应信息


**响应类型：** api.Label

**响应结构：**
```json
{
  "color": "string", // 标签颜色。
  "description": "string", // 标签描述。
  "id": "string", // 标签ID。
  "name": "string" // 标签名称。
}
```
## 请求示例

### cURL 示例

```bash
curl -X PUT \
  "${CNB_API_ENDPOINT}/{repo}/-/issues/{number}/labels" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-H "Content-Type: application/json" \
  -d '{
  "labels": ["string"]
}'
```
