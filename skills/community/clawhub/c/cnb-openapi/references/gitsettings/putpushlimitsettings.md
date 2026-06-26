# PutPushLimitSettings

## 原始 Swagger
https://api.cnb.cool/#/operations/PutPushLimitSettings

## 接口描述
设置仓库推送设置。Set push limit settings.
## 接口权限
repo-manage:rw
## 请求信息

**请求方法：** PUT

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/settings/push-limit

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| repo | 字符串 | 是 | 不带.git后缀的仓库名称。格式：`组织名称/仓库名称`|

### 请求体参数


**请求体结构：**

```json
{
  "allow_single_push_number": 0, // 允许单次推送最多允许更新分支和标签的个数数量。
  "check_single_push_number": false, // 是否开启单次更新分支和标签的个数限制。
  "only_master_can_push_tag": false, // 是否仅允许负责人和管理员推送或删除标签、创建或删除版本。
  "push_commit_must_be": "string" // 推送提交到仓库，对提交作者和提交人进行检查。可选值：`any`,`registered`,`pusher`
}
```
## 响应信息


**响应类型：** 无特定格式
## 请求示例

### cURL 示例

```bash
curl -X PUT \
  "${CNB_API_ENDPOINT}/{repo}/-/settings/push-limit" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-H "Content-Type: application/json" \
  -d '{
  "allow_single_push_number": 0,
  "check_single_push_number": false,
  "only_master_can_push_tag": false,
  "push_commit_must_be": "string"
}'
```
