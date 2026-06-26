# CreateBranch

## 原始 Swagger
https://api.cnb.cool/#/operations/CreateBranch

## 接口描述
创建新分支。Create a new branch based on a start point.
## 接口权限
repo-code:rw
## 请求信息

**请求方法：** POST

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/git/branches

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
  "name": "string", // 新分支的名称。
  "start_point": "string" // 新分支的起始点。格式：`分支名称`,`提交哈希`,`标签名称`
}
```
## 响应信息


**响应类型：** 无特定格式
## 请求示例

### cURL 示例

```bash
curl -X POST \
  "${CNB_API_ENDPOINT}/{repo}/-/git/branches" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-H "Content-Type: application/json" \
  -d '{
  "name": "string",
  "start_point": "string"
}'
```
