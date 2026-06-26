# PutTagAnnotations

## 原始 Swagger
https://api.cnb.cool/#/operations/PutTagAnnotations

## 接口描述
设定指定 tag 的元数据。Set the metadata of the specified tag.
## 接口权限
repo-contents:rw
## 请求信息

**请求方法：** PUT

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

### 请求体参数


**请求体结构：**

```json
{
  "annotations": [{
    "key": "string", // 标签元数据的键名。
    "value": "string" // 标签元数据的值。
  }] // 设置tag元数据列表信息。
}
```
## 响应信息


**响应类型：** 无特定格式
## 请求示例

### cURL 示例

```bash
curl -X PUT \
  "${CNB_API_ENDPOINT}/{repo}/-/git/tag-annotations/{tag}" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-H "Content-Type: application/json" \
  -d '{
  "annotations": [{
    "key": "string",
    "value": "string"
  }]
}'
```
