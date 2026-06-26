# UpdateOutsideCollaborators

## 原始 Swagger
https://api.cnb.cool/#/operations/UpdateOutsideCollaborators

## 接口描述
更新指定仓库的外部贡献者权限信息。 Update permission information for external contributors in specified repository.
## 接口权限
repo-manage:rw
## 请求信息

**请求方法：** PUT

**请求地址：** ${CNB_API_ENDPOINT}/{slug}/-/outside-collaborators/{username}

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| slug | 字符串 | 是 | slug|
| username | 字符串 | 是 | username|

### 查询参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| role | 字符串 | 是| Role|
## 响应信息


**响应类型：** 无特定格式
## 请求示例

### cURL 示例

```bash
curl -X PUT \
  "${CNB_API_ENDPOINT}/{slug}/-/outside-collaborators/{username}" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-G \
-d "role=<role>" \
```
