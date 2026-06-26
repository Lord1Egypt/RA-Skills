# CreateRepo

## 原始 Swagger
https://api.cnb.cool/#/operations/CreateRepo

## 接口描述
创建仓库。Create repositories.
## 接口权限
group-resource:rw
## 请求信息

**请求方法：** POST

**请求地址：** ${CNB_API_ENDPOINT}/{slug}/-/repos

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| slug | 字符串 | 是 | Group slug|

### 请求体参数


**请求体结构：**

```json
{
  "description": "string",
  "license": "string",
  "name": "string",
  "visibility": "string"
}
```
## 响应信息


**响应类型：** 无特定格式
## 请求示例

### cURL 示例

```bash
curl -X POST \
  "${CNB_API_ENDPOINT}/{slug}/-/repos" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-H "Content-Type: application/json" \
  -d '{
  "description": "string",
  "license": "string",
  "name": "string",
  "visibility": "string"
}'
```
