# 百度地图地点检索及联想 API

## 服务概述

地点输入提示服务（又名Place Suggestion API）是一类Web API接口服务。它匹配用户输入内容，提供输入提示功能。常与地点检索服务搭配使用，也可作为轻量级地点检索服务单独使用（不支持复杂检索场景）。用户可通过该服务，匹配用户输入关键词的地点推荐列表。注意：请通过检索接口实时获取POI数据UID进行详情检索。

- **版本**: 2.0.0
- **服务标识**: `place_input_suggestion`
- **官方文档**: <https://lbs.baidu.com/faq/api?title=webapi/guide/webservice-placeapiV3/interfaceDocumentV3>

### API调用

**GET** `https://api.map.baidu.com/place/v3/suggestion`

### 输入参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 | 示例 |
|--------|------|------|--------|------|------|
| query | string | T | - | 输入建议关键字（支持拼音）。 | 上地、天安、中关、shanghai |
| region | string |  | - | 检索行政区划区域（仅支持到市级）。可输入行政区划名或对应citycode。增加区域内数据召回权重，如需严格限制召回数据在区域内，请搭配使用region_limit参数。region/location/bounds必须提供一个 | 北京市 |
| ak | string | T | - | 开发者的访问密钥，必填项。v2之前该属性为key。 | - |
| region_limit | boolean |  | - | 区域数据召回限制，为true时，仅召回region对应区域内数据。 | False |
| location | string |  | - | 传入location参数后，会转为周边检索，但不会严格按距离排序决定最终的排序。格式：纬度,经度。region/location/bounds必须提供一个 | 40.047857537164,116.31353434477 |
| radius | integer |  | 1000 | 圆形区域检索半径，单位为米。当半径过大，超过中心点所在城市边界时，会变为城市范围检索，检索范围为中心点所在城市。 | 1000 |
| bounds | string |  | - | 检索多边形区域。需传入多个坐标对集合，坐标对用','分割，首尾坐标对需相同。多边形为矩形时，可传入左下右上两顶点坐标对。bounds参数范围，最少2对，最大100对坐标。bounds参数在大于2对坐标时，需要首尾相连成闭合多边形。region/location/bounds必须提供一个 | 38.76623,116.43213,40.056878,116.30815,40.465,116.314,40.232,116.352,40.121,116.453,38.76623,116.43213 |
| coord_type | integer (enum: 1, 2, 3, 4) |  | 3 | 传入的坐标类型，1（wgs84ll即GPS经纬度），2（gcj02ll即国测局经纬度坐标），3（bd09ll即百度经纬度坐标），4（bd09mc即百度米制坐标）。 | - |
| extensions_adcode | boolean |  | - | 是否召回国标行政区划编码，true（召回）、false（不召回）。 | False |
| language | string |  | - | 多语言检索，支持多种语言召回结果。指定输入参数和召回参数结果的语言类型，可支持的语言类型为多种语言，不填默认为中文。注意：该功能为高级权限功能。 | en，fr |
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
      "tag": "文物古迹",
      "uid": "c9b5fb91d49345bc5d0d0262",
      "city": "北京市",
      "name": "天安门广场",
      "town": "东华门街道",
      "adcode": "110101",
      "address": "北京市-东城区-东长安街",
      "business": "",
      "children": [],
      "district": "东城区",
      "location": {
        "lat": 39.9096519665138,
        "lng": 116.4041774131041
      },
      "province": "北京市",
      "town_code": 110101001
    }
  ]
}
```

#### 响应字段定义 (基于 Schema)

| 字段路径 | 类型 | 必填 | 说明 | 示例 |
|----------|------|------|------|------|
| `message` | string |  | 对API访问状态值的英文说明，如果成功返回ok，并返回结果字段，如果失败返回错误说明。 | ok |
| `results[]` | object |  |  | None |
| `results[].adcode` | integer \| null |  | poi所属区域代码。 | 110101 |
| `results[].address` | string \| null |  | poi所在地址。 | 北京市-东城区-东长安街 |
| `results[].business` | string \| null |  | poi所属商圈（该字段已废弃，请您关注，会逐步下掉）。 |  |
| `results[].children[]` | object |  |  | None |
| `results[].children[].classified_poi_tag` | string \| null |  | poi子点详细分类标签。 | 出入口;门 |
| `results[].children[].content_info` | string \| null |  | poi子点内容标签。 | 近游客中心;仅行人;正门;近售票处 |
| `results[].children[].distance` | integer \| null |  | poi子点与主点的距离（若无distance返回，则说明该子点在主点内）。 | 486 |
| `results[].children[].location` | object \| null |  | poi子点坐标。 |  |
| `results[].children[].location.lat` | number |  | 纬度值。 | 39.9096519665138 |
| `results[].children[].location.lng` | number |  | 经度值。 | 116.4041774131041 |
| `results[].children[].pv_rate` | string \| null |  | poi子点的热度（XX%选择）。 | 67%选择 |
| `results[].children[].show_name` | string \| null |  | poi子点简称。 | A口 |
| `results[].children[].std_tag` | string \| null |  | poi子点分类标签。 | 出入口;门 |
| `results[].children[].uid` | string |  | poi子点ID，可用于poi详情检索。 | 5266235556c89081c056ac80 |
| `results[].city` | string \| null |  | poi所属城市。 | 北京市 |
| `results[].classified_poi_tag` | string \| null |  | POI展示分类（细致分类）。 | 旅游景点;5A景区 |
| `results[].district` | string \| null |  | poi所属区县。 | 东城区 |
| `results[].location` | object \| null |  | poi经纬度坐标。 |  |
| `results[].location.lat` | number |  | 纬度值。 | 39.9096519665138 |
| `results[].location.lng` | number |  | 经度值。 | 116.4041774131041 |
| `results[].name` | string |  | poi名称，单次请求最多返回10条结果。 | 天安门广场 |
| `results[].province` | string \| null |  | poi所属省份。 | 北京市 |
| `results[].tag` | string \| null |  | poi分类。 | 文物古迹 |
| `results[].town` | string \| null |  | poi所属乡镇街道。 | 东华门街道 |
| `results[].town_code` | integer \| null |  | poi所属乡镇街道编码。 | 110101001 |
| `results[].uid` | string |  | poi的唯一标示，ID。 | c9b5fb91d49345bc5d0d0262 |
| `status` | integer |  | 本次API访问状态，如果成功返回0，如果失败返回其他数字。（见服务状态码） | 0 |

### 常见问题

**Q: 哪些参数是调用此接口时必须提供的？**

A: query（搜索关键字）、region（检索区域）和 ak（访问密钥）是三个必填参数，缺少任何一个都会导致请求失败。

**Q: 一次请求最多返回多少个地点结果？**

A: 单次请求最多返回10条地点（POI）结果。

**Q: 如何严格限制返回结果只在指定的城市内？**

A: 除了设置 region 参数外，还需要将 region_limit 参数设置为 true，这样将仅召回 region 对应区域内的数据。

**Q: 返回的坐标是什么类型的？可以转换吗？**

A: 默认返回百度经纬度坐标（bd09ll）。可以通过设置 ret_coordtype 参数为 'gcj02ll' 来返回国测局经纬度坐标。传入的坐标类型由 coord_type 参数控制。

**Q: business（商圈）字段为什么是空的或提示已废弃？**

A: 文档中已注明 business 字段为已废弃字段，正在逐步下线，因此返回结果中可能为空或不包含此字段，请勿依赖此字段进行开发。
