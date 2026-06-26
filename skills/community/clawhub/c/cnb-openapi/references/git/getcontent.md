# GetContent

## 原始 Swagger
https://api.cnb.cool/#/operations/GetContent

## 接口描述
查询仓库文件列表或文件。List repository files or file.
## 接口权限
repo-code:r
## 请求信息

**请求方法：** GET

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/git/contents/{file_path}

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| repo | 字符串 | 是 | 不带.git后缀的仓库名称。格式：`组织名称/仓库名称`|
| file_path | 字符串 | 是 | 文件路径。|

### 查询参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| ref | 字符串 | 否| 提交的哈希值或分支名称。|
## 响应信息


**响应类型：** api.Content

**响应结构：**
```json
{
  "content": "string", // 当内容为text时的实际内容（base64编码）。
  "encoding": "string", // 内容编码方式，仅当内容类型为blob时有效。枚举值：`base64`
  "entries": [{
    "name": "string", // 对象名称（文件名或目录名）。
    "path": "string", // 对象在仓库中的完整路径。
    "sha": "string", // Git对象的哈希值。
    "type": "string" // 对象类型。枚举值：`tree`,`blob`,`link`,`submodule`
  }], // 子项列表，当内容类型为tree时返回，否则为空。
  "lfs_download_url": "string", // LFS对象的下载URL，仅当内容类型为lfs时有效。
  "lfs_oid": "string", // LFS对象的唯一标识符，仅当内容类型为lfs时有效。
  "lfs_size": 0, // LFS对象的大小（字节），仅当内容类型为lfs时有效。
  "name": "string", // 内容名称（文件名或目录名）。
  "path": "string", // 内容在仓库中的完整路径。
  "sha": "string", // Git对象的哈希值。
  "size": 0, // 内容大小（字节）。
  "type": "string" // 内容类型。枚举值：`tree`、`blob`、`lfs`、`empty`
}
```
## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/{repo}/-/git/contents/{file_path}" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-G \
-d "ref=<ref>" \
```
