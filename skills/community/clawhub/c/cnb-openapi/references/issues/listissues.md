# ListIssues

## 原始 Swagger
https://api.cnb.cool/#/operations/ListIssues

## 接口描述
查询仓库的 Issues。List issues.
## 接口权限
repo-issue:r
## 请求信息

**请求方法：** GET

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/issues

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
| page | 整数 | 否| 分页页码，输入值小于1，则调整为1。|
| page_size | 整数 | 否| 分页页大小，输入值小于0，则调整为10;输入值大于100，则调整为100。|
| state | 字符串 | 否| Issue状态过滤。可选值：`open`、`closed`|
| keyword | 字符串 | 否| Issue搜索关键词，支持在标题和内容中模糊搜索。|
| priority | 字符串 | 否| Issue优先级过滤。示例：`-2P,-1P,P0,P1,P2,P3`|
| labels | 字符串 | 否| Issue标签过滤。示例：`git,bug,feature`|
| labels_operator | 字符串 | 否| 标签过滤操作符。可选值：`contains_any`,`contains_all`|
| authors | 字符串 | 否| Issue创建者过滤，多个作者用英文逗号分隔。示例：`张三,李四`|
| assignees | 字符串 | 否| Issue处理人过滤，多个处理人用英文逗号分隔，-表示未分配处理人。示例：`张三,李四`,`-`|
| updated_time_begin | 字符串 | 否| Issue更新时间范围开始。示例：`2022-01-31`|
| updated_time_end | 字符串 | 否| Issue更新时间范围结束。示例：`2022-02-16`|
| close_time_begin | 字符串 | 否| Issue关闭时间范围开始。示例：`2022-01-31`|
| close_time_end | 字符串 | 否| Issue关闭时间范围结束。示例：`2022-02-16`|
| order_by | 字符串 | 否| Issue排序字段，-前缀表示倒序。可选值：`created_at`,`-created_at`,`-updated_at`,`-last_acted_at`|
## 响应信息


**响应类型：** 数组[api.Issue]

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
    }], // Issue处理人列表，最多支持8个处理人。
    "author": {
      "avatar": "string", // 用户头像。
      "email": "string", // 用户邮箱。
      "freeze": false, // 是否冻结。
      "is_npc": false, // 是否是 NPC。
      "nickname": "string", // 昵称。
      "username": "string" // 用户名。
    }, // Issue创建者信息。
    "comment_count": 0, // Issue评论数量。
    "created_at": "string", // Issue创建时间。
    "ended_at": "string", // Issue结束日期。
    "invisible": false, // Issue是否可见。
    "labels": [{
      "color": "string", // 标签颜色。
      "description": "string", // 标签描述。
      "id": "string", // 标签ID。
      "name": "string" // 标签名称。
    }], // Issue标签列表，最多支持10个标签。
    "last_acted_at": "string", // Issue最后活动时间。
    "number": "string", // Issue的唯一标识编号。
    "priority": "string", // Issue优先级。枚举值：`-2P`,`-1P`,`P0`,`P1`,`P2`,`P3`
    "started_at": "string", // Issue开始日期。
    "state": "string", // Issue状态。枚举值：`open`,`closed`
    "state_reason": "string", // 状态变更原因。枚举值：`open`,`completed`,`not_planned`,`reopened`
    "title": "string", // Issue标题，长度限制2-255字符。
    "updated_at": "string" // Issue最后更新时间。
  }
]
```
## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/{repo}/-/issues" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-G \
-d "page=<page>" \
-d "page_size=<page_size>" \
-d "state=<state>" \
-d "keyword=<keyword>" \
-d "priority=<priority>" \
-d "labels=<labels>" \
-d "labels_operator=<labels_operator>" \
-d "authors=<authors>" \
-d "assignees=<assignees>" \
-d "updated_time_begin=<updated_time_begin>" \
-d "updated_time_end=<updated_time_end>" \
-d "close_time_begin=<close_time_begin>" \
-d "close_time_end=<close_time_end>" \
-d "order_by=<order_by>" \
```
