# ListGroups

## 原始 Swagger
https://api.cnb.cool/#/operations/ListGroups

## 接口描述
查询当前用户在指定组织下拥有指定权限的子组织列表。Get the list of sub-organizations that the current user has access to in the specified organization.
## 接口权限
account-engage:r
## 请求信息

**请求方法：** GET

**请求地址：** ${CNB_API_ENDPOINT}/user/groups/{slug}

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| slug | 字符串 | 是 | Group slug|

### 查询参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| page | 整数 | 否| Pagination page number|
| page_size | 整数 | 否| Pagination page size|
| access | 整数 | 否| access level|
## 响应信息


**响应类型：** 数组[dto.OrganizationAccess]

**响应结构（数组元素）：**
```json
[
{
    "access_role": {
    }, // AccessRole 用户在当前资源的最大权限
    "all_member_count": 0,
    "all_sub_group_count": 0, // 下面所有层级子组织
    "all_sub_mission_count": 0, // 下面所有层级子任务
    "all_sub_registry_count": 0,
    "all_sub_repo_count": 0, // 下面所有层级子仓库
    "created_at": "string",
    "description": "string",
    "domain": "string",
    "email": "string",
    "follow_count": 0,
    "freeze": false,
    "has_sub_group": false,
    "id": "string",
    "member_count": 0,
    "name": "string",
    "path": "string",
    "pinned": false,
    "pinned_time": "string",
    "readme_repo_path": "string",
    "remark": "string",
    "site": "string",
    "sub_group_count": 0, // 下一级子组织数量
    "sub_mission_count": 0,
    "sub_registry_count": 0,
    "sub_repo_count": 0, // 下一级子仓库
    "updated_at": "string",
    "wechat_mp": "string"
  }
]
```
## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/user/groups/{slug}" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-G \
-d "page=<page>" \
-d "page_size=<page_size>" \
-d "access=<access>" \
```
