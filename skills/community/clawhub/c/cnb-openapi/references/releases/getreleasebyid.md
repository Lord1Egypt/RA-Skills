# GetReleaseByID

## 原始 Swagger
https://api.cnb.cool/#/operations/GetReleaseByID

## 接口描述
根据 id	查询指定 release, 包含附件信息。Get a release by id, include assets information.
## 接口权限
repo-code:r
## 请求信息

**请求方法：** GET

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
## 响应信息


**响应类型：** api.Release

**响应结构：**
```json
{
  "assets": [{
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
  }], // 附件列表。
  "author": {
    "avatar": "string", // 用户头像。
    "email": "string", // 用户邮箱。
    "freeze": false, // 是否冻结。
    "is_npc": false, // 是否是 NPC。
    "nickname": "string", // 昵称。
    "username": "string" // 用户名。
  }, // 作者信息。
  "body": "string", // 版本描述。
  "created_at": "string", // 创建时间。
  "draft": false, // 是否为草稿版本。
  "id": "string", // 版本唯一标识符。
  "is_latest": false, // 是否为最新版本。
  "name": "string", // 版本标题。
  "prerelease": false, // 是否为预发布版本。
  "published_at": "string", // 版本发布时间。
  "tag_commitish": "string", // 标签与提交标识符。
  "tag_name": "string", // 标签名称。
  "updated_at": "string" // 更新时间。
}
```
## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/{repo}/-/releases/{release_id}" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
```
