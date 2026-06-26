# GetCommitStatuses

## 原始 Swagger
https://api.cnb.cool/#/operations/GetCommitStatuses

## 接口描述
查询指定 commit 的提交状态。List commit check statuses.
## 接口权限
repo-code:r
## 请求信息

**请求方法：** GET

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/git/commit-statuses/{commitish}

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| repo | 字符串 | 是 | 不带.git后缀的仓库名称。格式：`组织名称/仓库名称`|
| commitish | 字符串 | 是 | Git引用标识符。格式：`分支名称`,`提交哈希值`,`标签名称`|
## 响应信息


**响应类型：** 数组[git_woa_com_cnb_monorepo_git_internal_app_git_service_bff_api.CommitStatus]

**响应结构（数组元素）：**
```json
[
{
    "context": "string", // 提交状态上下文标识符。
    "created_at": "string", // 创建时间。
    "description": "string", // 提交状态描述信息。
    "state": "string", // 提交状态。枚举值：`pending`,`success`,`failure`,`error`,`skip`
    "target_url": "string", // 提交状态详情链接。
    "updated_at": "string" // 更新时间。
  }
]
```
## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/{repo}/-/git/commit-statuses/{commitish}" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
```
