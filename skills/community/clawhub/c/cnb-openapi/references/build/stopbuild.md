# StopBuild

## 原始 Swagger
https://api.cnb.cool/#/operations/StopBuild

## 接口描述
停止一个构建。 Stop a build.
## 接口权限
repo-cnb-trigger:rw
## 请求信息

**请求方法：** POST

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/build/stop/{sn}

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| repo | 字符串 | 是 | repo|
| sn | 字符串 | 是 | SN|
## 响应信息


**响应类型：** dto.BuildResult

**响应结构：**
```json
{
  "buildLogUrl": "string", // 构建链接
  "message": "string", // 构建信息
  "sn": "string", // 构建号
  "success": false // 构建是否触发成功，不代表构建结果
}
```
## 请求示例

### cURL 示例

```bash
curl -X POST \
  "${CNB_API_ENDPOINT}/{repo}/-/build/stop/{sn}" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
```
