# PostLabel

## 原始 Swagger
https://api.cnb.cool/#/operations/PostLabel

## 接口描述
创建一个 标签。Create a label.
## 接口权限
repo-notes:rw
## 请求信息

**请求方法：** POST

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/labels

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| repo | 字符串 | 是 | repo|

### 请求体参数


**请求体结构：**

```json
{
  "color": "string", // The hexadecimal color code for the label, without the leading `#`.
  "description": "string",
  "name": "string"
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
curl -X POST \
  "${CNB_API_ENDPOINT}/{repo}/-/labels" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-H "Content-Type: application/json" \
  -d '{
  "color": "string",
  "description": "string",
  "name": "string"
}'
```
