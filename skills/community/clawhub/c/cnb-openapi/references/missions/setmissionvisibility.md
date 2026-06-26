# SetMissionVisibility

## 原始 Swagger
https://api.cnb.cool/#/operations/SetMissionVisibility

## 接口描述
改变任务集可见性。Update the visibility of a mission.
## 接口权限
mission-manage:rw
## 请求信息

**请求方法：** POST

**请求地址：** ${CNB_API_ENDPOINT}/{mission}/-/settings/set_visibility

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| mission | 字符串 | 是 | mission path|

### 查询参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| visibility | 字符串 | 是| 任务集可见性|
## 响应信息


**响应类型：** 无特定格式
## 请求示例

### cURL 示例

```bash
curl -X POST \
  "${CNB_API_ENDPOINT}/{mission}/-/settings/set_visibility" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-G \
-d "visibility=<visibility>" \
```
