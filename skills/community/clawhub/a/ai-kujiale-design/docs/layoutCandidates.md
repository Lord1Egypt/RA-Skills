## 描述

获取方案中各房间的候选布局列表，用于用户选择满意的布局方案

## API

```
GET https://oauth.kujiale.com/oauth2/openapi/ai-design-skill/design/layout-candidates
```

## 入参

### Query Param

| 参数 | 是否必须 | 参数类型 | 参数说明 |
| --- | :---: | :---: | ---- |
| access_token | 是 | string | 用户系统配置的令牌 |
| designId | 是 | string | 方案ID |

## 响应

### 数据结构

```javascript
{
  "c": "0",
  "m": "string",
  "d": [
    {
      "roomId": "551",
      "roomName": "客餐厅",
      "candidateList": [
        {
          "obsId": "candidate_001",
          "name": "方案A",
          "maasRoomLayoutId": "layout_001",
          "layoutList": [
            {
              "name": "沙发",
              "length": 2000.0,
              "width": 800.0,
              "position": { "x": 1000.0, "y": 500.0 },
              "rotation": 0.0
            }
          ]
        }
      ]
    }
  ]
}
```

### 字段说明

| 参数 | 是否必须 | 参数类型 | 参数说明 |
| --- | :---: | :---: | ---- |
| c | 否 | string | 响应码 |
| m | 否 | string | 响应信息 |
| d | 否 | list&object | 响应数据，房间候选布局列表 |
| d.roomId | 否 | string | 房间ID |
| d.roomName | 否 | string | 房间名称 |
| d.candidateList | 否 | list&object | 候选布局列表 |
| d.candidateList.obsId | 否 | string | 布局ID |
| d.candidateList.name | 否 | string | 布局名称 |
| d.candidateList.maasRoomLayoutId | 否 | string | 算法布局ID |
| d.candidateList.layoutList | 否 | list&object | 布局家具列表 |