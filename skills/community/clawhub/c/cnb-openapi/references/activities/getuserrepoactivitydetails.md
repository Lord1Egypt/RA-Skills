# GetUserRepoActivityDetails

## 原始 Swagger
https://api.cnb.cool/#/operations/GetUserRepoActivityDetails

## 接口描述
个人仓库动态详情列表。List of personal repository activity details.
## 接口权限
account-engage:r
## 请求信息

**请求方法：** GET

**请求地址：** ${CNB_API_ENDPOINT}/users/{username}/repo-activities/{activityType}

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| username | 字符串 | 是 | UserName|
| activityType | 字符串 | 是 | activity type|

### 查询参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| slug | 字符串 | 是| 仓库路径|
| date | 字符串 | 是| 查询日期，格式 yyyyMM，或者 yyyyMMdd|
## 响应信息


**响应类型：** 数组[interface{}]## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/users/{username}/repo-activities/{activityType}" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-G \
-d "slug=<slug>" \
-d "date=<date>" \
```
