# DeleteBranchLock

## 原始 Swagger
https://api.cnb.cool/#/operations/DeleteBranchLock

## 接口描述
解除锁定分支
## 接口权限
repo-code:rw
## 请求信息

**请求方法：** DELETE

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/git/branch-locks/{branch}

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| repo | 字符串 | 是 | 不带.git后缀的仓库名称。格式：`组织名称/仓库名称`|
| branch | 字符串 | 是 | 分支名称|
## 响应信息


**响应类型：** 无特定格式
## 请求示例

### cURL 示例

```bash
curl -X DELETE \
  "${CNB_API_ENDPOINT}/{repo}/-/git/branch-locks/{branch}" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
```
