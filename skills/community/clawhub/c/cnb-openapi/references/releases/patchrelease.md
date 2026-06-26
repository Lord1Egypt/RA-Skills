# PatchRelease

## 原始 Swagger
https://api.cnb.cool/#/operations/PatchRelease

## 接口描述
更新 release。Update a release.
## 接口权限
repo-code:rw
## 请求信息

**请求方法：** PATCH

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/releases/{release_id}

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
  "body": "string", // 版本描述。
  "draft": false, // 是否为草稿版本。
  "make_latest": "string", // 是否设置为最新版本。可选值：`true`,`false`,`legacy`
  "name": "string", // 版本标题。
  "prerelease": false // 是否为预发布版本。
}
```
## 响应信息


**响应类型：** 无特定格式
## 请求示例

### cURL 示例

```bash
curl -X PATCH \
  "${CNB_API_ENDPOINT}/{repo}/-/releases/{release_id}" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-H "Content-Type: application/json" \
  -d '{
  "body": "string",
  "draft": false,
  "make_latest": "string",
  "name": "string",
  "prerelease": false
}'
```
