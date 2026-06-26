# StartWorkspace

## 原始 Swagger
https://api.cnb.cool/#/operations/StartWorkspace

## 接口描述
启动云原生开发环境，已存在环境则直接打开，否则重新创建开发环境。Start cloud-native dev. Opens existing env or creates a new one.
## 接口权限
repo-cnb-trigger:rw
## 请求信息

**请求方法：** POST

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/workspace/start

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
  "branch": "string", // 分支名或 tag 名，例如：main 或 v1.0.0。
  "ref": "string" // Git ref，例如，refs/heads/main 或 refs/tags/v1.0.0。不传 ref 时默认基于分支启动
}
```
## 响应信息


**响应类型：** dto.StartWorkspaceResult

**响应结构：**
```json
{
  "buildLogUrl": "string", // 仅新创建开发环境时返回，表示创建开发环境的流水线日志地址
  "message": "string", // 仅新创建开发环境时返回，表示创建开发环境的提示信息
  "sn": "string", // 仅新创建开发环境时返回，表示创建开发环境的流水线 sn
  "url": "string" // 如果存在开发环境，则返回 WebIDE 访问 url；如果不存在开发环境，则返回启动云原生开发的 loading 页面 url 地址
}
```
## 请求示例

### cURL 示例

```bash
curl -X POST \
  "${CNB_API_ENDPOINT}/{repo}/-/workspace/start" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-H "Content-Type: application/json" \
  -d '{
  "branch": "string",
  "ref": "string"
}'
```
