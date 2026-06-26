# GetReleaseAsset

## 原始 Swagger
https://api.cnb.cool/#/operations/GetReleaseAsset

## 接口描述
查询指定的 release 附件 the specified release asset.
## 接口权限
repo-code:r
## 请求信息

**请求方法：** GET

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/releases/{release_id}/assets/{asset_id}

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
| asset_id | 字符串 | 是 | 附件唯一标识符。|
## 响应信息


**响应类型：** api.ReleaseAsset

**响应结构：**
```json
{
  "brower_download_url": "string", // 浏览器下载URL（通过主域名，用于用户直接访问）。
  "content_type": "string", // 附件内容类型。
  "created_at": "string", // 创建时间。
  "download_count": 0, // 下载次数。
  "hash_algo": "string", // 附件哈希算法。
  "hash_value": "string", // 附件哈希值。
  "id": "string", // 附件唯一标识符。
  "name": "string", // 附件名称。
  "path": "string", // 附件路径。
  "size": 0, // 附件大小（字节）。
  "updated_at": "string", // 更新时间。
  "uploader": {
    "avatar": "string", // 用户头像。
    "email": "string", // 用户邮箱。
    "freeze": false, // 是否冻结。
    "is_npc": false, // 是否是 NPC。
    "nickname": "string", // 昵称。
    "username": "string" // 用户名。
  }, // 附件上传者信息。
  "url": "string" // API下载URL（通过API域名，用于程序化下载）。
}
```
## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/{repo}/-/releases/{release_id}/assets/{asset_id}" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
```
