# PostPullReview

## 原始 Swagger
https://api.cnb.cool/#/operations/PostPullReview

## 接口描述
新增一次合并请求评审。Create a pull review.
## 接口权限
repo-notes:rw
## 请求信息

**请求方法：** POST

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/pulls/{number}/reviews

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| repo | 字符串 | 是 | 不带.git后缀的仓库名称。格式：`组织名称/仓库名称`|
| number | 字符串 | 是 | Pull唯一标识编号。|

### 请求体参数


**请求体结构：**

```json
{
  "body": "string", // Review的评审意见内容。
  "comments": [{
    "body": "string", // 评论内容。
    "end_line": 0, // 结束行号，subject_type=line时必填。
    "end_side": "string", // 评论结束位置的代码版本侧，subject_type=line时必填。可选值：`left`,`right`
    "path": "string", // 文件路径。示例值：`src/main.go`
    "start_line": 0, // 起始行号，subject_type=line时必填。
    "start_side": "string", // 评论起始位置的代码版本侧，subject_type=line时必填。可选值：`left`,`right`
    "subject_type": "string" // 评论对象类型，当subject_type为file时无需指定行号和侧别字段。可选值：`line`,`file`
  }], // 评审中的具体评论列表。
  "event": "string" // Review事件类型.如：`approve`,`comment`,`request_changes`,`pending`
}
```
## 响应信息


**响应类型：** 无特定格式
## 请求示例

### cURL 示例

```bash
curl -X POST \
  "${CNB_API_ENDPOINT}/{repo}/-/pulls/{number}/reviews" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-H "Content-Type: application/json" \
  -d '{
  "body": "string",
  "comments": [{
    "body": "string",
    "end_line": 0,
    "end_side": "string",
    "path": "string",
    "start_line": 0,
    "start_side": "string",
    "subject_type": "string"
  }],
  "event": "string"
}'
```
