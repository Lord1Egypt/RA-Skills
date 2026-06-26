# ListAssets

## 原始 Swagger
https://api.cnb.cool/#/operations/ListAssets

## 接口描述
仓库的 asset 记录列表
## 接口权限
repo-manage:r
## 请求信息

**请求方法：** GET

**请求地址：** ${CNB_API_ENDPOINT}/{slug}/-/list-assets

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| slug | 字符串 | 是 | slug|

### 查询参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| page | 整数 | 否| 第几页，从1开始|
| page_size | 整数 | 否| 每页多少条数据|
## 响应信息


**响应类型：** 数组[dto.AssetRecords]

**响应结构（数组元素）：**
```json
[
{
    "created_at": "string",
    "id": "string",
    "origin_path": "string", // 来源地址，例如 release 附件的来源地址是对应的 release 页面。issue和pr文件没有。
    "path": "string",
    "record_type": {
    }, // 资源类型，slug_img和slug_file可调用DeleteAsset接口直接删除该资源，repo_release和repo_commit则不行
    "referer": "string",
    "size_in_byte": 0
  }
]
```
## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/{slug}/-/list-assets" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-G \
-d "page=<page>" \
-d "page_size=<page_size>" \
```
