# GetUserActivitiesByDate

## 原始 Swagger
https://api.cnb.cool/#/operations/GetUserActivitiesByDate

## 接口描述
获取个人动态活跃详情汇总。Get user activities by date.
## 接口权限
account-engage:r
## 请求信息

**请求方法：** GET

**请求地址：** ${CNB_API_ENDPOINT}/users/{username}/activities

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| username | 字符串 | 是 | UserName|

### 查询参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| date | 字符串 | 否| 查询日期，格式 yyyyMM，或者 yyyyMMdd|
## 响应信息


**响应类型：** dto.ActivityDate

**响应结构：**
```json
{
  "code_review_count": 0,
  "code_reviews": [{
    "detail": {
      "path": "string" // 完整仓库路径
    }, // 公仓转私仓或仓库被删除后为 null
    "exposed_repo_path": "string", // activity 发生时仓库的 path，这时的 path 是可以公开的
    "freeze": false, // 仓库是否封禁
    "repo_unaccessible": false, // 仓库是否不可访问（公仓转私仓或仓库被删除后不可访问）
    "time": 0.0,
    "visibility_level": {
    } // 仓库可见性
  }],
  "commit_count": 0,
  "commits": [{
    "detail": {
      "path": "string" // 完整仓库路径
    }, // 公仓转私仓或仓库被删除后为 null
    "exposed_repo_path": "string", // activity 发生时仓库的 path，这时的 path 是可以公开的
    "freeze": false, // 仓库是否封禁
    "repo_unaccessible": false, // 仓库是否不可访问（公仓转私仓或仓库被删除后不可访问）
    "time": 0.0,
    "visibility_level": {
    } // 仓库可见性
  }],
  "group_count": 0,
  "groups": [{
    "create_at": "string",
    "detail": {
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
    }, // 组织详情，组织被删后为 null
    "remark": "string" // 组织别名，组织被删除后才有值
  }],
  "issues": [{
    "detail": {
      "path": "string" // 完整仓库路径
    }, // 公仓转私仓或仓库被删除后为 null
    "exposed_repo_path": "string", // activity 发生时仓库的 path，这时的 path 是可以公开的
    "freeze": false, // 仓库是否封禁
    "repo_unaccessible": false, // 仓库是否不可访问（公仓转私仓或仓库被删除后不可访问）
    "time": 0.0,
    "visibility_level": {
    } // 仓库可见性
  }],
  "issues_count": 0,
  "private_score": 0,
  "pull_request_count": 0,
  "pull_requests": [{
    "detail": {
      "path": "string" // 完整仓库路径
    }, // 公仓转私仓或仓库被删除后为 null
    "exposed_repo_path": "string", // activity 发生时仓库的 path，这时的 path 是可以公开的
    "freeze": false, // 仓库是否封禁
    "repo_unaccessible": false, // 仓库是否不可访问（公仓转私仓或仓库被删除后不可访问）
    "time": 0.0,
    "visibility_level": {
    } // 仓库可见性
  }],
  "repo_count": 0,
  "repos": [{
    "create_at": "string",
    "detail": {
      "created_at": "string",
      "description": "string",
      "display_module": {
        "activity": false, // 仓库动态
        "contributors": false, // 仓库贡献者
        "release": false // 仓库版本
      },
      "flags": {
      },
      "fork_count": 0,
      "forked_from_repo": {
        "created_at": "string",
        "freeze": false,
        "path": "string",
        "resource_id": 0,
        "resource_type": {
        },
        "root_freeze": false,
        "root_id": 0,
        "updated_at": "string"
      }, // 预留
      "freeze": false,
      "id": "string",
      "language": "string", // 仓库程序语言，预留
      "languages": {
        "color": "string",
        "language": "string"
      }, // 仓库语言
      "last_update_nickname": "string", // 最新代码更新人姓名
      "last_update_username": "string", // 最新代码更新人账户名
      "last_updated_at": {
        "time": "string",
        "valid": false // Valid is true if Time is not NULL
      }, // 最新代码更新时间
      "license": "string",
      "mark_count": 0,
      "name": "string",
      "open_issue_count": 0, // 开启的issue数
      "open_pull_request_count": 0, // 开启的pull request数
      "path": "string", // 完整仓库路径
      "second_languages": {
        "color": "string",
        "language": "string"
      }, // 第二语言
      "site": "string",
      "star_count": 0,
      "status": {
      },
      "tags": ["<unknown>"],
      "topics": "string",
      "updated_at": "string",
      "visibility_level": {
      },
      "web_url": "string"
    }, // 公仓转私仓或仓库被删除后为 null
    "exposed_repo_path": "string", // activity 发生时仓库的 path，这时的 path 是可以公开的
    "freeze": false, // 仓库是否封禁
    "repo_unaccessible": false, // 仓库是否不可访问（公仓转私仓或仓库被删除后不可访问）
    "visibility_level": {
    } // 仓库可见性
  }]
}
```
## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/users/{username}/activities" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-G \
-d "date=<date>" \
```
