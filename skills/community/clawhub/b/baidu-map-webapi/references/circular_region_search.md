# 百度地图地点检索及联想 API

## 服务概述

开发者可设置圆心坐标和半径，检索圆形区域内的地点信息（POI）。支持多关键字并集检索、按POI分类检索、结果排序、分页、多语言检索等高级功能。当检索半径过大，超过中心点所在城市边界时，检索范围会自动变为该城市范围。

- **版本**: 2.0.0
- **服务标识**: `circular_region_search`
- **官方文档**: <https://lbs.baidu.com/faq/api?title=webapi/guide/webservice-placeapiV3/interfaceDocumentV3>

### API调用

**GET** `https://api.map.baidu.com/place/v3/around`

### 输入参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 | 示例 |
|--------|------|------|--------|------|------|
| query | string | T | - | 检索关键字。支持多个关键字并集检索，不同关键字间以$符号分隔，最多10个。也可通过POI分类进行检索。 | 银行 |
| location | string | T | - | 圆形区域检索中心点经纬度坐标，格式为“纬度,经度”。不支持多个点。 | 39.915,116.404 |
| ak | string | T | - | 开发者的访问密钥（API Key），必填项。 | 您的AK |
| radius | integer |  | 1000 | 圆形区域检索半径，单位为米。默认1000。 | 2000 |
| radius_limit | boolean |  | - | 是否严格限定召回结果在设置的检索半径范围内。true（是），false（否）。 | True |
| is_light_version | boolean |  | False | true：优先保证检索速度，排序更简单直接；false（默认）：优化检索结果的排序，使返回的POI更接近百度地图App的推荐顺序。 | True |
| type | string |  | - | 对query召回结果进行二次筛选，内容建议参考POI分类。query和type支持只填一项。 | 火锅 |
| scope | integer (enum: 1, 2) |  | - | 检索结果详细程度。1 或空：返回基本信息；2：返回检索POI详细信息。 | 2 |
| coord_type | integer (enum: 1, 2, 3, 4) |  | 3 | 传入的坐标类型。1：wgs84ll（GPS经纬度）；2：gcj02ll（国测局经纬度）；3：bd09ll（百度经纬度，默认）；4：bd09mc（百度米制坐标）。 | 3 |
| filter | string |  | - | 检索排序条件，格式：industry_type:行业\|sort_name:排序方式\|sort_rule:排序规则。行业：hotel/cater/life；排序方式：default/price/overall_rating/distance；排序规则：0（从高到低）/1（从低到高）。 | industry_type:cater|sort_name:overall_rating|sort_rule:1 |
| extensions_adcode | boolean |  | - | 是否召回国标行政区划编码。true（召回）、false（不召回）。 | True |
| photo_show | boolean |  | False | 是否输出图片信息：true(输出)，false(不输出)。此为高级权限功能。 | False |
| from_language | string |  | zh | query的语言类型，支持不同语言的检索词。不填默认为中文，可设置为auto（自动判断）。 | auto |
| language | string |  | zh | 多语言检索，支持多种语言召回结果。默认为中文。此为高级权限功能。 | en |
| page_num | integer |  | 0 | 分页页码，默认为0（第一页），1代表第二页，以此类推。仅当返回结果为poi时可以翻页。 | 0 |
| page_size | integer |  | 10 | 单次召回POI数量，默认为10条，最大返回20条。取值范围10-20。 | 10 |
| ret_coordtype | string |  | - | 返回的坐标类型，添加后POI返回国测局经纬度坐标（gcj02ll）。 | gcj02ll |
| output | string (enum: json) |  | json | 输出数据格式，仅支持json。 | json |

### 响应结果

#### 响应示例 (供参考)

```json
{
  "status": 0,
  "message": "ok",
  "results": [
    {
      "uid": "14cf81e3aae18d1914948ebb",
      "area": "东城区",
      "city": "北京市",
      "name": "中国民生银行(北京正义路支行)",
      "town": "东华门街道",
      "detail": 1,
      "address": "北京市东城区东长安街35号首层西侧",
      "location": {
        "lat": 39.91518549590169,
        "lng": 116.41350155480602
      },
      "province": "北京市",
      "street_id": "14cf81e3aae18d1914948ebb",
      "telephone": "(010)65284468",
      "town_code": 110101001
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

A: query（检索关键字）、location（中心点坐标）、ak（访问密钥）这三个参数是必须填写的。

**Q: 如果设置的检索半径很大，会有什么影响？**

A: 当半径过大，超过中心点所在城市边界时，检索范围会自动变为该城市范围，而不再严格限定为圆形区域。

**Q: 如何对检索结果进行排序？**

A: 可以使用filter参数进行排序，指定行业类型(industry_type)、排序方式(sort_name)和排序规则(sort_rule)，例如按餐饮行业评分从低到高排序。

**Q: 接口是否支持使用英文或其他语言关键字进行检索？**

A: 支持。通过设置from_language参数（如设为'auto'或指定语种代码）可以传入非中文关键字。通过language参数可以指定返回结果的语种，但此为高级权限功能。

**Q: 如何获取POI的图片、详细热度等高级信息？**

A: 需要购买百度地图的商用授权，然后联系商务提交工单申请开通相应的高级权限（如photo_show、view_heat等字段）。
