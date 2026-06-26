# GetGroup

## 原始 Swagger
https://api.cnb.cool/#/operations/GetGroup

## 接口描述
获取指定组织信息。Get information for the specified organization.
## 接口权限
group-resource:r
## 请求信息

**请求方法：** GET

**请求地址：** ${CNB_API_ENDPOINT}/{group}

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| group | 字符串 | 是 | group path|
## 响应信息


**响应类型：** dto.OrganizationAccess

**响应结构：**
```json
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
```
## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/{group}" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
```
