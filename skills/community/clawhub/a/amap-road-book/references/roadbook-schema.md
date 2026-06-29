# 路书 JSON 结构

生成可用于地图渲染的路书数据时使用本结构。后续同一份数据可以接入网页渲染器、静态地图渲染器或线上行程页。

## 规划请求

调用高德 API 前，建议先整理成以下内部结构：

```json
{
  "origin": "合肥",
  "destination": "北京",
  "dateRange": {
    "start": "2026-06-15",
    "end": "2026-06-18",
    "days": 4
  },
  "mustVisit": ["圆明园", "北京环球度假区", "北京大兴国际机场"],
  "intercityTransport": "rail",
  "localTransport": "public_transit",
  "lodging": {
    "name": null,
    "area": "海淀"
  },
  "pace": "relaxed",
  "constraints": ["抵达日有行李"],
  "language": "zh-CN"
}
```

## 路书输出

```json
{
  "title": "合肥到北京高德路书",
  "origin": {
    "label": "合肥",
    "adcode": "340100"
  },
  "destination": {
    "label": "北京",
    "adcode": "110000"
  },
  "dateRange": {
    "start": "2026-06-15",
    "end": "2026-06-18",
    "days": 4
  },
  "assumptions": [
    "住宿区域按海淀处理，用户未提供具体酒店。",
    "高铁班次和票价需要在高德以外确认。"
  ],
  "warnings": [
    "北京环球度假区当天跨城通勤时间较长。"
  ],
  "days": [
    {
      "id": "day-1",
      "date": "2026-06-15",
      "title": "抵达北京并入住酒店",
      "weather": {
        "city": "北京",
        "text": "多云",
        "temperature": "24-31 C",
        "source": "amap-weather"
      },
      "pace": "relaxed",
      "stops": [
        {
          "id": "stop-1",
          "time": "09:00",
          "name": "合肥南站",
          "type": "railway_station",
          "address": "合肥",
          "poiId": "optional-amap-poi-id",
          "lng": 117.289,
          "lat": 31.800,
          "durationMinutes": 45,
          "note": "乘坐高铁出发。",
          "source": "amap-keyword-search"
        }
      ],
      "legs": [
        {
          "id": "leg-1",
          "from": "合肥南站",
          "to": "北京南站",
          "mode": "rail",
          "durationText": "约 4 小时 30 分钟",
          "distanceText": "城际交通",
          "summary": "用户偏好高铁，具体班次需另行确认。",
          "steps": [],
          "source": "user-preference"
        }
      ]
    }
  ]
}
```

必需顶层字段：`title`、`origin`、`destination`、`dateRange`、`days`。

必需每日字段：`id`、`title`、`stops`、`legs`。

必需停靠点字段：`name`、`lng`、`lat`。

必需路段字段：`from`、`to`、`mode`、`durationText`、`summary`。

## 交通方式枚举

尽量使用以下 `mode` 值：

- `walk`
- `public_transit`
- `drive`
- `taxi`
- `bike`
- `rail`
- `flight`
- `mixed`

## 来源标记

使用 `source` 字段说明数据可信度：

- `amap-geocode`
- `amap-regeo`
- `amap-keyword-search`
- `amap-around-search`
- `amap-route`
- `amap-weather`
- `user-provided`
- `agent-assumption`
- `requires-third-party-confirmation`
