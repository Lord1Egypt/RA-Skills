# ListPullFiles

## 原始 Swagger
https://api.cnb.cool/#/operations/ListPullFiles

## 接口描述
查询指定合并请求的文件列表。Lists the files in a specified pull request.
## 接口权限
repo-pr:r
## 请求信息

**请求方法：** GET

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/pulls/{number}/files

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| repo | 字符串 | 是 | 不带.git后缀的仓库名称。格式：`组织名称/仓库名称`|
| number | 字符串 | 是 | Pull唯一标识编号。|
## 响应信息


**响应类型：** 数组[api.PullFile]

**响应结构（数组元素）：**
```json
[
{
    "additions": 0, // 新增行数。
    "blob_url": "string", // 文件的Blob对象访问地址。
    "contents_url": "string", // 文件内容访问地址。
    "deletions": 0, // 删除行数。
    "filename": "string", // 文件名称。
    "patch": "string", // 文件的差异补丁内容。
    "raw_url": "string", // 文件的原始内容访问地址。
    "sha": "string", // 文件的提交哈希值。
    "status": "string" // 文件更改状态。枚举值：`add`,`modify`,`delete`,`rename`,`copy`
  }
]
```
## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/{repo}/-/pulls/{number}/files" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
```
