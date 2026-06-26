# TopContributors

## 原始 Swagger
https://api.cnb.cool/#/operations/TopContributors

## 接口描述
获取仓库 top 活跃用户。List the top active users
## 接口权限
repo-base-info:r
## 请求信息

**请求方法：** GET

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/top-activity-users

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| repo | 字符串 | 是 | repo|

### 查询参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| top | 整数 | 否| 返回的用户个数|
## 响应信息


**响应类型：** 数组[dto.UsersResult]

**响应结构（数组元素）：**
```json
[
{
    "address": "string",
    "appreciate_status": 0, // 用户赞赏码状态，0-无赞赏码，1-有
    "avatar": "string",
    "bio": "string",
    "company": "string",
    "created_at": "string",
    "email": "string",
    "follow_count": 0,
    "follow_mission_count": 0,
    "follow_repo_count": 0,
    "follower_count": 0,
    "freeze": false,
    "gender": 0,
    "group_count": 0,
    "id": "string",
    "is_following": false, // 查询人是否follow了此用户
    "location": "string",
    "locked": false,
    "mission_count": 0,
    "nickname": "string",
    "public_mission_count": 0,
    "public_registry_count": 0,
    "public_repo_count": 0,
    "readme_repo_path": "string",
    "registry_count": 0,
    "repo_count": 0,
    "reward_amount": 0,
    "reward_count": 0,
    "site": "string",
    "stars_count": 0,
    "type": {
    },
    "username": "string",
    "verified": 0, // 认证类型
    "verified_expire_in": "string", // 认证过期时间
    "wechat_mp": "string",
    "wechat_mp_qrcode": "string"
  }
]
```
## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/{repo}/-/top-activity-users" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-G \
-d "top=<top>" \
```
