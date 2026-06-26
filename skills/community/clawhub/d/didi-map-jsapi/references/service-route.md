---
outline: deep
---
 # RoutePlanService


**`路线规划服务`**

路径规划API提供了多种出行方式的路线规划服务，您可以为用户提供最佳出行路线建议。

路线规划服务包含4个核心能力：

* 驾车路线规划([driving](#driving))：提供综合路径规划服务，用于为接驾或送驾场景提供最佳路线。
* 骑行路线规划([bicycling](#bicycling))：规划骑行路线，提供从起点到终点的自行车导航路线、距离和时间。
* 步行路线规划([walking](#walking))：规划步行路线，提供从起点到终点的步行导航路线、距离和时间。
* 公交路线规划([transit](#transit))：划公交路线，提供从起点到终点的公共交通路线、距离和时间。

## driving
**`驾车路线规划`**

### 请求

#### 请求参数
请求参数应为[RoutePlanReq][10]模型的JSON格式。


#### 请求示例
```javascript
window.DiMapLoader.load({
  key: "您申请的服务端key",
}).then(async ({ DiMap }) => {
    const routePlanService = new DiMap.RoutePlanService();
    const [err, res] = await routePlanService.driving({
        packs: [
            {
                origin: "116.2807,40.04811",
                destination: "116.29334,40.05203",
                departure_time: 1741662325,
                routeplan_type: "1",
                need_polyline: true
            }
        ]
    })
    console.log("driving--res", res)
})
```

### 响应

#### 响应格式
成功响应为 **[RoutePlanResponse][6]** 模型的JSON格式。

#### 响应示例
```json
{
    "status": 10000,
    "msg": "OK",
    "trace_id": "0ab68d31691455ce76bba01c0dd8e602",
    "results": [
        {
            "errcode": 0,
            "errmsg": "ok",
            "routes": [
                {
                    "dist": 1659,
                    "duration": 338,
                    "geo_list": [
                        {
                            "latitude": 40.04811745749209,
                            "longitude": 116.28069728746046
                        },
                        {
                            "latitude": 40.04811,
                            "longitude": 116.28066
                        }
                    ],
                    "tag": "平台推荐"
                }
            ]
        }
    ]
}
```

## bicycling

**`骑行路线规划`**

### 请求

#### 请求参数
| 参数名 | 必选 | 类型 | 描述 | 示例值 |
|--------|------|------|------|--------|
| origin | 是 | string | 起点经纬度，格式：lng,lat | "116.2807,40.04811" |
| destination | 是 | string | 终点经纬度，格式：lng,lat | "116.29334,40.05203" |

#### 请求示例
```javascript
window.DiMapLoader.load({
  key: "您申请的服务端key"
}).then(async ({ DiMap }) => {
    const routePlanService = new DiMap.RoutePlanService();
    const [err, res] = await routePlanService.bicycling({
        origin: "116.2807,40.04811",
        destination: "116.29334,40.05203"
    })
    console.log("bicycling--res", res)
})
```

### 响应

#### 响应格式
成功响应为 **[BicyclingResponse][7]** 模型的JSON格式。

#### 响应示例
```json
{
  "status": 10000,
  "msg": "OK",
  "trace_id": "0a88552d691465717eef12c00e449d02",
  "results": [
    {
      "dist": 1625,
      "duration": 507,
      "errcode": 0,
      "errmsg": "ok",
      "geo_list": [
        {
          "latitude": 40.04811628178853,
          "longitude": 116.28069769073119
        },
        {
          "latitude": 40.04811,
          "longitude": 116.28066
        },
        {
          "latitude": 40.04879,
          "longitude": 116.28052
        },
        {
          "latitude": 40.049,
          "longitude": 116.28048
        },
        {
          "latitude": 40.04905,
          "longitude": 116.28046
        }
      ]
    }
  ]
}
```

## walking

**`步行路线规划`**

### 请求

#### 请求参数
| 参数名 | 必选 | 类型 | 描述 | 示例值 |
|--------|------|------|------|--------|
| origin | 是 | string | 起点经纬度，格式：lng,lat | "116.2807,40.04811" |
| destination | 是 | string | 终点经纬度，格式：lng,lat | "116.29334,40.05203" |

#### 请求示例
```javascript
window.DiMapLoader.load({
  key: "您申请的服务端key"
}).then(async ({ DiMap }) => {
    const routePlanService = new DiMap.RoutePlanService();
    const [err, res] = await routePlanService.walking({
        origin: "116.2807,40.04811",
        destination: "116.29334,40.05203"
    })
    console.log("walking--res", res)
})
```

### 响应

#### 响应格式
成功响应为 **[WalkRouteResponse][8]** 模型的JSON格式。

#### 响应示例

```javascript
{
    "status": 10000,
    "msg": "OK",
    "trace_id": "0aac90c869158108253f3dd52f693f02",
    "results": [
        {
            "dist": 1524.0960494456072,
            "duration": 1219,
            "geo_list": [
                {
                    "latitude": 40.04811,
                    "longitude": 116.28071
                },
                {
                    "latitude": 40.04846,
                    "longitude": 116.28063
                },
                {
                    "latitude": 40.0488,
                    "longitude": 116.28056
                },
                {
                    "latitude": 40.04891,
                    "longitude": 116.28054
                },
                {
                    "latitude": 40.04902,
                    "longitude": 116.28051
                },
            ]
        }
    ]
}
```

## transit

**`公交路线规划`**

### 请求

#### 请求参数
| 参数名 | 必选 | 类型 | 描述 | 示例值 |
|--------|------|------|------|--------|
| origin | 是 | string | 起点经纬度，格式：lng,lat | "116.2807,40.04811" |
| destination | 是 | string | 终点经纬度，格式：lng,lat | "116.29334,40.05203" |
| city | 是 | string | 城市名称 | "北京市" |
| strategy | 否 | number | 路线偏好策略：0-推荐模式;1-最快捷模式;2-最少步行模式;3-最少换乘模式;4-不乘地铁模式;5-地铁优先模式 | 0 |
| departure_time | 否 | number | 出发时间，unix秒级时间戳，默认0表示现在出发 | 1741662325 |
| route_num | 否 | number | 返回方案个数，取值1-10，默认5 | 3 |

#### 请求示例
```javascript
window.DiMapLoader.load({
  key: "您申请的服务端key"
}).then(async ({ DiMap }) => {
    const routePlanService = new DiMap.RoutePlanService();
    const [err, res] = await routePlanService.transit({
        origin: "116.2807,40.04811",
        destination: "116.29334,40.05203",
        city: "北京市",
        strategy: 0,
        departure_time: Math.floor(Date.now() / 1000),
        route_num: 3
    })
    console.log("transit--res", res)
})
```

### 响应

#### 响应格式
成功响应为 **[TransitRouteResponse][9]** 模型的JSON格式。

#### 响应示例
```json
{
    "status": 10000,
    "msg": "OK",
    "trace_id": "0ab775d769153d7c852d9a5a12cccf02",
    "results": [
        {
            "cost": 200,
            "destination": "116.29334,40.05203",
            "distance": 1688,
            "duration": 1140,
            "origin": "116.2807,40.04811",
            "walking_distance": 735,
            "segments": [
                {
                    "mode": "WALKING",
                    "walking": {
                        "origin": "116.28071,40.04811",
                        "destination": "116.2831,40.05111",
                        "distance": 532,
                        "duration": 420
                    }
                },
                {
                    "mode": "TRANSIT",
                    "metrobus": [
                        {
                            "name": "365路",
                            "id": "24712744857960001",
                            "type": 1,
                            "cost": 200,
                            "distance": 953,
                            "duration": 152,
                            "first_time": "05:30",
                            "last_time": "21:00",
                            "departure_stop": {
                                "name": "软件园北站",
                                "location": "116.283133,40.051162"
                            },
                            "arrival_stop": {
                                "name": "东北旺北", 
                                "location": "116.293944,40.053319"
                            }
                        }
                    ]
                },
                {
                    "mode": "WALKING",
                    "walking": {
                        "origin": "116.29395,40.05327",
                        "destination": "116.29332,40.05202",
                        "distance": 203,
                        "duration": 180
                    }
                }
            ]
        }
    ]
}
```


[1]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Object

[2]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array

[3]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Promise

[4]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String

[5]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Number

[6]:/web/guide/响应模型.html#routeplanresponse

[7]:/web/guide/响应模型.html#bicyclingresponse

[8]:/web/guide/响应模型.html#walkrouteresponse

[9]:/web/guide/响应模型.html#transitrouteresponse

[10]:/web/guide/响应模型.html#routeplanreq