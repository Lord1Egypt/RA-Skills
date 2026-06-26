# BuildLogsDelete

## 原始 Swagger
https://api.cnb.cool/#/operations/BuildLogsDelete

## 接口描述
删除流水线日志内容。Delete pipeline logs content.
## 接口权限
repo-cnb-trigger:rw
## 请求信息

**请求方法：** DELETE

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/build/logs/{sn}

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| repo | 字符串 | 是 | Repo path|
| sn | 字符串 | 是 | Sn|
## 响应信息


**响应类型：** dto.BuildCommonResult

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
curl -X DELETE \
  "${CNB_API_ENDPOINT}/{repo}/-/build/logs/{sn}" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
```
