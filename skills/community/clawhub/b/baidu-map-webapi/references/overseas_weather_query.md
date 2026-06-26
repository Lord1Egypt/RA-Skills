# 百度地图海外天气查询 API

## 服务概述

通过行政区划代码或经纬度查询海外城市的实时天气及未来7天天气预报。该接口支持通过海外城市行政区划编码或经纬度坐标查询海外城市的实时天气信息、未来7天天气预报以及未来24小时逐小时预报。用户可选择返回的数据类型，支持中文和英文两种语言。

- **版本**: 1.0.0
- **服务标识**: `weather_abroad`
- **官方文档**: <https://lbs.baidu.com/faq/api?title=webapi/weather-abroad>

### API调用

**GET** `https://api.map.baidu.com/weather_abroad/v1/`

### 输入参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 | 示例 |
|--------|------|------|--------|------|------|
| district_id | string |  | - | 海外城市行政区划编码（自定义编码，仅限本服务使用），与location参数二选一 | JPN10041030001 |
| location | string |  | - | 经纬度坐标，格式：经度,纬度。支持bd09mc/bd09ll/wgs84/gcj02坐标系 | 139.698,35.658 |
| ak | string | T | - | 开发者密钥，需在API控制台申请 | your_ak |
| data_type | string (enum: now, fc, index, alert, fc_hour...) | T | - | 请求数据类型，控制返回内容：now(实况)/fc(预报)/index(指数)/alert(预警)/fc_hour(逐小时预报)/all(全部) | all |
| output | string (enum: json, xml) |  | json | 返回格式，支持json或xml | json |
| language | string (enum: cn, en) |  | cn | 语言类型，中文(cn)或英文(en)，默认中文。目前仅支持行政区划显示英文 | cn |
| coordtype | string (enum: wgs84, bd09ll, bd09mc, gcj02) |  | wgs84 | 坐标类型，支持wgs84/bd09ll/bd09mc/gcj02 | wgs84 |

### 响应结果

#### 响应示例 (供参考)

```json
{
  "result": {
    "now": {
      "rh": 52,
      "temp": 13,
      "text": "阴",
      "uptime": "20200220150000",
      "wind_dir": "东风",
      "feels_like": 11,
      "wind_class": "2级"
    },
    "location": {
      "id": "JPN10041030001",
      "city": "目黑区",
      "name": "目黑区",
      "country": "日本",
      "province": "东京都"
    },
    "forecasts": [
      {
        "low": 12,
        "date": "2020-02-20",
        "high": 12,
        "week": "星期四",
        "wc_day": "<3级",
        "wd_day": "东风",
        "text_day": "阴",
        "wc_night": "<3级",
        "wd_night": "东北风",
        "text_night": "多云"
      }
    ],
    "forecast_hours": [
      {
        "rh": 15,
        "text": "晴",
        "clouds": 10,
        "prec_1h": 0,
        "temp_fc": 14,
        "wind_dir": "西南风",
        "data_time": "2020-04-01 16:00:00",
        "wind_class": "3~4级"
      }
    ]
  },
  "status": 0,
  "message": "success"
}
```

#### 响应字段定义 (基于 Schema)

| 字段路径 | 类型 | 必填 | 说明 | 示例 |
|----------|------|------|------|------|
| `message` | string |  | 状态信息 | success |
| `result` | object |  | 天气数据结果 | None |
| `result.forecast_hours` | array |  | 未来24小时逐小时预报数据 | None |
| `result.forecast_hours[].clouds` | integer |  | 云量(%)，异常值999999 | 10 |
| `result.forecast_hours[].data_time` | string |  | 数据时间 | 2020-04-01 16:00:00 |
| `result.forecast_hours[].dpt` | integer |  | 露点温度（℃），user_type=vip时返回，异常值999999 | None |
| `result.forecast_hours[].pop` | integer |  | 降水概率（%），user_type=vip时返回，异常值999999 | None |
| `result.forecast_hours[].prec_1h` | number |  | 1小时累计降水量(mm)，异常值999999 | 0 |
| `result.forecast_hours[].pressure` | integer |  | 气压（hPa），user_type=vip时返回，异常值999999 | None |
| `result.forecast_hours[].rh` | integer |  | 相对湿度，异常值999999 | 15 |
| `result.forecast_hours[].temp_fc` | integer |  | 温度(℃)，异常值999999 | 14 |
| `result.forecast_hours[].text` | string |  | 天气现象 | 晴 |
| `result.forecast_hours[].uvi` | integer |  | 紫外线指数，user_type=vip时返回，异常值999999 | None |
| `result.forecast_hours[].wind_angle` | integer |  | 风向角度（°），user_type=vip时返回，异常值999999 | None |
| `result.forecast_hours[].wind_class` | string |  | 风力等级 | 3~4级 |
| `result.forecast_hours[].wind_dir` | string |  | 风向描述 | 西南风 |
| `result.forecasts` | array |  | 7天天气预报数据 | None |
| `result.forecasts[].date` | string |  | 日期（当地时间） | 2020-02-20 |
| `result.forecasts[].high` | integer |  | 最高温度(℃)，异常值999999 | 12 |
| `result.forecasts[].low` | integer |  | 最低温度(℃)，异常值999999 | 12 |
| `result.forecasts[].text_day` | string |  | 白天天气现象 | 阴 |
| `result.forecasts[].text_night` | string |  | 晚上天气现象 | 多云 |
| `result.forecasts[].wc_day` | string |  | 白天风力 | <3级 |
| `result.forecasts[].wc_night` | string |  | 晚上风力 | <3级 |
| `result.forecasts[].wd_day` | string |  | 白天风向 | 东风 |
| `result.forecasts[].wd_night` | string |  | 晚上风向 | 东北风 |
| `result.forecasts[].week` | string |  | 星期（当地时间） | 星期四 |
| `result.location` | any |  |  | None |
| `result.now` | any |  |  | None |
| `status` | integer |  | 返回状态码，0表示成功 | 0 |

### 常见问题

**Q: 如何获取海外城市的行政区划编码？**

A: 海外城市行政区划编码为自定义编码，仅限本服务使用。可通过文档中提供的Excel文件下载获取完整的海外城市编码列表。

**Q: district_id和location参数可以同时使用吗？**

A: 可以同时传递，但系统会优先使用district_id参数。如果同时传递，默认以district_id为准进行查询。

**Q: data_type参数有哪些可选值？分别返回什么数据？**

A: data_type支持now(实况数据)、fc(7天预报)、index(指数)、alert(预警)、fc_hour(逐小时预报)、all(全部数据)。选择不同的值将控制返回的内容范围。

**Q: VIP用户和普通用户返回的数据有什么区别？**

A: VIP用户可获取更多高级数据，如风向角度、紫外线指数、气压、露点温度等字段。这些字段在普通用户请求时不会返回。

**Q: 返回数据中的异常值999999表示什么？**

A: 当某些气象数据无法获取或无效时，系统会返回999999作为异常值标识，如温度、湿度等数值型字段。
