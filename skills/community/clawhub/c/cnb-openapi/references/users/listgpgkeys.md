# ListGPGKeys

## 原始 Swagger
https://api.cnb.cool/#/operations/ListGPGKeys

## 接口描述
获取用户 GPG keys 列表。List GPG Keys.
## 接口权限
account-profile:r
## 请求信息

**请求方法：** GET

**请求地址：** ${CNB_API_ENDPOINT}/user/gpg-keys

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 查询参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| page | 整数 | 否| pagination page number|
| page_size | 整数 | 否| pagination page size|
| keyword | 字符串 | 否| gpg search key|
## 响应信息


**响应类型：** api.GPGPublicKey

**响应结构：**
```json
{
  "created_at": "string", // 主密钥添加时间
  "emails": [{
    "email": "string", // 邮箱
    "verified": false // 是否已验证
  }], // 邮箱
  "expired_at": "string", // 主密钥过期时间
  "id": "string", // 主密钥ID
  "key_id": "string", // 公钥 KeyID
  "name": "string", // 标题
  "raw_key": "string", // PGP公钥文本
  "subkeys": [{
    "created_at": "string", // 子密钥添加时间
    "expired_at": "string", // 子密钥过期时间
    "id": "string", // 子密钥ID
    "key_id": "string", // 子密钥 KeyID
    "primary_key_id": "string" // 主密钥 ID
  }] // 子密钥
}
```
## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/user/gpg-keys" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-G \
-d "page=<page>" \
-d "page_size=<page_size>" \
-d "keyword=<keyword>" \
```
