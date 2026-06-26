# GetRaw

## 原始 Swagger
https://api.cnb.cool/#/operations/GetRaw

## 接口描述
获得仓库指定文件内容
## 接口权限
repo-code:r
## 请求信息

**请求方法：** GET

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/git/raw/{ref_with_path}

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| repo | 字符串 | 是 | 不带.git后缀的仓库名称。格式：`组织名称/仓库名称`|
| ref_with_path | 字符串 | 是 | 包含路径的Git引用。格式：`分支名/文件路径`,`标签名/文件路径`,`提交哈希/文件路径`|

### 查询参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| max_in_byte | 整数 | 否| 获得文件内容大小限制（字节），0表示使用gitConfig.RawFileLimitInByte配置值。|
## 响应信息


**响应类型：** 字符串## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/{repo}/-/git/raw/{ref_with_path}" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-G \
-d "max_in_byte=<max_in_byte>" \
```
