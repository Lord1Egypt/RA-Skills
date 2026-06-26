# GetMissionViewConfig

## 原始 Swagger
https://api.cnb.cool/#/operations/GetMissionViewConfig

## 接口描述
查询任务集视图配置信息。Get mission view config.
## 接口权限
mission-manage:r
## 请求信息

**请求方法：** GET

**请求地址：** ${CNB_API_ENDPOINT}/{mission}/-/mission/view

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| mission | 字符串 | 是 | Mission slug|

### 查询参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| id | 字符串 | 是| View ID|
## 响应信息


**响应类型：** dto.MissionViewConfig

**响应结构：**
```json
{
  "fields": [{
    "field": "string",
    "width": 0
  }], // 字段配置
  "group": {
    "customOrders": {
      "field": "string",
      "value": [null]
    },
    "customVisible": {
      "field": "string",
      "value": [null]
    },
    "expendedList": [null],
    "field": "string",
    "order": {
    }
  }, // 分组信息
  "id": "string", // 视图唯一标识
  "selectors": [{
    "field": "string",
    "operator": {
    },
    "value": ["string"]
  }], // 筛选条件
  "sorts": [{
    "field": "string",
    "order": {
    }
  }], // 排序条件
  "type": {
  } // 视图类型
}
```
## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/{mission}/-/mission/view" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-G \
-d "id=<id>" \
```
