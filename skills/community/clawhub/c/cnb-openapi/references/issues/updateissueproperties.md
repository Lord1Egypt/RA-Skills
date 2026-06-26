# UpdateIssueProperties

## 原始 Swagger
https://api.cnb.cool/#/operations/UpdateIssueProperties

## 接口描述
批量更新Issue自定义属性值
## 接口权限
repo-issue:rw
## 请求信息

**请求方法：** PATCH

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/issues/{number}/property

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| repo | 字符串 | 是 | 不带.git后缀的仓库名称。格式：`组织名称/仓库名称`|
| number | 字符串 | 是 | Issue唯一标识编号。|

### 请求体参数


**请求体结构：**

```json
{
  "properties": [{
    "key": "string", // Issue自定义属性键名。
    "value": "string" // Issue自定义属性值。
  }] // Issue自定义属性列表。
}
```
## 响应信息


**响应类型：** api.IssuePropertyUpdateResult

**响应结构：**
```json
{
  "failed_count": 0, // 更新失败的属性数量
  "failed_keys": ["string"], // 更新失败的属性key列表，仅当存在失败时返回
  "success_count": 0 // 更新成功的属性数量
}
```
## 请求示例

### cURL 示例

```bash
curl -X PATCH \
  "${CNB_API_ENDPOINT}/{repo}/-/issues/{number}/property" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-H "Content-Type: application/json" \
  -d '{
  "properties": [{
    "key": "string",
    "value": "string"
  }]
}'
```
