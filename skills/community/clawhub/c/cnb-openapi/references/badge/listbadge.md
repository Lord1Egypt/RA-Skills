# ListBadge

## 原始 Swagger
https://api.cnb.cool/#/operations/ListBadge

## 接口描述
获取徽章列表数据。List badge data
## 接口权限
repo-commit-status:r
## 请求信息

**请求方法：** GET

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/badge/list

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| repo | 字符串 | 是 | 仓库完整路径|

### 请求体参数


**请求体结构：**

```json
{
}
```
## 响应信息


**响应类型：** dto.ListBadgeResult

**响应结构：**
```json
{
  "badges": [{
    "desc": "string", // 徽章描述
    "group": {
      "status": "string", // 徽章分组状态
      "type": "string", // 徽章分组类型
      "typeEn": "string" // 徽章分组英文类型
    }, // 徽章分组
    "link": "string", // 徽章链接
    "name": "string", // 徽章名称
    "type": "string", // 徽章类型
    "url": "string" // 徽章URL
  }] // 徽章列表
}
```
## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/{repo}/-/badge/list" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-H "Content-Type: application/json" \
  -d '{
}'
```
