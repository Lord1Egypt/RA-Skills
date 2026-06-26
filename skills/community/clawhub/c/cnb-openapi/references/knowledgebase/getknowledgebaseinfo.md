# GetKnowledgeBaseInfo

## 原始 Swagger
https://api.cnb.cool/#/operations/GetKnowledgeBaseInfo

## 接口描述
获取知识库信息
## 接口权限
repo-code:r
## 请求信息

**请求方法：** GET

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/knowledge/base

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| repo | 字符串 | 是 | repo|
## 响应信息


**响应类型：** dto.KnowledgeBaseInfoRes

**响应结构：**
```json
{
  "embedding_model": {
    "dimension": 0,
    "name": "string"
  },
  "exclude": "string",
  "id": "string",
  "include": "string",
  "issue_last_sync_time": "string",
  "issue_sync_enabled": false,
  "last_commit_sha": "string",
  "metadata": {
    "issue": {
      "labels": "string", // 逗号分隔的标签字符串，如 "bug,feature"
      "state": "string" // "open", "closed"
    },
    "processing": {
      "chunk_overlap": 0,
      "chunk_size": 0,
      "text_separator": "string"
    },
    "version": "string"
  },
  "statistics": {
    "count": 0,
    "size": 0
  }
}
```
## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/{repo}/-/knowledge/base" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
```
