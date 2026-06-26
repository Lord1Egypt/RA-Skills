# UploadBadge

## 原始 Swagger
https://api.cnb.cool/#/operations/UploadBadge

## 接口描述
上传徽章数据。Upload badge data
## 接口权限
repo-commit-status:rw
## 请求信息

**请求方法：** POST

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/badge/upload

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| repo | 字符串 | 是 | 仓库完整路径|

### 请求体参数


**请求体结构：**

```json
{
  "key": "string", // 徽章 key。目前允许上传的 key 包括：security/tca
  "latest": false, // 是否上传 latest 徽章。默认为 false：不上传 latest，仅上传 commitid 对应的徽章；true：上传 latest 和 commitid 对应的徽章
  "link": "string", // 点击徽章右侧的跳转链接
  "message": "string", // 徽章右侧显示内容
  "sha": "string", // commit id
  "value": 0 // 徽章数值，不传默认用 message 代替
}
```
## 响应信息


**响应类型：** dto.UploadBadgeResult

**响应结构：**
```json
{
  "latest_url": "string", // latest 对应的徽章 url 地址。如果没有传 latest: true，则该字段为空字符串
  "url": "string" // commitid 对应的徽章 url 地址
}
```
## 请求示例

### cURL 示例

```bash
curl -X POST \
  "${CNB_API_ENDPOINT}/{repo}/-/badge/upload" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-H "Content-Type: application/json" \
  -d '{
  "key": "string",
  "latest": false,
  "link": "string",
  "message": "string",
  "sha": "string",
  "value": 0
}'
```
