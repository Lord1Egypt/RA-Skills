# 百度地图全球逆地理编码 API

## 服务概述

全球逆地理编码服务提供将坐标点（经纬度）转换为对应位置信息（如所在行政区划，周边地标点分布）功能。自2024年10月起，服务提供灵活的行政区划数据源选项（统计局或民政部）。用户可根据需要控制是否召回POI、道路数据，并选择POI排序策略、坐标类型、返回语言等。

- **版本**: 2.0.0
- **服务标识**: `global_reverse_geocoding`
- **官方文档**: <https://lbs.baidu.com/faq/api?title=webapi/guide/webservice-geocoding-abroad-base>

### API调用

**GET** `https://api.map.baidu.com/reverse_geocoding/v3/`

### 输入参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 | 示例 |
|--------|------|------|--------|------|------|
| ak | string | T | - | 用户申请注册的访问密钥（Access Key）。 | 您的AK |
| location | string | T | - | 需要解析的经纬度坐标，格式为“纬度,经度”。 | 38.76623,116.43213 |
| poi_types | string |  | - | 控制返回附近POI类型，需配合extensions_poi=1使用。多个类型用‘\|’分割，不传则返回全部类型。 | 酒店|房地产 |
| extensions_poi | integer (enum: 0, 1) |  | - | 是否召回POI数据。0：不召回；1：召回（默认周边1000米内POI），并返回语义化描述和包含POI的结构化地址。 | 1 |
| radius | integer |  | 1000 | POI召回半径（米），需配合extensions_poi=1使用。允许设置区间为0-3000，超过按3000处理。 | 500 |
| extensions_road | boolean |  | False | 是否召回坐标周围最近的3条道路数据。 | True |
| region_data_source | integer (enum: 1, 2) |  | 2 | 行政区划数据来源。1：统计局（含开发区）；2：民政部（不含开发区）。 | 2 |
| entire_poi | integer |  | - | 设置该参数可召回更多POI，优化formatted_address_poi的结果，需与sort_strategy参数配合使用。 | 1 |
| sort_strategy | string (enum: distance, rank, default) |  | distance | 配合entire_poi使用，对POI结果排序（影响formatted_address_poi）。可选：distance（距离）、rank（重要性）、default（综合）。 | rank |
| coordtype | string (enum: bd09ll, bd09mc, gcj02ll, wgs84ll) |  | bd09ll | 传入坐标的坐标系类型。 | gcj02ll |
| ret_coordtype | string (enum: bd09ll, gcj02ll, bd09mc) |  | bd09ll | 返回结果的坐标系类型。 | gcj02ll |
| sn | string |  | - | 当所用AK的校验方式为SN校验时，此参数必须。 | - |
| output | string (enum: json, xml) |  | xml | 返回数据的格式。 | json |
| callback | string |  | - | 用于JSONP跨域请求的回调函数名。 | showLocation |
| language | string |  | en | 指定返回结果的语言。国内默认zh-CN，海外默认en。支持多种语言代码。 | zh-CN |
| language_auto | integer (enum: 0, 1) |  | - | 当指定language参数时，是否自动填充未覆盖语言的行政区划数据。1：填充；0：不填充。 | 1 |

### 响应结果

#### 响应示例 (供参考)

```json
{
  "result": {
    "edz": {
      "name": ""
    },
    "pois": [],
    "roads": [],
    "business": "姚家园",
    "cityCode": 131,
    "location": {
      "lat": 39.95133518263271,
      "lng": 116.51484487904992
    },
    "poiRegions": [],
    "business_info": [
      {
        "name": "姚家园",
        "adcode": 110105,
        "distance": "0",
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
      "distance": "",
      "district": "朝阳区",
      "province": "北京市",
      "direction": "",
      "town_code": "110105030",
      "city_level": 2,
      "country_code": 0,
      "street_number": "",
      "country_code_iso": "CHN",
      "country_code_iso2": "CN"
    },
    "formatted_address": "北京市朝阳区东坝路",
    "sematic_description": "",
    "formatted_address_poi": ""
  },
  "status": 0
}
```

#### 响应字段定义 (基于 Schema)

| 字段路径 | 类型 | 必填 | 说明 | 示例 |
|----------|------|------|------|------|
| `result` | object |  | 返回的结果对象。 |  |
| `result.addressComponent` | object |  | 地址组成成分对象。注意：国外行政区划字段仅代表层级。 |  |
| `result.addressComponent.adcode` | integer \| null |  | 行政区划代码。 | 110105 |
| `result.addressComponent.city` | string \| null |  | 城市名。如果坐标在省辖县或县级市，此字段可能为空。 | 北京市 |
| `result.addressComponent.city_level` | integer \| null |  | 城市所在级别（主要对国外有参考意义，0-4分别对应country, province, city, district, town）。 | 2 |
| `result.addressComponent.country` | string \| null |  | 国家名称。 | 中国 |
| `result.addressComponent.country_code` | integer \| null |  | 国家编码。 | 0 |
| `result.addressComponent.country_code_iso` | string \| null |  | 国家英文缩写（三位）。 | CHN |
| `result.addressComponent.country_code_iso2` | string \| null |  | 国家英文缩写（两位）。 | CN |
| `result.addressComponent.direction` | string \| null |  | 相对当前坐标点的方向（当有门牌号时返回）。 |  |
| `result.addressComponent.distance` | string \| null |  | 相对当前坐标点的距离（当有门牌号时返回）。 |  |
| `result.addressComponent.district` | string \| null |  | 区县名。 | 朝阳区 |
| `result.addressComponent.province` | string \| null |  | 省名。 | 北京市 |
| `result.addressComponent.street` | string \| null |  | 道路名。 | 东坝路 |
| `result.addressComponent.street_number` | string \| null |  | 道路门牌号。 |  |
| `result.addressComponent.town` | string \| null |  | 乡镇名。 | 东风(地区)乡 |
| `result.addressComponent.town_code` | string \| null |  | 乡镇ID。 | 110105030 |
| `result.addressComponent.village` | string \| null |  | 社区、村（需商用授权开通）。 |  |
| `result.addressComponent.village_code` | string \| null |  | 社区、村ID（需商用授权开通）。 |  |
| `result.business` | string \| null |  | 坐标所在商圈信息，最多返回3个，以逗号分隔。 | 姚家园 |
| `result.business_info` | array \| null |  | 商圈详细信息数组。 |  |
| `result.business_info[]` | object |  |  | None |
| `result.business_info[].direction` | string \| null |  | 参考位置到输入坐标的方位关系。 | 内 |
| `result.business_info[].distance` | string \| null |  | 参考位置到输入坐标的直线距离。 | 0 |
| `result.business_info[].location` | object |  | 商圈中心点经纬度坐标。 |  |
| `result.business_info[].location.lat` | number |  | 纬度。 | 39.94628680620237 |
| `result.business_info[].location.lng` | number |  | 经度。 | 116.5085279048735 |
| `result.business_info[].name` | string |  | 商圈名称。 | 姚家园 |
| `result.cityCode` | integer \| null |  | 百度定义的城市ID（建议使用adcode）。 | 131 |
| `result.edz` | object |  | 所属开发区信息对象。 |  |
| `result.edz.name` | string \| null |  | 开发区/工业区等非行政区划区域名称。 |  |
| `result.formatted_address` | string \| null |  | 标准的结构化地址（不包含POI信息）。 | 北京市朝阳区东坝路 |
| `result.formatted_address_poi` | string \| null |  | 详细的结构化地址（包含POI信息），需设置extensions_poi=1才能返回。 | 四川省成都市青羊区西御河街道成都市实验小学(人民中路校区) |
| `result.location` | object |  | 经纬度坐标对象。 |  |
| `result.location.lat` | number |  | 纬度值。 | 39.95133518263271 |
| `result.location.lng` | number |  | 经度值。 | 116.51484487904993 |
| `result.poiRegions` | array \| null |  | 归属区域面信息数组。 |  |
| `result.poiRegions[]` | object |  |  | None |
| `result.poiRegions[].direction_desc` | string \| null |  | 请求坐标与所归属区域面的相对位置关系。 |  |
| `result.poiRegions[].distance` | string \| null |  | 离坐标点距离。 |  |
| `result.poiRegions[].name` | string |  | 归属区域面名称。 |  |
| `result.poiRegions[].region_area` | string \| null |  | 所属AOI的面积（单位：平方米）。 |  |
| `result.poiRegions[].tag` | string \| null |  | 归属区域面类型。 |  |
| `result.poiRegions[].uid` | string |  | POI唯一标识。 |  |
| `result.pois` | array \| null |  | 周边POI数组，需设置extensions_poi=1。 |  |
| `result.pois[]` | object |  |  | None |
| `result.pois[].addr` | string \| null |  | POI地址信息。 |  |
| `result.pois[].aoi_name` | string \| null |  | POI所属的AOI名称（当entire_poi=1时返回）。 |  |
| `result.pois[].cp` | string \| null |  | 数据来源（已废弃）。 |  |
| `result.pois[].direction` | string \| null |  | 和当前坐标点的方向。 |  |
| `result.pois[].distance` | string \| null |  | 离坐标点距离。 |  |
| `result.pois[].name` | string |  | POI名称。 |  |
| `result.pois[].parent_poi` | object \| null |  | POI对应的主点POI信息（如无则为空）。 |  |
| `result.pois[].point` | number \| null |  | POI坐标{x,y}。 |  |
| `result.pois[].popularity_level` | string \| null |  | POI的热度值，1-9代表热度从低到高。 |  |
| `result.pois[].tag` | string \| null |  | POI详细类型，如‘美食;中餐厅’。 |  |
| `result.pois[].tel` | string \| null |  | 电话。 |  |
| `result.pois[].uid` | string |  | POI唯一标识。 |  |
| `result.pois[].zip` | string \| null |  | 邮编。 |  |
| `result.roads` | array \| null |  | 周边道路信息数组，需设置extensions_road=true。 |  |
| `result.roads[]` | object |  |  | None |
| `result.roads[].direction` | string \| null |  | 输入点和道路的相对方向。 |  |
| `result.roads[].distance` | string \| null |  | 传入坐标点距离道路的大概距离。 |  |
| `result.roads[].location` | string \| null |  | 坐标点。 |  |
| `result.roads[].name` | string |  | 周边道路名称。 |  |
| `result.sematic_description` | string \| null |  | 当坐标定位到AOI面时，获取AOI面内的具体POI描述，辅助定位。需设置extensions_poi=1。 | 第一郡内,亮晶视光配镜东北258米 |
| `status` | integer |  | 本次API访问状态码，0表示成功，其他值表示失败（具体见错误码表）。<br/><br/>**枚举值说明：**<br/>`0`: ok: 正常<br/>`1`: 服务器内部错误: 该服务响应超时或系统内部错误。<br/>`2`: 参数错误: 坐标类型错误，location格式错误。<br/>`10`: 上传内容超过8M: Post上传数据不能超过8M。<br/>`101`: AK参数不存在: 请求消息没有携带AK参数。<br/>`200`: APP不存在，AK有误: 根据请求的AK，找不到对应的APP。<br/>`210`: APP IP校验失败: 请求IP不在白名单内。<br/>`211`: APP SN校验失败: 请求的SN和服务端计算出来的SN不相等。<br/>`240`: APP 服务被禁用: 该AK没有此服务的权限。<br/>`302`: 天配额超限: 当日调用量超过配额，限制访问。<br/>`401`: 并发量超限: 当前并发量已经超过约定并发配额，限制访问。 | 0 |

### 常见问题

**Q: 如何选择正确的坐标系（coordtype）？**

A: 根据您的数据来源选择：bd09ll（百度地图）、gcj02ll（高德/腾讯等国内地图）、wgs84ll（GPS设备）。传入错误坐标系会导致定位偏移。

**Q: 为什么没有召回POI（pois）数据？**

A: 请检查请求参数是否设置了extensions_poi=1。该参数为0或不设置时，默认不返回POI数据。

**Q: 统计局和民政部的行政区划数据源有什么区别？**

A: 统计局数据包含开发区作为行政区划，适用于社交、电商等场景。民政部数据不包含开发区，适用于政策规划、公共管理等官方场景。可通过region_data_source参数选择。

**Q: 如何开通境外逆地理编码或五级行政区划（社区/村）服务？**

A: 这两项均为高级功能，需要购买商用授权后，通过官方工单系统申请开通。

**Q: 返回状态码（status）非0是什么意思？**

A: status非0表示请求失败。常见原因：AK错误或无权访问（2xx）、配额超限（302）、参数错误（2）。请参考文档中的“服务状态码”表格排查具体原因。
