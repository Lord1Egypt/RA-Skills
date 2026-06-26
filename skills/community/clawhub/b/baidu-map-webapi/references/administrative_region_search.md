# 百度地图地点检索及联想 API

## 服务概述

开发者可通过该功能，检索某一行政区划内（目前最细到区县级别）的地点信息。支持通过关键字、POI类型、区域限制、排序、分页等多种参数进行精细化检索。

- **版本**: 2.0.0
- **服务标识**: `administrative_region_search`
- **官方文档**: <https://lbs.baidu.com/faq/api?title=webapi/guide/webservice-placeapiV3/interfaceDocumentV3>

### API调用

**GET** `https://api.map.baidu.com/place/v3/region`

### 输入参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 | 示例 |
|--------|------|------|--------|------|------|
| query | string | T | - | 检索关键字。 | ATM机、美食 |
| region | string | T | - | 检索行政区划区域（支持到区县级）。增加区域内数据召回权重，如需严格限制召回数据在区域内，请搭配使用region_limit参数。可输入行政区划名或对应citycode。 | 北京市海淀区 |
| ak | string | T | - | 开发者的访问密钥，必填项。v2之前该属性为key。 | 您的AK |
| region_limit | boolean |  | - | 区域数据召回限制，为true时，仅召回region对应区域内数据。 | False |
| is_light_version | boolean |  | False | true：轻量化检索，检索速度大幅提升，排序更简单直接；false（默认）：优化检索结果的排序，使返回的POI更接近百度地图App的推荐顺序，提升结果的相关性和体验。 | False |
| type | string |  | - | 对query召回结果进行二次筛选，type内容建议参考POI分类，建议query同属于一个大类；如query=美食 type=火锅（用于泛搜索场景）。query和type支持只填一项。 | 火锅 |
| center | string |  | - | 传入poi坐标，辅助检索结果按距离排序与返回。需要搭配排序字段一起使用并结合coord_type字段说明该字段的坐标类型。 | 38.76623,116.43213 |
| scope | integer (enum: 1, 2) |  | - | 检索结果详细程度。取值为1 或空，则返回基本信息；取值为2，返回检索POI详细信息。 | - |
| coord_type | integer (enum: 1, 2, 3, 4) |  | 3 | 传入的坐标类型，1（wgs84ll即GPS经纬度），2（gcj02ll即国测局经纬度坐标），3（bd09ll即百度经纬度坐标），4（bd09mc即百度米制坐标）。 | - |
| filter | string |  | - | 检索排序条件，包含以下3部分：industry_type（行业类型：hotel/cater/life）；sort_name（排序方式：default/price/overall_rating/distance）；sort_rule（排序规则：0从高到低，1从低到高）。 | industry_type:cater,sort_name:overall_rating,sort_rule:1 |
| extensions_adcode | boolean |  | - | 是否召回国标行政区划编码。 | False |
| address_result | boolean (enum: false) |  | - | query传入结构化地址时，控制返回数据的类型。若不传入该字段，可能会召回门址数据，当address_result=false时，召回相应的POI数据避免召回门址数据。 | False |
| photo_show | boolean |  | False | 是否输出图片信息：true(输出)，false(不输出)。购买商用授权后可申请开通。 | False |
| from_language | string |  | 中文 | 入参query的语言类型，支持不同语言的检索词作为入参，不填默认为中文，可以设置为auto，大模型会自行判断入参语言。 | auto |
| language | string |  | 中文 | 召回结果的语言类型，支持多种语言召回结果，默认为中文。该功能为高级权限功能。 | en，fr |
| page_num | integer |  | 0 | 分页页码，默认为0,0代表第一页，1代表第二页，以此类推。常与page_size搭配使用，仅当返回结果为poi时可以翻页。 | - |
| page_size | integer |  | 10 | 单次召回POI数量，默认为10条记录，最大返回20条。取值为10-20。 | 10 |
| ret_coordtype | string |  | - | 返回的坐标类型，可选参数，添加后POI返回国测局经纬度坐标。 | gcj02ll |
| output | string (enum: json) |  | json | 输出数据格式，仅支持json。 | json |

### 响应结果

#### 响应示例 (供参考)

```json
{
  "status": 0,
  "message": "ok",
  "results": [
    {
      "uid": "05478f385d3729eef4eafc16",
      "area": "海淀区",
      "city": "北京市",
      "name": "中国银行ATM(北京上地信息路支行)",
      "town": "上地街道",
      "detail": 1,
      "address": "上地信息路15号1层104室",
      "location": {
        "lat": 40.04383967179688,
        "lng": 116.31584460688308
      },
      "province": "北京市",
      "town_code": 110108022
    }
  ],
  "query_type": "general",
  "result_type": "poi_type"
}
```

#### 响应字段定义 (基于 Schema)

| 字段路径 | 类型 | 必填 | 说明 | 示例 |
|----------|------|------|------|------|
| `message` | string |  | 对API访问状态值的英文说明，如果成功返回ok，并返回结果字段，如果失败返回错误说明。 | ok |
| `query_type` | string |  | 搜索类型：精搜precise/泛搜general。 | general |
| `result_type` | string |  | 召回结果类型：region_type 行政区划类型;address_type 结构化地址类型;poi_type poi类型;city_type 城市类型。 | poi_type |
| `results[]` | object |  |  | None |
| `results[].adcode` | integer \| null |  | poi所属区域代码。 | 110101 |
| `results[].address` | string \| null |  | poi所在地址。 | 上地信息路15号1层104室 |
| `results[].area` | string \| null |  | poi所属区县。 | 海淀区 |
| `results[].arrival_heat` | number \| null |  | poi的到达热度（高级权限）。 | 190.65 |
| `results[].city` | string \| null |  | poi所属城市。 | 北京市 |
| `results[].d7_hot_value` | integer \| null |  | poi近7天的热度总值。 | 211 |
| `results[].detail` | string \| null |  | 是否有详情页：1有，0没有。 | 1 |
| `results[].detail_info` | object \| null |  | 详细信息。 |  |
| `results[].detail_info.brand` | string \| null |  | poi对应的品牌。 | 淮扬菜 |
| `results[].detail_info.children[]` | object |  |  | None |
| `results[].detail_info.children[].address` | string \| null |  | poi子点地址。 | 北京市海淀区新建宫门路19号颐和园内 |
| `results[].detail_info.children[].classified_poi_tag` | string \| null |  | poi子点详细分类标签。 | 出入口;门 |
| `results[].detail_info.children[].location` | object \| null |  | poi子点坐标。 |  |
| `results[].detail_info.children[].location.lat` | number |  | 纬度值。 | 40.04383967179688 |
| `results[].detail_info.children[].location.lng` | number |  | 经度值。 | 116.31584460688308 |
| `results[].detail_info.children[].name` | string |  | poi子点名称。 | 颐和园-西门 |
| `results[].detail_info.children[].show_name` | string \| null |  | poi子点简称。 | 西门 |
| `results[].detail_info.children[].uid` | string |  | poi子点ID，可用于poi详情检索。 | 331152d1b94bc54dc41e5148 |
| `results[].detail_info.classified_poi_tag` | string \| null |  | POI展示分类（细致分类）。 | 旅游景点;5A景区 |
| `results[].detail_info.comment_num` | string \| null |  | poi的评论数。 |  |
| `results[].detail_info.description` | string \| null |  | 描述。 |  |
| `results[].detail_info.detail_url` | string \| null |  | poi的详情页。 | http://api.map.baidu.com/place/detail?uid=2a7a2... |
| `results[].detail_info.image_num` | string \| null |  | poi图片数。 | 10 |
| `results[].detail_info.indoor_floor` | string \| null |  | 室内poi所在楼层。 |  |
| `results[].detail_info.label` | string \| null |  | poi权威标签，标签细分解释。 | 淮扬菜 |
| `results[].detail_info.navi_location` | object \| null |  | poi对应的导航引导点坐标（上车点）。 |  |
| `results[].detail_info.navi_location.lat` | number |  | 纬度值。 | 40.04383967179688 |
| `results[].detail_info.navi_location.lng` | number |  | 经度值。 | 116.31584460688308 |
| `results[].detail_info.new_alias` | string \| null |  | poi别名。 | 故宫 |
| `results[].detail_info.overall_rating` | string \| null |  | poi的综合评分。 | 4.7 |
| `results[].detail_info.parent_id` | string \| null |  | poi父点id。 | 06d2dffda107b0ef89f15db6 |
| `results[].detail_info.photos` | array \| null |  | poi图片的下载链接。购买商用授权后可申请开通。 | [] |
| `results[].detail_info.price` | string \| null |  | poi商户的价格。 | 4.7 |
| `results[].detail_info.ranking` | string \| null |  | poi的相关榜单排名。 | 北京市展览馆榜NO.1 |
| `results[].detail_info.shop_hours` | string \| null |  | poi的营业时间。 | 10:30-14:00,16:30-22:00 |
| `results[].detail_info.type` | string \| null |  | 类型，如（hotel、cater、life），配合filter排序。 | hotel |
| `results[].heat_trend` | string \| null |  | 近7天热度增长（递减）XX%（高级权限）。 | 近7天热度递减5% |
| `results[].interact_heat` | number \| null |  | poi的互动热度（高级权限）。 | 36.05 |
| `results[].location` | object \| null |  | poi经纬度坐标。 |  |
| `results[].location.lat` | number |  | 纬度值。 | 40.04383967179688 |
| `results[].location.lng` | number |  | 经度值。 | 116.31584460688308 |
| `results[].name` | string |  | poi名称，单次请求最多返回10条结果。 | 中国银行ATM(北京上地信息路支行) |
| `results[].province` | string \| null |  | poi所属省份。 | 北京市 |
| `results[].status` | string \| null |  | poi营业状态 ：空（代表正常营业）、推算位置、暂停营业、可能已关闭、已关闭。 |  |
| `results[].street_id` | string \| null |  | poi所在街景图id。 | e176ad06ea2a026cd2f49e2c |
| `results[].telephone` | string \| null |  | poi的电话。 |  |
| `results[].town` | string \| null |  | poi所属乡镇街道。 | 上地街道 |
| `results[].town_code` | integer \| null |  | poi所属乡镇街道编码。 | 110108022 |
| `results[].uid` | string |  | poi的唯一标示，ID。 | 05478f385d3729eef4eafc16 |
| `results[].view_heat` | number \| null |  | poi的浏览热度（高级权限）。 | 2302.75 |
| `status` | integer |  | 本次API访问状态，如果成功返回0，如果失败返回其他数字。 | 0 |
| `total` | integer \| null |  | 召回poi数量，开发者请求中设置了page_num字段才会出现total字段。出于数据保护目的，单次请求total最多为150。 |  |

### 常见问题

**Q: 哪些参数是调用此接口时必须填写的？**

A: query（检索关键字）、region（检索区域）和ak（访问密钥）是三个必填参数。

**Q: 如何严格限制检索结果只返回指定区域内的数据？**

A: 除了填写region参数外，还需要将region_limit参数设置为true，这样将仅召回region对应区域内的数据。

**Q: 如何对检索结果进行排序，例如按距离或评分排序？**

A: 可以使用filter参数进行排序。需要指定industry_type（行业）、sort_name（排序字段，如distance或overall_rating）和sort_rule（排序规则）。按距离排序时还需配合center参数提供中心点坐标。

**Q: 接口支持分页吗？最多能获取多少条数据？**

A: 支持分页，使用page_num和page_size参数。page_size默认为10，最大为20。当启用分页时，total字段表示总条数，但出于数据保护，单次请求total最多显示150条。

**Q: 返回结果中的一些字段（如photos、热度数据）为什么是空的？**

A: 部分字段属于高级功能，例如图片信息(photo_show)、多语言检索(language)、热度数据(view_heat等)需要购买商用授权或联系商务提交工单申请开通后才能返回数据。
