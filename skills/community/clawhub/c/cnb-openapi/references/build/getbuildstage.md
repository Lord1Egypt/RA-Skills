# GetBuildStage

## 原始 Swagger
https://api.cnb.cool/#/operations/GetBuildStage

## 接口描述
查询流水线Stage详情。Get pipeline build stage detail.
## 接口权限
repo-cnb-trigger:r
## 请求信息

**请求方法：** GET

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/build/logs/stage/{sn}/{pipelineId}/{stageId}

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| repo | 字符串 | 是 | Repo path|
| sn | 字符串 | 是 | SN|
| pipelineId | 字符串 | 是 | PipelineId|
| stageId | 字符串 | 是 | stageId|
## 响应信息


**响应类型：** dto.BuildStageResult

**响应结构：**
```json
{
  "content": ["string"], // stage 日志内容，数组格式，一个元素表示一行日志
  "duration": 0, // stage 耗时，单位：ms
  "endTime": 0, // stage 结束时间
  "error": "string", // stage 错误信息
  "id": "string", // stage id
  "name": "string", // stage 名称
  "startTime": 0, // stage 开始时间
  "status": "string" // stage 状态:  "pending", "start", "success", "error", "cancel", "skipped"
}
```
## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/{repo}/-/build/logs/stage/{sn}/{pipelineId}/{stageId}" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
```
