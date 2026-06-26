# GetMemberAccessLevelOfRepo

## 原始 Swagger
https://api.cnb.cool/#/operations/GetMemberAccessLevelOfRepo

## 接口描述
获取指定仓库内, 访问成员在当前层级内的权限信息。Get permission information for accessing members at current level.
## 接口权限
repo-manage:r
## 请求信息

**请求方法：** GET

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/members/access-level

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| repo | 字符串 | 是 | slug|

### 查询参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| include_inherit | 布尔值 | 否| 是否包含继承的权限。If inherited permissions are included.|
## 响应信息


**响应类型：** dto.MemberAccessLevelInSlugUnion

**响应结构：**
```json
{
  "access_level": {
  },
  "inherit": false,
  "read_privilege": false,
  "write_privilege": false
}
```
## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/{repo}/-/members/access-level" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-G \
-d "include_inherit=<include_inherit>" \
```
