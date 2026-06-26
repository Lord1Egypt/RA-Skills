# ListPulls

## 原始 Swagger
https://api.cnb.cool/#/operations/ListPulls

## 接口描述
查询合并请求列表。List pull requests.
## 接口权限
repo-pr:r
## 请求信息

**请求方法：** GET

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/pulls

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| repo | 字符串 | 是 | 不带.git后缀的仓库名称。格式：`组织名称/仓库名称`|

### 查询参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| page | 整数 | 否| 分页页码。|
| page_size | 整数 | 否| 分页页大小。|
| state | 字符串 | 否| 合并请求状态过滤。可选值：`open`,`closed`,`all`|
| authors | 字符串 | 否| 作者名称过滤。示例值：`张三,李四`|
| reviewers | 字符串 | 否| 评审人名称过滤，-表示无评审人。示例值：`张三,李四`,`-`|
| reviewers_operator | 字符串 | 否| 评审者操作符。示例值：`contains_any`,`contains_all`|
| assignees | 字符串 | 否| 处理人名称过滤，-表示无处理人。示例值：`张三,李四`,`-`|
| assignees_operator | 字符串 | 否| 处理人操作符。示例值：`contains_any`,`contains_all`|
| labels | 字符串 | 否| 标签过滤。示例值：`git,bug,feature`|
| labels_operator | 字符串 | 否| 标签操作符。示例值：`contains_any`,`contains_all`|
| base_ref | 字符串 | 否| 目标分支引用。示例值：`master`|
## 响应信息


**响应类型：** 数组[api.PullRequest]

**响应结构（数组元素）：**
```json
[
{
    "assignees": [{
      "avatar": "string", // 用户头像。
      "email": "string", // 用户邮箱。
      "freeze": false, // 是否冻结。
      "is_npc": false, // 是否是 NPC。
      "nickname": "string", // 昵称。
      "username": "string" // 用户名。
    }], // 处理人列表。
    "author": {
      "avatar": "string", // 用户头像。
      "email": "string", // 用户邮箱。
      "freeze": false, // 是否冻结。
      "is_npc": false, // 是否是 NPC。
      "nickname": "string", // 昵称。
      "username": "string" // 用户名。
    }, // 作者信息。
    "base": {
      "ref": "string", // 分支引用名称。示例值：`refs/heads/main`
      "repo": {
        "id": "string", // 仓库的唯一标识符。
        "name": "string", // 仓库名称。
        "path": "string", // 仓库的路径标识符。
        "web_url": "string" // 仓库的Web访问地址。
      }, // 关联的仓库信息。
      "sha": "string" // 提交哈希值。
    }, // 目标分支信息。
    "blocked_on": "string", // 阻塞原因。枚举值：`no_merge_base`,`internal_error`,`code_conflict`,`status_check`,`waiting_review`
    "body": "string", // 合并请求内容。
    "comment_count": 0, // 评论数量。
    "created_at": "string", // 创建时间。
    "head": {
      "ref": "string", // 分支引用名称。示例值：`refs/heads/main`
      "repo": {
        "id": "string", // 仓库的唯一标识符。
        "name": "string", // 仓库名称。
        "path": "string", // 仓库的路径标识符。
        "web_url": "string" // 仓库的Web访问地址。
      }, // 关联的仓库信息。
      "sha": "string" // 提交哈希值。
    }, // 源分支信息。
    "is_wip": false, // 是否为WIP状态，WIP状态表示合并请求是否是草稿阶段。
    "labels": [{
      "color": "string", // 标签颜色。
      "description": "string", // 标签描述。
      "id": "string", // 标签ID。
      "name": "string" // 标签名称。
    }], // 标签列表。
    "last_acted_at": "string", // 最后更新时间。
    "mergeable_state": "string", // 可合并状态。枚举值：`checking`,`mergeable`,`merging`,`merged`,`conflict`,`no-merge-base`
    "merged_by": {
      "avatar": "string", // 用户头像。
      "email": "string", // 用户邮箱。
      "freeze": false, // 是否冻结。
      "is_npc": false, // 是否是 NPC。
      "nickname": "string", // 昵称。
      "username": "string" // 用户名。
    }, // 合并者信息。
    "number": "string", // Pulls唯一标识编号。
    "repo": {
      "id": "string", // 仓库的唯一标识符。
      "name": "string", // 仓库名称。
      "path": "string", // 仓库的路径标识符。
      "web_url": "string" // 仓库的Web访问地址。
    }, // 仓库信息。
    "review_count": 0, // 评审数量。
    "state": "string", // 合并请求状态。枚举值：`open`,`closed`,`merged`
    "title": "string", // 合并请求标题。
    "updated_at": "string" // 更新时间。
  }
]
```
## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/{repo}/-/pulls" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-G \
-d "page=<page>" \
-d "page_size=<page_size>" \
-d "state=<state>" \
-d "authors=<authors>" \
-d "reviewers=<reviewers>" \
-d "reviewers_operator=<reviewers_operator>" \
-d "assignees=<assignees>" \
-d "assignees_operator=<assignees_operator>" \
-d "labels=<labels>" \
-d "labels_operator=<labels_operator>" \
-d "base_ref=<base_ref>" \
```
