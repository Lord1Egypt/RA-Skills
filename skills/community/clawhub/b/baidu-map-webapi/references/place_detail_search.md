# 百度地图地点检索及联想 API

## 服务概述

地点详情检索接口用于获取指定POI（兴趣点）的详细信息。开发者需要通过其他检索功能（如区域检索）获取POI的UID，然后使用本接口传入UID来获取该POI的完整详情数据。不同类型POI返回的详情字段有所不同，包括基础信息、地理位置、行政区划、营业状态、联系方式、评分、图片、分类标签等。注意：必须通过检索接口实时获取POI的UID进行详情检索，不支持使用过时或静态的UID。

- **版本**: 2.0.0
- **服务标识**: `place_detail_search`
- **官方文档**: <https://lbs.baidu.com/faq/api?title=webapi/guide/webservice-placeapiV3/interfaceDocumentV3>

### API调用

**GET** `https://api.map.baidu.com/place/v3/detail`

### 输入参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 | 示例 |
|--------|------|------|--------|------|------|
| uid | string |  | - | POI的唯一标识符UID，用于检索单个POI详情。与uids参数二选一，必须提供其中一项。 | 65e1ee886c885190f60e77ff |
| uids | string |  | - | 多个UID的集合，最多可传入10个UID，用英文逗号分隔。与uid参数二选一，必须提供其中一项。 | 65e1ee886c885190f60e77ff,2a7a25ecf9cf13636d3e1bad |
| ak | string | T | - | 开发者的访问密钥（API Key），必填项。 | - |
| scope | integer (enum: 1, 2) |  | - | 检索结果详细程度。取值为1或空则返回基本信息；取值为2返回检索POI详细信息。 | 2 |
| extensions_adcode | boolean |  | False | 是否召回国标行政区划编码，true（召回）、false（不召回）。 | True |
| photo_show | boolean |  | False | 是否输出图片信息：true(输出)，false(不输出)。购买商用授权后可申请开通。 | False |
| ret_coordtype | string |  | - | 返回的坐标类型，可选参数，添加后POI返回国测局经纬度坐标。 | gcj02ll |
| language | string |  | - | 多语言检索，支持多种语言召回结果。指定输入参数和召回参数结果的语言类型，不填默认为中文。该功能为高级权限功能。 | en |
| output | string (enum: json) |  | json | 输出数据格式，仅支持json。 | json |

### 响应结果

#### 响应示例 (供参考)

```json
{
  "status": 0,
  "message": "ok",
  "results": [
    {
      "uid": "435d7aea036e54355abbbcc8",
      "area": "海淀区",
      "city": "北京市",
      "name": "百度大厦",
      "town": "上地街道",
      "detail": 1,
      "address": "北京市海淀区上地十街10号",
      "location": {
        "lat": 40.05702695093102,
        "lng": 116.30787762514564
      },
      "province": "北京市",
      "street_id": "435d7aea036e54355abbbcc8",
      "town_code": 110108022,
      "detail_info": {
        "tag": "房地产;写字楼",
        "type": "house",
        "image_num": "172",
        "detail_url": "http://api.map.baidu.com/place/detail?output=html&source=placeapi_v3&uid=435d7aea036e54355abbbcc8",
        "shop_hours": "",
        "comment_num": "200",
        "content_tag": "位置优越;毗邻地铁;花园景观",
        "navi_location": {
          "lat": 40.0571097883115,
          "lng": 116.30698866201296
        },
        "overall_rating": "4.7"
      }
    }
  ]
}
```

#### 响应字段定义 (基于 Schema)

| 字段路径 | 类型 | 必填 | 说明 | 示例 |
|----------|------|------|------|------|
| `message` | string |  | 对API访问状态值的英文说明，如果成功返回ok，并返回结果字段，如果失败返回错误说明。 | ok |
| `results[]` | object |  |  | None |
| `results[].adcode` | integer \| null |  | POI所属区域代码。 | 110108 |
| `results[].address` | string \| null |  | POI所在地址。 | 北京市海淀区上地十街10号 |
| `results[].area` | string \| null |  | POI所属区县。 | 海淀区 |
| `results[].city` | string \| null |  | POI所属城市。 | 北京市 |
| `results[].detail` | string \| null |  | 是否有详情页：1有，0没有。 | 1 |
| `results[].detail_info` | object \| null |  | POI的详细信息对象。 |  |
| `results[].detail_info.best_time` | string \| null |  | 最佳游玩时间。 | 9月-10月 |
| `results[].detail_info.brand` | string \| null |  | POI对应的品牌。 | 淮扬菜 |
| `results[].detail_info.children[]` | object |  |  | None |
| `results[].detail_info.children[].classified_poi_tag` | string \| null |  | POI子点详细分类标签。 | 出入口;门 |
| `results[].detail_info.children[].content_info` | string \| null |  | POI子点内容标签。 | 近游客中心;仅行人;正门;近售票处 |
| `results[].detail_info.children[].distance` | integer \| null |  | POI子点与主点的距离（若无distance返回，则说明该子点在主点内）。 | 486 |
| `results[].detail_info.children[].location` | object |  | POI子点坐标对象。 |  |
| `results[].detail_info.children[].location.lat` | number |  | 纬度值。 | 40.05702695093102 |
| `results[].detail_info.children[].location.lng` | number |  | 经度值。 | 116.30787762514564 |
| `results[].detail_info.children[].name` | string \| null |  | POI子点名称。 | 故宫博物院-午门(南门) |
| `results[].detail_info.children[].pv_rate` | string \| null |  | POI子点的热度（X%选择）。 | 67%选择 |
| `results[].detail_info.children[].show_name` | string \| null |  | POI子点简称。 | 午门(南门) |
| `results[].detail_info.children[].std_tag` | string \| null |  | POI子点分类标签。 | 出入口;门 |
| `results[].detail_info.children[].uid` | string \| null |  | POI子点ID。 | c1653405c7ff0f79ab175a78 |
| `results[].detail_info.classified_poi_tag` | string \| null |  | POI展示分类（细致分类）。 | 旅游景点;5A景区 |
| `results[].detail_info.comment_num` | string \| null |  | POI的评论数。 | 200 |
| `results[].detail_info.description` | string \| null |  | 描述。 | 北京故宫，旧称紫禁城，是中国明、清两代24位皇帝的皇宫，现在指位于北京的故宫博物院，位于北京市... |
| `results[].detail_info.detail_url` | string \| null |  | POI的详情页URL。 | http://api.map.baidu.com/place/detail?output=ht... |
| `results[].detail_info.image_num` | string \| null |  | POI图片数。 | 172 |
| `results[].detail_info.indoor_floor` | string \| null |  | 室内POI所在楼层。 |  |
| `results[].detail_info.navi_location` | object |  | POI对应的导航引导点坐标（上车点）。大型面状POI的导航引导点，一般为各类出入口。 |  |
| `results[].detail_info.navi_location.lat` | number |  | 纬度值。 | 40.05702695093102 |
| `results[].detail_info.navi_location.lng` | number |  | 经度值。 | 116.30787762514564 |
| `results[].detail_info.overall_rating` | string \| null |  | POI的综合评分。 | 4.7 |
| `results[].detail_info.parent_id` | string \| null |  | POI父点ID。 | 06d2dffda107b0ef89f15db6 |
| `results[].detail_info.photos` | array \| null |  | POI图片的下载链接数组。购买商用授权后可申请开通。 | [] |
| `results[].detail_info.price` | string \| null |  | POI商户的价格。 | 4.7 |
| `results[].detail_info.ranking` | string \| null |  | POI的相关榜单排名。 | 北京市本地人爱去榜NO.2 |
| `results[].detail_info.shop_hours` | string \| null |  | POI的营业时间，格式如10:30-14:00,16:30-22:00。 | 10:30-14:00,16:30-22:00 |
| `results[].detail_info.sug_time` | string \| null |  | 建议时长。 | 0.5-1天 |
| `results[].detail_info.tag` | string \| null |  | POI分类标签。 | 房地产;写字楼 |
| `results[].detail_info.type` | string \| null |  | POI类型，如hotel、cater、life等，配合filter排序。 | house |
| `results[].location` | object |  | POI经纬度坐标对象。 |  |
| `results[].location.lat` | number |  | 纬度值。 | 40.05702695093102 |
| `results[].location.lng` | number |  | 经度值。 | 116.30787762514564 |
| `results[].name` | string |  | POI名称。 | 百度大厦 |
| `results[].province` | string \| null |  | POI所属省份。 | 北京市 |
| `results[].status` | string \| null |  | POI营业状态：空（代表正常营业）、推算位置、暂停营业、可能已关闭、已关闭。 |  |
| `results[].street_id` | string \| null |  | POI所在街景图ID。 | 435d7aea036e54355abbbcc8 |
| `results[].telephone` | string \| null |  | POI的电话。 | (010)62881144 |
| `results[].town` | string \| null |  | POI所属乡镇街道。 | 上地街道 |
| `results[].town_code` | integer \| null |  | POI所属乡镇街道编码。 | 110108022 |
| `results[].uid` | string |  | POI的唯一标识符ID。 | 435d7aea036e54355abbbcc8 |
| `status` | integer |  | 本次API访问状态，如果成功返回0，如果失败返回其他数字。 | 0 |

### 常见问题

**Q: 如何获取POI的UID？**

A: 必须通过百度地图的其他检索接口（如区域检索、周边检索、矩形区域检索）实时获取POI的UID。不能使用过时或静态的UID，否则可能检索不到详情或返回错误。

**Q: uid和uids参数可以同时使用吗？**

A: 不可以。uid和uids参数是互斥的，必须且只能提供其中一项。uid用于检索单个POI详情，uids用于批量检索最多10个POI详情，多个UID用英文逗号分隔。

**Q: scope参数的作用是什么？**

A: scope参数控制返回结果的详细程度。设置为1或空时，只返回POI的基本信息（如名称、坐标、地址）。设置为2时，返回POI的详细信息，包括评分、营业时间、分类标签、图片数、评论数等。

**Q: photo_show和photos字段需要特殊权限吗？**

A: 是的。photo_show参数设置为true以输出图片信息，以及返回结果中的photos数组字段，都需要购买商用授权后才能联系商务提交工单申请开通。普通开发者默认无法使用这些功能。

**Q: 如何获取多语言结果？**

A: 通过language参数指定输入和返回结果的语言类型（如en、fr）。但请注意，多语言检索是高级权限功能，需要提交工单咨询开通。默认不填时返回中文结果。
