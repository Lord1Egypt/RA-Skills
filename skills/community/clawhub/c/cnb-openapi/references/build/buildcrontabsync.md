# BuildCrontabSync

## 原始 Swagger
https://api.cnb.cool/#/operations/BuildCrontabSync

## 接口描述
同步仓库分支下的定时任务。 Synchronize the content under the repository branch.
## 接口权限
repo-cnb-trigger:rw
## 请求信息

**请求方法：** POST

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/build/crontab/sync/{branch}

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| repo | 字符串 | 是 | repo|
| branch | 字符串 | 是 | Branch|
## 响应信息


**响应类型：** dto.BuildCommonResult

**响应结构：**
```json
{
  "code": 0, // 返回码，0 表示成功，1 表示失败
  "message": "string" // 描述
}
```
## 请求示例

### cURL 示例

```bash
curl -X POST \
  "${CNB_API_ENDPOINT}/{repo}/-/build/crontab/sync/{branch}" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
```
