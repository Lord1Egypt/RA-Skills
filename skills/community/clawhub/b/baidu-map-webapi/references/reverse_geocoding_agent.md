# 百度地图全球逆地理编码 API

## 服务概述

逆地理编码智能体是在逆地理编码将经纬度坐标转换为详细地址信息，帮助用户精准描述坐标位置的基础上，通过与Deepseek AI大模型结合，利用其强大的推理能力，能够根据不同应用场景智能分析，返回最合理的地址描述结果。同时，新接口简化了原有的参数设计，为开发者提供了更加便捷、易用的调用方式。

- **版本**: 2.0.0
- **服务标识**: `reverse_geocoding_agent`
- **官方文档**: <https://lbs.baidu.com/faq/api?title=webapi/guide/webservice-geocoding-abroad-agent>

### API调用

**GET** `https://api.map.baidu.com/reverse_geocoding/agent`

### 输入参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 | 示例 |
|--------|------|------|--------|------|------|
| ak | string | T | - | 用户申请注册的key，自v2开始参数修改为”ak”，之前版本参数为”key”。 | 您的AK |
| location | string | T | - | 根据经纬度坐标获取地址，格式为“纬度,经度”。 | 40.014523,116.309781 |
| coordtype | string (enum: bd09ll, bd09mc, gcj02ll, wgs84ll) |  | bd09ll | 传入的坐标类型，支持bd09ll（百度经纬度坐标）、bd09mc（百度米制坐标）、gcj02ll（国测局经纬度坐标，仅限中国）、wgs84ll（GPS经纬度）。 | bd09ll |
| ret_coordtype | string (enum: bd09ll, gcj02ll, bd09mc) |  | bd09ll | 返回的坐标类型，可选参数，添加后返回国测局经纬度坐标或百度米制坐标。 | bd09ll |
| demand | string | T | - | 用户的需求描述，可以加入对场景、偏好等描述，提升解析的精准度和匹配度，返回更贴合实际需求的结果。 | 我在打车，需要告诉司机我现在的位置 |

### 响应结果

#### 响应示例 (供参考)

```json
{
  "result": {
    "pois": [
      {
        "cp": " ",
        "tag": "美食;快餐店",
        "tel": "",
        "uid": "f9d184332acef8946240a94b",
        "zip": "",
        "addr": "东坝路朝阳站2层7-2号",
        "name": "永和大王(北京朝阳站店)",
        "point": {
          "lat": 0,
          "lng": 0
        },
        "poiType": "美食",
        "aoi_name": "姚家园",
        "distance": "43",
        "direction": "附近",
        "parent_poi": {
          "cp": "",
          "tag": "交通设施;火车站",
          "tel": "",
          "uid": "e4728174d1f54500acb22a87",
          "zip": "",
          "addr": "北京市朝阳区姚家园北路",
          "name": "北京朝阳站",
          "point": {
            "lat": 0,
            "lng": 0
          },
          "poiType": "",
          "aoi_name": "",
          "distance": "0",
          "direction": "附近",
          "popularity_level": "9"
        },
        "popularity_level": "9"
      }
    ],
    "roads": [
      {
        "name": "东坝路",
        "distance": "182",
        "location": {
          "lat": 39.94998794222986,
          "lng": 116.51618607030608
        },
        "direction": "西北"
      },
      {
        "name": "朝阳站路",
        "distance": "193",
        "location": {
          "lat": 39.95305567757272,
          "lng": 116.51441450621228
        },
        "direction": "南"
      }
    ],
    "location": {
      "lat": 39.95133518263271,
      "lng": 116.51484487904992
    },
    "poiRegions": [
      {
        "tag": "交通设施;火车站",
        "uid": "e4728174d1f54500acb22a87",
        "name": "北京朝阳站",
        "distance": "0",
        "direction_desc": "内"
      }
    ],
    "business_info": [
      {
        "name": "姚家园",
        "adcode": 110105,
        "distance": 0,
        "location": {
          "lat": 39.94628680620237,
          "lng": 116.5085279048735
        },
        "direction": "内"
      }
    ],
    "addressComponent": {
      "city": "北京市",
      "town": "东风(地区)乡",
      "adcode": "110105",
      "street": "东坝路",
      "country": "中国",
      "district": "朝阳区",
      "province": "北京市",
      "town_code": "110105030",
      "city_level": 2,
      "country_code": 0,
      "street_number": "",
      "country_code_iso": "CHN",
      "country_code_iso2": "CN"
    },
    "recommend_reason": "永和大王（Beijing Chaoyang Station）距离用户仅43m，是最近的美食类POI。",
    "recommend_address_poi": "北京市朝阳区东风(地区)乡永和大王(北京朝阳站店)(附近方向43米)"
  },
  "status": 0
}
```

#### 响应字段定义 (基于 Schema)

| 字段路径 | 类型 | 必填 | 说明 | 示例 |
|----------|------|------|------|------|
| `result` | object |  | 返回的结果 | None |
| `result.addressComponent` | object |  | 地址组成成分，注意国外行政区划字段仅代表层级。 | None |
| `result.addressComponent.adcode` | integer |  | 行政区划代码 | 110105 |
| `result.addressComponent.city` | string \| null |  | 城市名，如果经纬度所在城市是省辖县或者省辖县级市，返回的city结果为空。 | 北京市 |
| `result.addressComponent.country` | string |  | 国家 | 中国 |
| `result.addressComponent.direction` | string \| null |  | 相对当前坐标点的方向，当有门牌号的时候返回数据 |  |
| `result.addressComponent.distance` | string \| null |  | 相对当前坐标点的距离，当有门牌号的时候返回数据 |  |
| `result.addressComponent.district` | string |  | 区县名 | 朝阳区 |
| `result.addressComponent.province` | string |  | 省名 | 北京市 |
| `result.addressComponent.street` | string |  | 道路名 | 东坝路 |
| `result.addressComponent.street_number` | string \| null |  | 道路门牌号 |  |
| `result.addressComponent.town` | string |  | 乡镇名 | 东风(地区)乡 |
| `result.addressComponent.town_code` | string |  | 乡镇id | 110105030 |
| `result.addressComponent.village` | string \| null |  | 社区、村（购买商用授权后可申请开通） |  |
| `result.addressComponent.village_code` | string \| null |  | 社区、村id |  |
| `result.business_info` | array |  | 商圈信息数组 | None |
| `result.business_info[]` | object |  |  | None |
| `result.business_info[].direction` | string |  | 参考位置到输入坐标的方位关系，如北、南、内等 | 内 |
| `result.business_info[].distance` | string |  | 参考位置到输入坐标的直线距离 | 0 |
| `result.business_info[].location` | object |  | 商圈中心点经纬度坐标 | None |
| `result.business_info[].location.lat` | number |  | 纬度值 | 39.94628680620237 |
| `result.business_info[].location.lng` | number |  | 经度值 | 116.5085279048735 |
| `result.business_info[].name` | string |  | 商圈名称 | 姚家园 |
| `result.location` | object |  | 经纬度坐标 | None |
| `result.location.lat` | number |  | 纬度值 | 39.95133518263271 |
| `result.location.lng` | number |  | 经度值 | 116.51484487904993 |
| `result.poiRegions` | array |  | 归属区域面信息列表 | None |
| `result.poiRegions[]` | object |  |  | None |
| `result.poiRegions[].direction_desc` | string |  | 请求中的坐标与所归属区域面的相对位置关系 | 内 |
| `result.poiRegions[].distance` | string |  | 离坐标点距离 | 0 |
| `result.poiRegions[].name` | string |  | 归属区域面名称 | 北京朝阳站 |
| `result.poiRegions[].tag` | string |  | 归属区域面类型 | 交通设施;火车站 |
| `result.poiRegions[].uid` | string |  | poi唯一标识 | e4728174d1f54500acb22a87 |
| `result.pois` | array |  | 周边poi数组（最多返回10条POI，大模型选择的POI在第一条） | None |
| `result.pois[]` | object |  |  | None |
| `result.pois[].addr` | string |  | 地址信息 | 东坝路朝阳站2层7-2号 |
| `result.pois[].direction` | string |  | 和当前坐标点的方向 | 附近 |
| `result.pois[].distance` | string |  | 离坐标点距离 | 43 |
| `result.pois[].name` | string |  | poi名称 | 永和大王(北京朝阳站店) |
| `result.pois[].point` | object |  | poi坐标，包含lng和lat | None |
| `result.pois[].point.lat` | number |  | 纬度值 | 0 |
| `result.pois[].point.lng` | number |  | 经度值 | 0 |
| `result.pois[].tag` | string |  | poi类型，如‘美食;中餐厅’。tag与poiType字段均为poi类型，建议使用tag字段，信息更详细。 | 美食;快餐店 |
| `result.pois[].tel` | string \| null |  | 电话 |  |
| `result.pois[].uid` | string |  | poi唯一标识 | f9d184332acef8946240a94b |
| `result.recommend_address_poi` | string |  | 大模型推荐的结构化地址（包含POI信息） | 北京市朝阳区东风(地区)乡永和大王(北京朝阳站店)(附近方向43米) |
| `result.recommend_reason` | string |  | 大模型推荐的原因 | 永和大王（Beijing Chaoyang Station）距离用户仅43m，是最近的美食类POI。 |
| `result.roads` | array |  | 道路信息数组 | None |
| `result.roads[]` | object |  |  | None |
| `result.roads[].direction` | string |  | 输入点和道路的相对方向 | 西北 |
| `result.roads[].distance` | string |  | 传入的坐标点距离道路的大概距离 | 182 |
| `result.roads[].location` | object |  | 坐标点 | None |
| `result.roads[].location.lat` | number |  | 纬度值 | 39.94998794222986 |
| `result.roads[].location.lng` | number |  | 经度值 | 116.51618607030609 |
| `result.roads[].name` | string |  | 周边道路名称 | 东坝路 |
| `status` | integer |  | 本次API访问状态，如果成功返回0，如果失败返回其他数字。<br/><br/>**枚举值说明：**<br/>`0`: ok: 正常<br/>`1`: 服务器内部错误: 该服务响应超时或系统内部错误<br/>`2`: 参数错误: 坐标类型错误，location格式错误<br/>`10`: 上传内容超过8M: Post上传数据不能超过8M<br/>`101`: AK参数不存在: 请求消息没有携带AK参数<br/>`102`: MCODE参数不存在: 对于Mobile类型的应用请求需要携带mcode参数<br/>`200`: APP不存在: 根据请求的AK，找不到对应的APP<br/>`201`: APP被用户自己禁用: 请在控制台解禁<br/>`202`: APP被管理员删除: 恶意APP被管理员删除<br/>`203`: APP类型错误: 当前API控制台支持Server、Mobile及Browser类型，其他类型错误 | 0 |

### 常见问题

**Q: 如何申请AK？**

A: 访问百度地图开放平台，注册账号并创建应用，即可在控制台获取AK。

**Q: demand参数有什么作用？**

A: demand参数用于描述用户需求场景（如打车、导航），帮助AI模型更精准地分析并返回合适的地址描述。

**Q: 支持哪些坐标类型？**

A: 支持bd09ll（百度经纬度坐标）、bd09mc（百度米制坐标）、gcj02ll（国测局坐标，仅限中国）、wgs84ll（GPS坐标）。

**Q: 返回的POI信息最多有多少条？**

A: pois数组最多返回10条POI，其中大模型选择的POI在第一条。

**Q: 如何提高地址描述的准确性？**

A: 在demand参数中详细描述场景和偏好（如“我在打车，需要告诉司机我现在的位置”），可提升解析精准度。
