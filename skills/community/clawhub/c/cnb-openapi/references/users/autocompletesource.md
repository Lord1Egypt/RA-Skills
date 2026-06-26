# AutoCompleteSource

## 原始 Swagger
https://api.cnb.cool/#/operations/AutoCompleteSource

## 接口描述
查询当前用户用户拥有指定权限的所有资源列表。List resources that the current user has specified permissions for.
## 接口权限
account-engage:r
## 请求信息

**请求方法：** GET

**请求地址：** ${CNB_API_ENDPOINT}/user/autocomplete_source

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 查询参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| source_type | 字符串 | 否| Source type|
| page | 整数 | 否| Pagination page number|
| page_size | 整数 | 否| Pagination page size|
| search | 字符串 | 否| Filter by resources.|
| access | 字符串 | 否| 最小仓库权限，默认owner。Minima repository permissions|
| order_by | 字符串 | 否| Order field|
| desc | 布尔值 | 否| 排序顺序。Ordering.|
## 响应信息


**响应类型：** 数组[字符串]## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/user/autocomplete_source" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-G \
-d "source_type=<source_type>" \
-d "page=<page>" \
-d "page_size=<page_size>" \
-d "search=<search>" \
-d "access=<access>" \
-d "order_by=<order_by>" \
-d "desc=<desc>" \
```
