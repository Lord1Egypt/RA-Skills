# AddMembersOfRegistry

## 原始 Swagger
https://api.cnb.cool/#/operations/AddMembersOfRegistry

## 接口描述
添加成员。Add members.
## 接口权限
registry-manage:rw
## 请求信息

**请求方法：** POST

**请求地址：** ${CNB_API_ENDPOINT}/{registry}/-/members/{username}

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| registry | 字符串 | 是 | slug|
| username | 字符串 | 是 | username|

### 请求体参数


**请求体结构：**

```json
{
  "access_level": "string",
  "is_outside_collaborator": false
}
```
## 响应信息


**响应类型：** 无特定格式
## 请求示例

### cURL 示例

```bash
curl -X POST \
  "${CNB_API_ENDPOINT}/{registry}/-/members/{username}" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-H "Content-Type: application/json" \
  -d '{
  "access_level": "string",
  "is_outside_collaborator": false
}'
```
