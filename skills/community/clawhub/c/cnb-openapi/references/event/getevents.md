# GetEvents

## 原始 Swagger
https://api.cnb.cool/#/operations/GetEvents

## 接口描述
获取仓库动态预签名地址，并返回内容。Get events pre-signed URL and return content.## 请求信息

**请求方法：** GET

**请求地址：** ${CNB_API_ENDPOINT}/events/{repo}/-/{date}

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| repo | 字符串 | 是 | repo path|
| date | 字符串 | 是 | 动态日期,支持按天或小时为维度获取,格式为yy-mm-dd-h or yy-mm-dd, eg:2025-09-11-5|
## 响应信息


**响应类型：** 无特定格式
## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/events/{repo}/-/{date}" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
```
