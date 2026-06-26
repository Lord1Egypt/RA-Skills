# PostReleaseAssetUploadURL

## 原始 Swagger
https://api.cnb.cool/#/operations/PostReleaseAssetUploadURL

## 接口描述
新增一个 release 附件。Create a release asset.
## 接口权限
repo-code:rw
## 请求信息

**请求方法：** POST

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/releases/{release_id}/asset-upload-url

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| repo | 字符串 | 是 | 不带.git后缀的仓库名称。格式：`组织名称/仓库名称`|
| release_id | 字符串 | 是 | 版本唯一标识符。|

### 请求体参数


**请求体结构：**

```json
{
  "asset_name": "string", // 附件名称。
  "overwrite": false, // 是否覆盖同名附件。
  "size": 0, // 附件大小，单位为字节。
  "ttl": 0 // 附件存在时间，单位为天
}
```
## 响应信息


**响应类型：** openapi.ReleaseAssetUploadURL

**响应结构：**
```json
{
  "expires_in_sec": 0, // URL过期时间，单位为秒。
  "upload_url": "string", // 附件上传URL。
  "verify_url": "string" // 附件上传确认验证URL。
}
```
## 请求示例

### cURL 示例

```bash
curl -X POST \
  "${CNB_API_ENDPOINT}/{repo}/-/releases/{release_id}/asset-upload-url" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-H "Content-Type: application/json" \
  -d '{
  "asset_name": "string",
  "overwrite": false,
  "size": 0,
  "ttl": 0
}'
```
