# PostCommitAssetUploadConfirmation

## 原始 Swagger
https://api.cnb.cool/#/operations/PostCommitAssetUploadConfirmation

## 接口描述
确认 commit 附件上传完成。Confirm commit asset upload.
## 接口权限
repo-code:rw
## 请求信息

**请求方法：** POST

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/git/commit-assets/{sha1}/asset-upload-confirmation/{upload_token}/{asset_path}

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| repo | 字符串 | 是 | 不带.git后缀的仓库名称。格式：`组织名称/仓库名称`|
| sha1 | 字符串 | 是 | 提交的哈希值。|
| upload_token | 字符串 | 是 | PostCommitAssetUploadURL接口返回值verify_url字段提取的upload_token。|
| asset_path | 字符串 | 是 | PostCommitAssetUploadURL接口返回值verify_url字段提取的asset_path。|

### 查询参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| ttl | 整数 | 否| 附件保持的天数。0 表示永久，最大不能超过 180 天|
## 响应信息


**响应类型：** 无特定格式
## 请求示例

### cURL 示例

```bash
curl -X POST \
  "${CNB_API_ENDPOINT}/{repo}/-/git/commit-assets/{sha1}/asset-upload-confirmation/{upload_token}/{asset_path}" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-G \
-d "ttl=<ttl>" \
```
