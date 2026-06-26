# DeleteWorkspace

## 原始 Swagger
https://api.cnb.cool/#/operations/DeleteWorkspace

## 接口描述
删除我的云原生开发环境。Delete my workspace.
## 接口权限
account-engage:rw
## 请求信息

**请求方法：** POST

**请求地址：** ${CNB_API_ENDPOINT}/workspace/delete

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 请求体参数


**请求体结构：**

```json
{
  "pipelineId": "string", // 表示要删除的开发环境流水线 id，sn 和 pipelineId 二选一，优先使用 pipelineId
  "sn": "string" // 表示要删除的开发环境流水线构建号，sn 和 pipelineId 二选一，优先使用 pipelineId
}
```
## 响应信息


**响应类型：** dto.WorkspaceDeleteResult

**响应结构：**
```json
{
  "code": 0, // 返回码，0 表示成功，1 表示失败
  "message": "string" // 描述
}
```
## 请求示例

### cURL 示例

```bash
curl -X POST \
  "${CNB_API_ENDPOINT}/workspace/delete" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-H "Content-Type: application/json" \
  -d '{
  "pipelineId": "string",
  "sn": "string"
}'
```
