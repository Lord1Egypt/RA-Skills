## 描述

获取户型图信息，用于展示户型平面图给用户确认

## API

```
GET https://www.kujiale.com/api/designinfo/floorplans?planid={planId}
```

注意：此接口不需要鉴权，无需 access_token

## 入参

### Query Param

| 参数 | 是否必须 | 参数类型 | 参数说明 |
| --- | :---: | :---: | ---- |
| planid | 是 | string | 户型ID |

## 响应

### 数据结构

```javascript
{
  "c": "0",
  "m": "",
  "d": {
    "allScore": 77,
    "homeAnalysisScore": {
      "movingLineScore": 29,
      "zoneScore": 30,
      "ventilationScore": 18,
      "created": 1755173750000,
      "lastmodified": 1779270658000,
      "id": "3FO4K4W0G1HG",
      "planId": "3FO4M214MD75"
    },
    "floorplanInfos": [
      {
        "area": 220.64716,
        "realArea": 176.51773,
        "planImage": "https://qhtbdoss.kujiale.com/fpimgnew/sit/3FO4M214MD75/panoguide/1/c98a317964e991963c6338fe9ac728f8_800x800.jpg",
        "levelIndex": 0,
        "levelName": "一层"
      }
    ]
  }
}
```

### 字段说明

| 参数 | 是否必须 | 参数类型 | 参数说明 |
| --- | :---: | :---: | ---- |
| c | 是 | string | 响应码，"0"表示成功 |
| m | 是 | string | 响应信息 |
| d | 是 | object | 响应数据 |
| d.allScore | 否 | number | 户型总分 |
| d.homeAnalysisScore | 否 | object | 户型分析评分 |
| d.floorplanInfos | 否 | list&object | 楼层户型图信息列表，可能为空数组 |
| d.floorplanInfos.area | 否 | number | 建筑面积（平方米） |
| d.floorplanInfos.realArea | 否 | number | 实际面积（平方米） |
| d.floorplanInfos.planImage | 否 | string | 户型平面图URL |
| d.floorplanInfos.levelIndex | 否 | number | 楼层索引，0表示一层 |
| d.floorplanInfos.levelName | 否 | string | 楼层名称 |

## 使用说明

- 取 `floorplanInfos[0].planImage` 展示给用户确认户型
- 若 `floorplanInfos` 为空数组，表示户型图获取失败，需提示用户重新操作