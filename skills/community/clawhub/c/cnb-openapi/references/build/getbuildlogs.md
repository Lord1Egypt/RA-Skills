# GetBuildLogs

## 原始 Swagger
https://api.cnb.cool/#/operations/GetBuildLogs

## 接口描述
查询流水线构建列表。List pipeline builds.
## 接口权限
repo-cnb-trigger:r
## 请求信息

**请求方法：** GET

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/build/logs

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| repo | 字符串 | 是 | Repo path|

### 查询参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| createTime | 字符串 | 否| Start date in "YYYY-MM-DD" format, e.g. "2024-12-01"|
| endTime | 字符串 | 否| End date in "YYYY-MM-DD" format, e.g. "2024-12-01"|
| event | 字符串 | 否| Event name, e.g. "push"|
| page | 整数 | 否| Pagination page number, default(1)|
| page_size | 整数 | 否| Pagination page size, default(30), max(100)|
| sha | 字符串 | 否| Commit ID, e.g. "2221d4535ec0c921bcd0858627c5025a871dd2b5"|
| sn | 字符串 | 否| Build SN, e.g. "cnb-1qa-1i3f5ecau|
| sourceRef | 字符串 | 否| Source branch name, e.g. "dev"|
| status | 字符串 | 否| Build status: "pending", "success", "error", "cancel"|
| targetRef | 字符串 | 否| Target branch name, e.g. "main"|
| userId | 字符串 | 否| User ID|
| userName | 字符串 | 否| Username|
## 响应信息


**响应类型：** dto.BuildLogsResult

**响应结构：**
```json
{
  "data": [{
    "buildLogUrl": "string", // 构建日志 url
    "commitTitle": "string", // 提交日志 title
    "createTime": "string", // 构建开始时间
    "duration": 0, // 构建耗时，单位：ms
    "event": "string", // 事件名
    "eventUrl": "string", // 事件 url
    "freeze": false, // 构建用户是否被冻结
    "groupName": "string", // 组织名
    "labels": "string", // 流水线标签
    "nickName": "string", // 构建用户昵称
    "pipelineFailCount": 0, // 失败的子流水线个数
    "pipelineSuccessCount": 0, // 成功的子流水线个数
    "pipelineTotalCount": 0, // 子流水线个数
    "sha": "string", // commitid
    "slug": "string", // 仓库路径
    "sn": "string", // 构建号
    "sourceRef": "string", // 源分支名
    "sourceSlug": "string", // 源仓库路径
    "status": "string", // 构建状态
    "targetRef": "string", // 目标分支名
    "title": "string", // 构建 title
    "userName": "string" // 用户名
  }], // 构建数据列表
  "init": false, // 当前仓库是否已经有构建记录，1 表示有构建记录，0 表示没有构建记录
  "timestamp": 0, // 当前时间戳
  "total": 0 // 总数
}
```
## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/{repo}/-/build/logs" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-G \
-d "createTime=<createTime>" \
-d "endTime=<endTime>" \
-d "event=<event>" \
-d "page=<page>" \
-d "page_size=<page_size>" \
-d "sha=<sha>" \
-d "sn=<sn>" \
-d "sourceRef=<sourceRef>" \
-d "status=<status>" \
-d "targetRef=<targetRef>" \
-d "userId=<userId>" \
-d "userName=<userName>" \
```
