# 百度地图国内天气查询 API

## 服务概述

国内天气查询接口，支持通过行政区划代码、经纬度坐标或省市区名称查询国内天气信息。可获取实时天气、未来7天预报、逐小时预报、生活指数、气象预警等数据。支持百度坐标（BD-09ll/BD-09mc）、国测局坐标（GCJ-02）、GPS坐标（WGS-84）四种坐标系。适用于天气应用开发、出行规划、农业气象监测、智能家居天气联动等场景。

- **版本**: 2.0.0
- **服务标识**: `weather`
- **官方文档**: <https://lbs.baidu.com/faq/api?title=webapi/weather/base>

### API调用

**GET** `https://api.map.baidu.com/weather/v1/`

### 输入参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 | 示例 |
|--------|------|------|--------|------|------|
| district_id | string |  | - | 区县的行政区划编码，与 location、district 三者必选其一。 | 222405 |
| location | string |  | - | 经纬度，经度在前纬度在后，逗号分隔。支持 bd09mc/bd09ll/wgs84/gcj02。与 district_id、district 三者必选其一。 | 116.405285,39.904989 |
| province | string |  | - | 省份名称，用于辅助名称查询。 | 山东省 |
| city | string |  | - | 城市名称，用于辅助名称查询。 | 济南市 |
| district | string |  | - | 区县名称，用于名称查询，与 district_id、location 三者必填其一。 | 历下区 |
| ak | string | T | - | 开发者密钥，在API控制台申请获得。 | hhR4GDGHfREwblbolOYhio8HkHyRdDoq |
| data_type | string (enum: now, fc, index, alert, fc_hour...) | T | - | 请求数据类型，控制返回内容。可选值：now(实时天气)、fc(7天预报)、index(生活指数)、alert(气象预警)、fc_hour(逐小时预报)、all(全部)。 | all |
| output | string (enum: json, xml) |  | json | 返回格式，支持 json/xml，默认为 json。 | json |
| coordtype | string (enum: wgs84, bd09ll, bd09mc, gcj02) |  | wgs84 | 坐标类型。支持 wgs84/bd09ll/bd09mc/gcj02，默认为 wgs84。 | wgs84 |
| callback | string |  | - | JSONP 回调函数名，当 output=json 时有效。 | showWeather |

### 响应结果

#### 响应示例 (供参考)

```json
{
  "result": {
    "now": {
      "rh": 73,
      "aqi": 140,
      "vis": 3471,
      "pm25": 107,
      "temp": 4,
      "text": "多云",
      "clouds": 999999,
      "uptime": "20200220143500",
      "prec_1h": 0,
      "wind_dir": "东风",
      "feels_like": 1,
      "wind_class": "2级"
    },
    "alerts": [
      {
        "desc": "市气象局发布道路冰雪蓝色预警信号...",
        "type": "道路冰雪",
        "level": "蓝色预警",
        "title": "市气象局发布道路冰雪蓝色预警[IV级/一般]"
      }
    ],
    "indexes": [
      {
        "name": "晨练指数",
        "brief": "较适宜",
        "detail": "天气阴沉，请避免在林中晨练。"
      }
    ],
    "location": {
      "id": "110101",
      "city": "北京市",
      "name": "东城",
      "country": "中国",
      "province": "北京市"
    },
    "forecasts": [
      {
        "aqi": 93,
        "low": -2,
        "date": "2020-02-20",
        "high": 7,
        "week": "星期四",
        "wc_day": "<3级",
        "wd_day": "东南风",
        "text_day": "多云",
        "wc_night": "<3级",
        "wd_night": "北风",
        "text_night": "阴"
      }
    ]
  },
  "status": 0
}
```

#### 响应字段定义 (基于 Schema)

| 字段路径 | 类型 | 必填 | 说明 | 示例 |
|----------|------|------|------|------|
| `message` | string |  | 状态信息描述 | success |
| `result` | object |  | 天气查询结果 | None |
| `result.alerts` | array |  | 气象预警数组，data_type=alert/all 时返回 | None |
| `result.alerts[].desc` | string |  | 预警详细描述 | None |
| `result.alerts[].level` | string |  | 预警等级 | 蓝色预警 |
| `result.alerts[].title` | string |  | 预警标题 | None |
| `result.alerts[].type` | string |  | 预警事件类型 | 道路冰雪 |
| `result.forecast_hours` | array |  | 未来24小时逐小时预报，data_type=fc_hour/all 时返回 | None |
| `result.forecast_hours[].clouds` | integer |  | 云量（%） | None |
| `result.forecast_hours[].data_time` | string |  | 数据时间 | None |
| `result.forecast_hours[].prec_1h` | number |  | 1小时累计降水量（mm） | None |
| `result.forecast_hours[].rh` | integer |  | 相对湿度 | None |
| `result.forecast_hours[].temp_fc` | integer |  | 温度（℃） | None |
| `result.forecast_hours[].text` | string |  | 天气现象 | None |
| `result.forecast_hours[].wind_class` | string |  | 风力等级 | None |
| `result.forecast_hours[].wind_dir` | string |  | 风向描述 | None |
| `result.forecasts` | array |  | 7天预报数组，data_type=fc/all 时返回 | None |
| `result.forecasts[].aqi` | integer |  | 空气质量指数 | 93 |
| `result.forecasts[].date` | string |  | 日期，北京时区 | 2020-02-20 |
| `result.forecasts[].high` | integer |  | 最高温度（℃） | 7 |
| `result.forecasts[].low` | integer |  | 最低温度（℃） | -2 |
| `result.forecasts[].text_day` | string |  | 白天天气现象 | 多云 |
| `result.forecasts[].text_night` | string |  | 夜间天气现象 | 阴 |
| `result.forecasts[].wc_day` | string |  | 白天风力 | <3级 |
| `result.forecasts[].wc_night` | string |  | 夜间风力 | <3级 |
| `result.forecasts[].wd_day` | string |  | 白天风向 | 东南风 |
| `result.forecasts[].wd_night` | string |  | 夜间风向 | 北风 |
| `result.forecasts[].week` | string |  | 星期 | 星期四 |
| `result.indexes` | array |  | 生活指数数组，data_type=index/all 时返回 | None |
| `result.indexes[].brief` | string |  | 概要说明 | 较适宜 |
| `result.indexes[].detail` | string |  | 详细说明 | 天气阴沉，请避免在林中晨练。 |
| `result.indexes[].name` | string |  | 指数名称 | 晨练指数 |
| `result.location` | object |  | 查询位置信息。行政区划查询时含 country/province/city/name/id；经纬度查询时含 lng/lat | None |
| `result.location.city` | string |  | 城市名称 | 北京市 |
| `result.location.country` | string |  | 国家名称 | 中国 |
| `result.location.id` | string |  | 区县行政区划编码 | 110101 |
| `result.location.lat` | number |  | 纬度（经纬度查询时返回） | 39.904989 |
| `result.location.lng` | number |  | 经度（经纬度查询时返回） | 116.405285 |
| `result.location.name` | string |  | 区县名称 | 东城 |
| `result.location.province` | string |  | 省份名称 | 北京市 |
| `result.now` | object |  | 实时天气数据，data_type=now/all 时返回 | None |
| `result.now.aqi` | integer |  | 空气质量指数 | 140 |
| `result.now.clouds` | integer |  | 云量（%） | 999999 |
| `result.now.co` | number |  | 一氧化碳浓度（mg/m³） | None |
| `result.now.feels_like` | integer |  | 体感温度（℃） | 1 |
| `result.now.no2` | integer |  | 二氧化氮浓度（μg/m³） | None |
| `result.now.o3` | integer |  | 臭氧浓度（μg/m³） | None |
| `result.now.pm10` | integer |  | PM10浓度（μg/m³） | None |
| `result.now.pm25` | integer |  | PM2.5浓度（μg/m³） | 107 |
| `result.now.prec_1h` | number |  | 1小时累计降水量（mm） | 0 |
| `result.now.rh` | integer |  | 相对湿度（%） | 73 |
| `result.now.so2` | integer |  | 二氧化硫浓度（μg/m³） | None |
| `result.now.temp` | integer |  | 温度（℃） | 4 |
| `result.now.text` | string |  | 天气现象 | 多云 |
| `result.now.uptime` | string |  | 数据更新时间，北京时间 | 20200220143500 |
| `result.now.vis` | integer |  | 能见度（m） | 3471 |
| `result.now.wind_class` | string |  | 风力等级 | 2级 |
| `result.now.wind_dir` | string |  | 风向描述 | 东风 |
| `status` | integer |  | 请求状态码，0表示成功<br/><br/>**枚举值说明：**<br/>`0`: 成功<br/>`1`: AK参数错误：AK不存在或非法<br/>`2`: 服务内部错误：服务器内部错误，请稍后重试<br/>`3`: 位置参数错误：location/district_id/district 参数格式错误或无效<br/>`4`: 坐标类型错误：coordtype 参数值不在允许范围内<br/>`5`: 无权限：该AK没有权限调用此服务<br/>`101`: 服务禁用：服务已被禁用<br/>`102`: 请求超限：访问频次超限 | 0 |

### 常见问题

**Q: district_id、location、district 三个参数如何选择？**

A: 三者必填其一。district_id 用于行政区划编码查询；location 用于经纬度查询；district 用于区县名称查询，可配合 province、city 辅助定位。

**Q: location 参数的格式是什么？**

A: 经纬度，经度在前纬度在后，逗号分隔，例如 "116.405285,39.904989"。坐标类型由 coordtype 指定。

**Q: data_type 各取值分别返回什么数据？**

A: now: 实时天气；fc: 7天预报；index: 生活指数；alert: 气象预警；fc_hour: 24小时逐小时预报；all: 全部数据。

**Q: 如果 district_id 和 location 同时传会怎样？**

A: 默认以 district_id 为准。

**Q: 生活指数包含哪些字段？**

A: 每项包含 name(名称)、brief(概要)、detail(详细说明)。
