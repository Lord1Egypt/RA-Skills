# 百度地图地点检索及联想 API

## 服务概述

多维检索接口能够理解用户输入的自然语言多条件查询（例如“可以带狗的餐厅”、“适合自驾的旅游景点”），通过语义分析和模糊匹配，从海量POI数据中召回最相关的结果。该接口支持按区域、类型、坐标、排序条件等多种维度进行筛选和排序，并返回丰富的POI详细信息。

- **版本**: 2.0.0
- **服务标识**: `content_search`
- **官方文档**: <https://lbs.baidu.com/faq/api?title=webapi/guide/webservice-placeapiV3/multidimensional>

### API调用

**GET** `https://api.map.baidu.com/api_place_pro/v1/region`

### 输入参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 | 示例 |
|--------|------|------|--------|------|------|
| query | string | T | - | 检索关键字，支持自然语言多定语查询。 | 宠物友好餐厅 |
| region | string | T | - | 限定搜索区域，如城市名。 | 北京市 |
| region_limit | boolean |  | False | 区域数据召回限制。为true时，仅召回region对应区域内数据。 | True |
| type | string |  | - | 对query召回结果进行二次筛选，建议参考POI分类。query和type支持只填一项。 | 火锅 |
| scope | integer (enum: 1, 2) |  | - | 检索结果详细程度。1或空返回基本信息；2返回POI详细信息。 | 2 |
| coord_type | integer (enum: 1, 2, 3, 4) |  | 3 | 传入的坐标类型。1: wgs84ll(GPS), 2: gcj02ll(国测局), 3: bd09ll(百度，默认), 4: bd09mc(百度米制)。 | 3 |
| center | string |  | - | 传入POI坐标（纬度,经度），辅助检索结果按距离排序，需搭配filter排序字段和coord_type使用。 | 38.76623,116.43213 |
| filter | string |  | - | 检索排序条件，格式为 industry_type:行业类型;sort_name:排序方式;sort_rule:排序规则。行业类型：hotel(酒店)、cater(餐饮)、life(生活)。排序方式：default(默认)、price(价格)、overall_rating(评分)、distance(距离，需结合center)。排序规则：0(从高到低)、1(从低到高)。 | industry_type:cater;sort_name:overall_rating;sort_rule:1 |
| extensions_adcode | boolean |  | - | 是否召回国标行政区划编码。true召回，false不召回。 | True |
| address_result | boolean (enum: false) |  | - | query传入结构化地址时，控制返回数据类型。默认为true可能会召回门址数据；address_result=false时，召回POI数据。 | False |
| photo_show | boolean |  | False | 是否输出图片信息。true输出，false不输出。此为高级权限功能。 | False |
| language | string |  | - | 多语言检索，支持多种语言召回结果，默认为中文。此为高级权限功能。 | en |
| page_num | integer |  | 0 | 分页页码，0代表第一页，1代表第二页，以此类推。仅当返回结果为poi时可以翻页。 | 0 |
| page_size | integer |  | 10 | 单次召回POI数量，默认为10条，最大返回20条。 | 10 |
| ret_coordtype | string (enum: bd09ll, bd09mc, wgs84ll, gcj02ll) |  | - | 返回的坐标类型，默认返回百度坐标系。 | bd09ll |
| output | string (enum: json, xml) |  | - | 输出数据格式。 | json |
| baidu_user_id | string |  | - | 用户请求id，任意定义，不可超过16位字符串。与baidu_session_id配合使用可实现个性化搜索。 | 12345 |
| baidu_session_id | string |  | - | 百度对话id，任意定义，不可超过16位字符串。用于辨别同一轮请求，优化搜索效果。不可和baidu_user_id相同。 | 67891 |

### 响应结果

#### 响应示例 (供参考)

```json
{
  "total": 30,
  "status": 0,
  "message": "ok",
  "results": [
    {
      "uid": "fc6e4cc3de01b0ff095cb3a5",
      "area": "管城回族区",
      "city": "郑州市",
      "name": "东府饭店(高铁东站黑金冠店)",
      "town": "圃田乡",
      "adcode": "410104",
      "detail": 1,
      "status": "",
      "address": "商鼎路与心怡路交叉口东南角永和宇宙星一楼",
      "location": {
        "lat": 34.76054100923168,
        "lng": 113.78117913246852
      },
      "province": "河南省",
      "street_id": "fc6e4cc3de01b0ff095cb3a5",
      "telephone": "0371-55556818,0371-55558198",
      "town_code": 410104202,
      "match_term": "宠物友好;饭店餐馆;高颜值宴会厅",
      "detail_info": {
        "tag": "美食;中餐厅",
        "type": "cater",
        "brand": "东府饭店",
        "label": "特色菜",
        "price": "75.0",
        "ranking": "郑州市团建聚餐No.2",
        "children": [],
        "parent_id": "242425ad4ec48090132935cd",
        "detail_url": "http://api.map.baidu.com/place/detail?uid=fc6e4cc3de01b0ff095cb3a5&output=html&source=placeapi_v3",
        "shop_hours": "10:00-14:00,17:30-21:30",
        "comment_num": "5",
        "navi_location": {
          "lat": 34.760636600628196,
          "lng": 113.7811511831568
        },
        "overall_rating": "4.8",
        "classified_poi_tag": "美食;中餐馆;特色菜"
      },
      "poi_related_score": 1.8529655933380127
    }
  ],
  "query_type": "general",
  "result_type": "poi_type"
}
```

#### 响应字段定义 (基于 Schema)

| 字段路径 | 类型 | 必填 | 说明 | 示例 |
|----------|------|------|------|------|
| `message` | string |  | 对API访问状态值的英文说明，成功返回ok。 | ok |
| `query_type` | string |  | 搜索类型：精搜precise或泛搜general。 | general |
| `result_type` | string |  | 召回结果类型：region_type(行政区划), address_type(结构化地址), poi_type(poi), city_type(城市)。 | poi_type |
| `results[]` | object |  |  | None |
| `results[].adcode` | integer \| null |  | POI所属区域代码。 | 410104 |
| `results[].address` | string \| null |  | POI所在地址。 | 商鼎路与心怡路交叉口东南角永和宇宙星一楼 |
| `results[].area` | string \| null |  | POI所属区县。 | 管城回族区 |
| `results[].city` | string \| null |  | POI所属城市。 | 郑州市 |
| `results[].detail` | string \| null |  | 是否有详情页：1有，0没有。 | 1 |
| `results[].detail_info` | object \| null |  | POI详细信息对象。 |  |
| `results[].detail_info.brand` | string \| null |  | POI对应的品牌。 | 东府饭店 |
| `results[].detail_info.children[]` | object |  |  | None |
| `results[].detail_info.children[].address` | string \| null |  | POI子点地址。 |  |
| `results[].detail_info.children[].classified_poi_tag` | string \| null |  | POI子点详细分类标签。 |  |
| `results[].detail_info.children[].location` | object \| null |  | POI子点坐标对象。 |  |
| `results[].detail_info.children[].name` | string \| null |  | POI子点名称。 |  |
| `results[].detail_info.children[].show_name` | string \| null |  | POI子点简称。 |  |
| `results[].detail_info.children[].uid` | string \| null |  | POI子点ID，可用于详情检索。 |  |
| `results[].detail_info.classified_poi_tag` | string \| null |  | POI展示分类（细致分类）。 | 美食;中餐馆;特色菜 |
| `results[].detail_info.comment_num` | string \| null |  | POI的评论数。 | 5 |
| `results[].detail_info.detail_url` | string \| null |  | POI的详情页URL。 | http://api.map.baidu.com/place/detail?uid=fc6e4... |
| `results[].detail_info.image_num` | string \| null |  | POI图片数。 |  |
| `results[].detail_info.indoor_floor` | string \| null |  | 室内POI所在楼层。 |  |
| `results[].detail_info.label` | string \| null |  | POI权威标签，如停车场类型、景区等级等。 | 特色菜 |
| `results[].detail_info.navi_location` | object \| null |  | POI对应的导航引导点坐标（上车点）。 |  |
| `results[].detail_info.navi_location.lat` | number \| null |  | 导航点纬度。 | 34.760636600628196 |
| `results[].detail_info.navi_location.lng` | number \| null |  | 导航点经度。 | 113.78115118315681 |
| `results[].detail_info.new_alias` | string \| null |  | POI别名。 | 珍珠Pearl·云南菜(郑州银泰inPARK店) |
| `results[].detail_info.overall_rating` | string \| null |  | POI的综合评分。 | 4.8 |
| `results[].detail_info.parent_id` | string \| null |  | POI父点id。 | 242425ad4ec48090132935cd |
| `results[].detail_info.photos` | array \| null |  | POI图片的下载链接数组。此为高级权限功能。 | [] |
| `results[].detail_info.price` | string \| null |  | POI商户的价格。 | 75.0 |
| `results[].detail_info.ranking` | string \| null |  | POI的相关榜单排名。 | 郑州市团建聚餐No.2 |
| `results[].detail_info.shop_hours` | string \| null |  | POI的营业时间。 | 10:30-14:00,16:30-22:00 |
| `results[].detail_info.type` | string \| null |  | 类型，如hotel、cater、life，配合filter排序。 | cater |
| `results[].location` | object |  | POI经纬度坐标对象。 |  |
| `results[].location.lat` | number |  | 纬度值。 | 34.76054100923168 |
| `results[].location.lng` | number |  | 经度值。 | 113.78117913246851 |
| `results[].match_term` | string \| null |  | 多维检索匹配标签。 | 宠物友好;饭店餐馆;高颜值宴会厅 |
| `results[].name` | string |  | POI名称。 | 东府饭店(高铁东站黑金冠店) |
| `results[].poi_related_score` | number \| null |  | POI匹配置信度。1.8以上非常满足，1.5以上比较满足，0.8-1.5一般满足，0.8以下不满足。 | 1.8529655933380127 |
| `results[].province` | string \| null |  | POI所属省份。 | 河南省 |
| `results[].status` | string \| null |  | POI营业状态，空代表正常营业。其他状态如暂停营业等为高级权限功能。 |  |
| `results[].telephone` | string \| null |  | POI的电话。 | 0371-55556818,0371-55558198 |
| `results[].town` | string \| null |  | POI所属乡镇街道。 | 圃田乡 |
| `results[].town_code` | integer \| null |  | POI所属乡镇街道编码。 | 410104202 |
| `results[].uid` | string |  | POI的唯一标识ID。 | fc6e4cc3de01b0ff095cb3a5 |
| `status` | integer |  | 本次API访问状态，成功返回0，失败返回其他数字。 | 0 |
| `total` | integer \| null |  | 召回POI总数。设置了page_num字段才会出现，单次请求最多为150。 | 30 |

### 常见问题

**Q: query 和 region 参数是否必须同时提供？**

A: 是的，query（检索关键字）和 region（限定区域）都是必选参数，必须同时提供才能进行有效检索。

**Q: 如何对结果进行翻页？**

A: 使用 page_num 和 page_size 参数。page_num 从0开始（0为第一页），page_size 控制每页数量（10-20条）。仅当返回结果为 poi 类型时可以翻页。

**Q: 如何让返回结果按距离、价格或评分排序？**

A: 使用 filter 参数。需要指定 industry_type（行业）、sort_name（排序字段，如 distance, price, overall_rating）和 sort_rule（0降序/1升序）。按距离排序时还需提供 center 参数。

**Q: 单次请求最多能返回多少条POI？total字段显示150是什么意思？**

A: 单次请求通过 page_size 最多返回20条POI记录。total 字段表示符合条件的所有POI总数，但出于数据保护，该值单次请求最多显示为150。

**Q: 如何开通图片、多语言、营业状态等高级功能？**

A: 图片（photo_show）、多语言（language）、详细营业状态（status）等为高级权限功能。购买商用授权后，需联系百度地图商务，并通过提交工单申请开通。
