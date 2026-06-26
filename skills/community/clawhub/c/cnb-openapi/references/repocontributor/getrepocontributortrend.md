# GetRepoContributorTrend

## 原始 Swagger
https://api.cnb.cool/#/operations/GetRepoContributorTrend

## 接口描述
查询仓库贡献者前 100 名的详细趋势数据。Query detailed trend data for top 100 contributors of the repository.
## 接口权限
repo-code:r
## 请求信息

**请求方法：** GET

**请求地址：** ${CNB_API_ENDPOINT}/{slug}/-/contributor/trend

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| slug | 字符串 | 是 | slug|

### 查询参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| limit | 整数 | 否| limit, 0~100|
| exclude_external_users | 布尔值 | 否| exclude_external_users, true|false|
## 响应信息


**响应类型：** web.RepoContribTrend

**响应结构：**
```json
{
  "meta": {
    "gen_branch": "string",
    "gen_hash": "string",
    "updated_at": "string"
  },
  "repo_data": [{
    "a": 0, // 每周增加的行数
    "c": 0, // 每周的提交数量
    "d": 0, // 每周删除的行数
    "w": 0 // 周的时间戳
  }],
  "user_total": 0,
  "users_data": [{
    "author": {
      "email": "string",
      "user_name": "string"
    }, // 贡献者信息
    "commit_count": 0, // 贡献者的总提交数
    "weeks": [{
      "a": 0, // 每周增加的行数
      "c": 0, // 每周的提交数量
      "d": 0, // 每周删除的行数
      "w": 0 // 周的时间戳
    }] // 贡献者以周为单位的提交趋势数据
  }],
  "week_total": 0,
  "with_line_counts": false // 是否统计增删的行数, 默认总提交超过 10000 的仓库不统计
}
```
## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/{slug}/-/contributor/trend" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-G \
-d "limit=<limit>" \
-d "exclude_external_users=<exclude_external_users>" \
```
