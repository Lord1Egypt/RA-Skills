# AiChatCompletions

## 原始 Swagger
https://api.cnb.cool/#/operations/AiChatCompletions

## 接口描述
AI 对话。调用者需有代码写权限（CNB_TOKEN 仅需读权限，部署令牌不检查读写权限）。AI chat completions. Requires caller to have repo write permission.
## 接口权限
repo-code:r
## 请求信息

**请求方法：** POST

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/ai/chat/completions

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
  "messages": [{
    "content": "string", // 内容
    "role": "string" // 角色，可选值：user、assistant
  }], // 对话内容
  "model": "string", // 模型名称
  "stream": false // 是否流式返回结果，部分模型可能不支持非流式
}
```
## 响应信息


**响应类型：** dto.AiChatCompletionsResult

**响应结构：**
```json
{
  "choices": [{
    "finish_reason": "string", // 结束原因
    "index": 0, // 索引
    "message": {
      "content": "string", // 内容
      "role": "string" // 角色，可选值：user、assistant
    } // 消息
  }], // 选择
  "created": 0, // 创建时间
  "id": "string", // ID
  "model": "string", // 模型
  "object": "string" // 对象
}
```
## 请求示例

### cURL 示例

```bash
curl -X POST \
  "${CNB_API_ENDPOINT}/{repo}/-/ai/chat/completions" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-H "Content-Type: application/json" \
  -d '{
  "messages": [{
    "content": "string",
    "role": "string"
  }],
  "model": "string",
  "stream": false
}'
```
