# DeleteTagAnnotation

## 原始 Swagger
https://api.cnb.cool/#/operations/DeleteTagAnnotation

## 接口描述
删除指定 tag 的元数据。Delete the metadata of the specified tag.
## 接口权限
repo-contents:rw
## 请求信息

**请求方法：** DELETE

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/git/tag-annotations/{tag_with_key}

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| repo | 字符串 | 是 | 不带.git后缀的仓库名称。格式：`组织名称/仓库名称`|
| tag_with_key | 字符串 | 是 | tag元数据名称。格式：`标签名称/元数据key`|
## 响应信息


**响应类型：** 无特定格式
## 请求示例

### cURL 示例

```bash
curl -X DELETE \
  "${CNB_API_ENDPOINT}/{repo}/-/git/tag-annotations/{tag_with_key}" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
```
