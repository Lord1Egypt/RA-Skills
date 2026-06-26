# ListMemberAccessLevelOfGroup

## 原始 Swagger
https://api.cnb.cool/#/operations/ListMemberAccessLevelOfGroup

## 接口描述
获取指定组织内指定成员的权限信息, 结果按组织层级来展示, 包含上层组织的权限继承信息。Get specified member's permissions with organizational hierarchy.
## 接口权限
group-manage:r
## 请求信息

**请求方法：** GET

**请求地址：** ${CNB_API_ENDPOINT}/{group}/-/members/{username}/access-level

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| group | 字符串 | 是 | slug|
| username | 字符串 | 是 | username|
## 响应信息


**响应类型：** 数组[dto.MemberAccessLevel]

**响应结构（数组元素）：**
```json
[
{
    "access_level": {
    },
    "path": "string"
  }
]
```
## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/{group}/-/members/{username}/access-level" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
```
