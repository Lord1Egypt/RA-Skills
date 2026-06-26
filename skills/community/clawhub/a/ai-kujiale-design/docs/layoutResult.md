## 描述

AI智能设计平台指定方案执行智能布局后的布局结果

## API

```
GET https://oauth.kujiale.com/oauth2/openapi/ai-design-skill/design/layout-res
```

## 入参

### Query Param

| 参数 | 是否必须 | 参数类型 | 参数说明 |
| --- | :---: | :---: | ---- |
|access_token                                      |是| string              | 用户系统配置的令牌|
| designId | 是 | string | 方案ID |

## 响应

### 数据结构

```javascript
{
  "c": "0",
  "m": "string",
  "d": [
    {
      "layoutList": [
        {
          "name": "玄关柜",
          "length": 1320.0,
          "width": 351.5625,
          "position": {
            "x": 2451.693,
            "y": 314.87213
          },
          "rotation": 3.1415927
        }
      ],
      "roomId": "551",
      "roomName": "客餐厅"
    }
  ]
}
```

### 字段说明

| 参数 | 是否必须 | 参数类型 | 参数说明 |
| --- | :---: | :---: | ---- |
| c | 否 | string | 响应码 |
| m | 否 | string | null |
| d | 否 | list&object | 响应数据 |
| d.roomId | 否 | string | 房间ID |
| d.roomName | 否 | string | 房间名称 |
| d.layoutList | 否 | list&object | 布局列表 |
| d.layoutList.name | 否 | string | 名称 |
| d.layoutList.position | 否 | object | 位置坐标，模型中心点位,单位毫米（mm） x：x坐标 y：y坐标 |
| d.layoutList.position.x | 否 | float | X坐标 |
| d.layoutList.position.y | 否 | float | Y坐标 |
| d.layoutList.length | 否 | float | 长 |
| d.layoutList.width | 否 | float | 宽 |
| d.layoutList.rotation | 否 | float | 旋转角度,用π(π=3.1415926)来表示，0:表示y轴的负方向,π：表示y轴的正方向轴的正方向 |
