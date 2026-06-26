# ListWorkspaces

## 原始 Swagger
https://api.cnb.cool/#/operations/ListWorkspaces

## 接口描述
获取我的云原生开发环境列表。List my workspaces.
## 接口权限
account-engage:r
## 请求信息

**请求方法：** GET

**请求地址：** ${CNB_API_ENDPOINT}/workspace/list

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 查询参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| branch | 字符串 | 否| Git branch name, e.g. "main"|
| end | 字符串 | 否| 查询结束时间。Query end time. format YYYY-MM-DD HH:mm:ssZZ, e.g. 2024-12-01 00:00:00+0800|
| page | 整数 | 否| Pagination page number, default(1)|
| page_size | 整数 | 否| Pagination page size, default(20), max(100)|
| slug | 字符串 | 否| Repository path, e.g. "groupname/reponame"|
| start | 字符串 | 否| 查询开始时间。Query start time. format YYYY-MM-DD HH:mm:ssZZ, e.g. 2024-12-01 00:00:00+0800|
| status | 字符串 | 否| 开发环境状态，running: 开发环境已启动，closed：开发环境已关闭。Workspace status: "running" for started, "closed" for stopped.|
## 响应信息


**响应类型：** dto.WorkspaceListResult

**响应结构：**
```json
{
  "hasMore": false, // 是否有更多数据
  "list": [{
    "branch": "string", // 分支名，例如：main
    "commit_count": 0, // 备份的 commit 数
    "create_time": "string", // 开发环境创建时间，例如：2024-12-02T03:20:22.000Z
    "duration": 0, // 开发环境持续时间，单位：ms（非实时更新）
    "file_count": 0, // 备份的文件数
    "file_list": "string", // 备份的文件列表，仅前五个备份文件相对路径
    "latest_sha": "string", // 环境销毁时远程最新的 commit short hash
    "pipeline_id": "string", // 创建环境的子流水线 id
    "remote_stash_count": 0, // 备份的 stash 数
    "repo_url": "string", // 仓库地址
    "restore_id": "string", // 恢复备份代码的流水线 id，如果有值表示备份代码已被恢复（重建环境时会恢复备份代码）
    "slug": "string", // 仓库路径，例如：groupname/reponame
    "sn": "string", // 创建开发环境的流水线 sn
    "ssh": false, // 开发环境是否支持 ssh 链接
    "status": "string", // 工作区状态，running: 开发环境已启动，closed：开发环境已关闭
    "workspace": "string" // 开发环境默认工作区路径
  }], // 云原生开发环境列表
  "pageInfo": {
    "page": 0,
    "page_size": 0
  }, // 分页信息
  "total": 0 // 总数
}
```
## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/workspace/list" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-G \
-d "branch=<branch>" \
-d "end=<end>" \
-d "page=<page>" \
-d "page_size=<page_size>" \
-d "slug=<slug>" \
-d "start=<start>" \
-d "status=<status>" \
```
