# PatchBranchProtection

## 原始 Swagger
https://api.cnb.cool/#/operations/PatchBranchProtection

## 接口描述
更新仓库保护分支规则。Update branch protection rule.
## 接口权限
repo-manage:rw
## 请求信息

**请求方法：** PATCH

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/settings/branch-protections/{id}

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| repo | 字符串 | 是 | 不带.git后缀的仓库名称。格式：`组织名称/仓库名称`|
| id | 字符串 | 是 | 保护分支规则唯一标识符。|

### 请求体参数


**请求体结构：**

```json
{
  "allow_creation": false, // 是否允许所有人创建保护分支。
  "allow_deletions": false, // 是否允许所有人删除保护分支。
  "allow_force_pushes": false, // 是否允许所有人强制推送。
  "allow_master_creation": false, // 是否仅允许仓库管理员及负责人创建保护分支。
  "allow_master_deletions": false, // 是否仅允许仓库管理员及负责人删除保护分支。
  "allow_master_force_pushes": false, // 是否仅允许仓库管理员及负责人强制推送。
  "allow_master_manual_merge": false, // 是否允许仓库管理员及负责人手动合并到目标分支。
  "allow_master_pushes": false, // 是否仅允许仓库管理员及负责人推送代码到保护分支中。
  "allow_pushes": false, // 是否允许所有人推送代码到保护分支中。
  "id": "string", // 保护分支规则唯一标识符。
  "required_approved_review_count": 0, // 需要的代码评审者数量。格式：`评审者数量 ∈ [1,5]`
  "required_approved_review_ratio": 0, // 需要的评审通过率。格式：`通过率 ∈ [1, 100]`
  "required_linear_history": false, // 是否仅允许线性提交。
  "required_master_approve": false, // 是否需至少一个仓库管理员批准。
  "required_must_auto_merge": false, // 是否仅允许自动合并。
  "required_must_push_via_pull_request": false, // 是否必须通过合并请求推送代码到此规则匹配分支中。
  "required_pull_request_reviews": false, // 保护分支的合并请求是否需要代码评审。
  "required_status_checks": false, // 是否需要通过状态检查。
  "rule": "string" // 保护分支规则名称，支持通配符。
}
```
## 响应信息


**响应类型：** 无特定格式
## 请求示例

### cURL 示例

```bash
curl -X PATCH \
  "${CNB_API_ENDPOINT}/{repo}/-/settings/branch-protections/{id}" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-H "Content-Type: application/json" \
  -d '{
  "allow_creation": false,
  "allow_deletions": false,
  "allow_force_pushes": false,
  "allow_master_creation": false,
  "allow_master_deletions": false,
  "allow_master_force_pushes": false,
  "allow_master_manual_merge": false,
  "allow_master_pushes": false,
  "allow_pushes": false,
  "id": "string",
  "required_approved_review_count": 0,
  "required_approved_review_ratio": 0,
  "required_linear_history": false,
  "required_master_approve": false,
  "required_must_auto_merge": false,
  "required_must_push_via_pull_request": false,
  "required_pull_request_reviews": false,
  "required_status_checks": false,
  "rule": "string"
}'
```
