# GetTagAnnotations

## 原始 Swagger
https://api.cnb.cool/#/operations/GetTagAnnotations

## 接口描述
查询指定 tag 的元数据。Query the metadata of the specified tag.
## 接口权限
repo-contents:r
## 请求信息

**请求方法：** GET

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/git/tag-annotations/{tag}

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| repo | 字符串 | 是 | 不带.git后缀的仓库名称。格式：`组织名称/仓库名称`|
| tag | 字符串 | 是 | 标签名称。示例：`v1.0.0`|
## 响应信息


**响应类型：** 数组[web.TagAnnotation]

**响应结构（数组元素）：**
```json
[
{
    "key": "string", // 元数据键名。
    "meta": {}, // 元数据信息，用于记录标签元数据的更新操作信息，包括操作者、操作时间、平台来源等审计信息。
    "value": "string" // 元数据值。
  }
]
```
## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/{repo}/-/git/tag-annotations/{tag}" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
```
