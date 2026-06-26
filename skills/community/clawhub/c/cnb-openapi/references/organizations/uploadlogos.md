# UploadLogos

## 原始 Swagger
https://api.cnb.cool/#/operations/UploadLogos

## 接口描述
发起一个上传 logo 的请求，返回上传文件的url，请使用 put 发起流式上传。Initiate a request to upload logo,returns upload URL.Use PUT to initiate a stream upload.
## 接口权限
group-manage:rw
## 请求信息

**请求方法：** POST

**请求地址：** ${CNB_API_ENDPOINT}/{group}/-/upload/logos

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| group | 字符串 | 是 | group|

### 请求体参数


**请求体结构：**

```json
{
  "ext": {}, // 文件扩展信息。
  "name": "string", // 文件名。
  "size": 0 // 文件大小。
}
```
## 响应信息


**响应类型：** dto.UploadAssetsResponse

**响应结构：**
```json
{
  "assets": {
    "content_type": "string", // 资源内容类型。
    "ext": {}, // 文件扩展信息。
    "name": "string", // 文件名。
    "path": "string", // 资源路径。
    "size": 0 // 文件大小。
  }, // 资源信息。
  "form": {}, // 上传表单参数。
  "token": "string", // 后续调用 confirm 接口用的。
  "upload_url": "string" // 上传URL地址。
}
```
## 请求示例

### cURL 示例

```bash
curl -X POST \
  "${CNB_API_ENDPOINT}/{group}/-/upload/logos" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-H "Content-Type: application/json" \
  -d '{
  "ext": {},
  "name": "string",
  "size": 0
}'
```
