# GetArchiveCompareChangedFiles

## 原始 Swagger
https://api.cnb.cool/#/operations/GetArchiveCompareChangedFiles

## 接口描述
打包下载两次 ref 之间的变更文件。Download archive of changed files for a compare.
## 接口权限
repo-code:r
## 请求信息

**请求方法：** GET

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/git/archive-compare-changed-files/{base_head}

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| repo | 字符串 | 是 | 不带.git后缀的仓库名称。格式：`组织名称/仓库名称`|
| base_head | 字符串 | 是 | 用于Git比较操作的基准和头部分支或提交的SHA值。格式：`base...head`|
## 响应信息


**响应类型：** 无特定格式
## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/{repo}/-/git/archive-compare-changed-files/{base_head}" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
```
