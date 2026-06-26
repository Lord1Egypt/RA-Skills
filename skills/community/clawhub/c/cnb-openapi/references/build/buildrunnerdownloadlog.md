# BuildRunnerDownloadLog

## 原始 Swagger
https://api.cnb.cool/#/operations/BuildRunnerDownloadLog

## 接口描述
流水线runner日志下载。Pipeline runner log download.
## 接口权限
repo-cnb-trigger:r
## 请求信息

**请求方法：** GET

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/build/runner/download/log/{pipelineId}

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| repo | 字符串 | 是 | Repo path|
| pipelineId | 字符串 | 是 | PipelineId|
## 响应信息


**响应类型：** 无特定格式
## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/{repo}/-/build/runner/download/log/{pipelineId}" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
```
