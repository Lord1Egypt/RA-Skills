# GetBadge

## 原始 Swagger
https://api.cnb.cool/#/operations/GetBadge

## 接口描述
获取徽章 svg 或 JSON 数据。Get badge svg or JSON data.
## 接口权限
repo-commit-status:r
## 请求信息

**请求方法：** GET

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/badge/git/{sha}/{badge}

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| repo | 字符串 | 是 | 仓库完整路径|
| sha | 字符串 | 是 | latest 或 commit 8 位短 hash（例如 89d48c07）|
| badge | 字符串 | 是 | 徽章名，例如 pr 事件徽章名为：ci/status/pull_request, 如需获取 JSON 数据，可加上 .json 后缀，如：ci/status/pull_request.json|

### 请求体参数


**请求体结构：**

```json
{
  "branch": "string" // 分支名，例如：main。不传则为默认分支，获取默认分支最新徽章。传了分支名，则获取该分支最新提交记录对应的徽章。
}
```
## 响应信息


**响应类型：** dto.GetBadgeResult

**响应结构：**
```json
{
  "color": "string", // 徽章颜色
  "label": "string", // 徽章左侧显示内容
  "link": "string", // 徽章链接
  "links": ["string"], // 徽章链接列表
  "message": "string" // 徽章右侧显示内容
}
```
## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/{repo}/-/badge/git/{sha}/{badge}" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-H "Content-Type: application/json" \
  -d '{
  "branch": "string"
}'
```
