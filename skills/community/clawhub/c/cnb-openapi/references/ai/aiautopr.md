# AiAutoPr

## 原始 Swagger
https://api.cnb.cool/#/operations/AiAutoPr

## 接口描述
根据传入的需求内容和需求标题借助 AI 自动编码并提 PR。Automatically code and create a PR with AI based on the input requirement content and title.
## 接口权限
repo-code:rw
## 请求信息

**请求方法：** POST

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/build/ai/auto-pr

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
  "body": "string", // 需求内容
  "branch": "string", // 基于该分支编码并提交代码到随机分支，然后将随机分支提 PR 到该分支
  "source": "string", // 需求来源，默认为 issue，其他来源的需求可写上，会出现在代码提交日志的描述信息里
  "title": "string", // 需求标题
  "url": "string" // 需求来源 URL 地址
}
```
## 响应信息


**响应类型：** dto.AiAutoPrResult

**响应结构：**
```json
{
  "buildLogUrl": "string", // 构建链接
  "message": "string", // message
  "sn": "string" // 构建号
}
```
## 请求示例

### cURL 示例

```bash
curl -X POST \
  "${CNB_API_ENDPOINT}/{repo}/-/build/ai/auto-pr" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-H "Content-Type: application/json" \
  -d '{
  "body": "string",
  "branch": "string",
  "source": "string",
  "title": "string",
  "url": "string"
}'
```
