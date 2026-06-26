# UpdateUserInfo

## 原始 Swagger
https://api.cnb.cool/#/operations/UpdateUserInfo

## 接口描述
更新指定用户的详情信息。Updates the specified user's profile information.
## 接口权限
account-profile:rw
## 请求信息

**请求方法：** POST

**请求地址：** ${CNB_API_ENDPOINT}/user

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 请求体参数


**请求体结构：**

```json
{
  "address": "string",
  "bio": "string",
  "company": "string",
  "location": "string",
  "name": "string",
  "nickname": "string",
  "readme_repo_id": 0,
  "readme_repo_path": "string",
  "site": "string",
  "wechat_mp": "string",
  "wechat_mp_qrcode": "string"
}
```
## 响应信息


**响应类型：** 无特定格式
## 请求示例

### cURL 示例

```bash
curl -X POST \
  "${CNB_API_ENDPOINT}/user" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-H "Content-Type: application/json" \
  -d '{
  "address": "string",
  "bio": "string",
  "company": "string",
  "location": "string",
  "name": "string",
  "nickname": "string",
  "readme_repo_id": 0,
  "readme_repo_path": "string",
  "site": "string",
  "wechat_mp": "string",
  "wechat_mp_qrcode": "string"
}'
```
