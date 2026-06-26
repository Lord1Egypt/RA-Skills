# PostMissionViewList

## 原始 Swagger
https://api.cnb.cool/#/operations/PostMissionViewList

## 接口描述
排序任务集视图。Sort mission view list.
## 接口权限
mission-manage:rw
## 请求信息

**请求方法：** POST

**请求地址：** ${CNB_API_ENDPOINT}/{mission}/-/mission/view-list

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| mission | 字符串 | 是 | Mission slug|

### 请求体参数


**请求体结构：**

```json
{
  "ids": ["string"] // 视图唯一标识列表，按此顺序排序
}
```
## 响应信息


**响应类型：** 无特定格式
## 请求示例

### cURL 示例

```bash
curl -X POST \
  "${CNB_API_ENDPOINT}/{mission}/-/mission/view-list" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-H "Content-Type: application/json" \
  -d '{
  "ids": ["string"]
}'
```
