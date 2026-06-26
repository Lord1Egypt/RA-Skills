# StartBuild

## 原始 Swagger
https://api.cnb.cool/#/operations/StartBuild

## 接口描述
开始一个构建。Start a build.
## 接口权限
repo-cnb-trigger:rw
## 请求信息

**请求方法：** POST

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/build/start

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| repo | 字符串 | 是 | repo|

### 请求体参数


**请求体结构：**

```json
{
  "branch": "string", // 触发分支，默认为主分支
  "config": "string", // 指定配置文件内容，yaml 格式
  "env": {}, // 环境变量，对象格式
  "event": "string", // 事件名，必须是 api_trigger 或以 api_trigger_ 开头，默认为 `api_trigger`
  "sha": "string", // commit id ，优先级比 tag 高，默认为分支最新提交记录
  "sync": "string", // 是否等待构建正式触发，为false时会立刻返回 sn 和 buildLogUrl
  "tag": "string" // 触发 tag，优先级比 branch 高
}
```
## 响应信息


**响应类型：** dto.BuildResult

**响应结构：**
```json
{
  "buildLogUrl": "string", // 构建链接
  "message": "string", // 构建信息
  "sn": "string", // 构建号
  "success": false // 构建是否触发成功，不代表构建结果
}
```
## 请求示例

### cURL 示例

```bash
curl -X POST \
  "${CNB_API_ENDPOINT}/{repo}/-/build/start" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-H "Content-Type: application/json" \
  -d '{
  "branch": "string",
  "config": "string",
  "env": {},
  "event": "string",
  "sha": "string",
  "sync": "string",
  "tag": "string"
}'
```
