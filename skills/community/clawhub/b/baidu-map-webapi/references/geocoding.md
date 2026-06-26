# 百度地图地理编码 API

## 服务概述

用户可通过该功能，将结构化地址（省/市/区/街道/门牌号）解析为对应的位置坐标。地址结构越完整，地址内容越准确，解析的坐标精度越高。当前为V3.0版本接口文档，V2.0及以前版本自2019.6.18起新用户无法使用。老用户仍可继续使用V2.0及以前版本请求实现全球逆地理编码服务，为保障用户体验，建议您尽快迁移到V3.0版本。

- **版本**: 2.0.0
- **服务标识**: `geocoding_api`
- **官方文档**: <https://lbs.baidu.com/faq/api?title=webapi/guide/webservice-geocoding-base>

### API调用

**GET** `https://api.map.baidu.com/geocoding/v3/`

### 输入参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 | 示例 |
|--------|------|------|--------|------|------|
| address | string | T | - | 待解析的地址。最多支持128个字节。可以输入两种样式的值：1、标准的结构化地址信息（推荐）；2、支持“*路与*路交叉口”描述方式（不保证返回）。 | 北京市海淀区上地十街10号 |
| ak | string | T | - | 用户申请注册的访问密钥（key）。 | 您的AK |
| city | string |  | - | 地址所在的城市名。用于指定上述地址所在的城市，当多个城市都有上述地址时，该参数起到过滤作用，但不限制坐标召回城市。 | 北京市 |
| ret_coordtype | string (enum: gcj02ll, bd09mc, bd09ll) |  | bd09ll | 返回的坐标类型。 | gcj02ll |
| sn | string |  | - | 若用户所用ak的校验方式为sn校验时该参数必须。 | - |
| output | string (enum: json, xml) |  | xml | 输出格式。 | json |
| callback | string |  | - | 将json格式的返回值通过callback函数返回以实现jsonp功能。 | showLocation |
| extension_analys_level | string (enum: 0, 1, true, false) |  | 0 | 是否触发解析到最小地址结构功能。值为1或true时，触发analys_level字段返回；值为0或false时，analys_level字段不返回。 | 1 |
| extension_poi_infos | boolean |  | False | 是否返回经纬度所在的地址信息。 | True |

### 响应结果

#### 响应示例 (供参考)

```json
{
  "result": {
    "level": "门址",
    "precise": 1,
    "location": {
      "lat": 40.056828485961,
      "lng": 116.30762232672
    },
    "confidence": 80,
    "comprehension": 100
  },
  "status": 0
}
```

#### 响应字段定义 (基于 Schema)

| 字段路径 | 类型 | 必填 | 说明 | 示例 |
|----------|------|------|------|------|
| `count` | integer \| null |  | 解析结果的数量（当extension_poi_infos=true时返回）。 |  |
| `poi_infos` | object \| null |  | 解析结果信息列表（当extension_poi_infos=true时返回；第一个结果为对result里经纬度的解析）。 |  |
| `poi_infos.adcode` | integer \| null |  | 行政区划代码。 | 110106 |
| `poi_infos.analys_level` | string \| null |  | 可以解析地址文本中的最小地址结构。 | POI |
| `poi_infos.city` | string \| null |  | 城市。 | 北京市 |
| `poi_infos.comprehension` | integer \| null |  | 描述地址理解程度。分值范围0-100，分值越大，理解程度越高。 | 100 |
| `poi_infos.confidence` | integer \| null |  | 描述打点绝对精度（坐标点的误差范围）。 | 80 |
| `poi_infos.country` | string \| null |  | 国家。 | 中国 |
| `poi_infos.district` | string \| null |  | 区县。 | 丰台区 |
| `poi_infos.formatted_address` | string \| null |  | 结构化地址（不包含POI信息）。 | 北京市丰台区石榴庄街道宋庄路73号院-2号楼 |
| `poi_infos.level` | string \| null |  | 可以打点到地址文本中的真实地址结构类型。 | 餐饮 |
| `poi_infos.location` | object \| null |  | 坐标。 |  |
| `poi_infos.location.lat` | number \| null |  | 纬度值。 |  |
| `poi_infos.location.lng` | number \| null |  | 经度值。 |  |
| `poi_infos.name` | string \| null |  | poi 名字（当经纬度为某poi时返回）。 | 天安门 |
| `poi_infos.precise` | integer \| null |  | 是否精确查找。1为精确查找，0为不精确。 | 1 |
| `poi_infos.province` | string \| null |  | 省份。 | 北京市 |
| `poi_infos.street` | string \| null |  | 街道。 | 宋庄路 |
| `poi_infos.street_number` | string \| null |  | 街道代码。 | 73号院-2号楼 |
| `poi_infos.town` | string \| null |  | 乡镇。 | 石榴庄街道 |
| `poi_infos.town_code` | string \| null |  | 乡镇代码。 | 110106021 |
| `poi_infos.uid` | string \| null |  | poi唯一标识。 | 41f0fd987c2ff931aecb66e5 |
| `result` | object |  | 返回的结果（策略首推的结果，对应poi_infos的第一个结果）。 |  |
| `result.analys_level` | string \| null |  | 可以解析地址文本中的最小地址结构，如“POI”。（当extension_analys_level=true时返回） | POI |
| `result.comprehension` | integer |  | 描述地址理解程度。分值范围0-100，分值越大，服务对地址理解程度越高（建议以此字段作为解析结果判断标准）。 | 100 |
| `result.confidence` | integer |  | 描述打点绝对精度（坐标点的误差范围）。分值越高，误差越小。 | 80 |
| `result.level` | string |  | 可以打点到地址文本中的真实地址结构类型，如“道路”、“门址”等。 | 门址 |
| `result.location` | object |  | 经纬度坐标。 |  |
| `result.location.lat` | number |  | 纬度值。 | 40.056828485961 |
| `result.location.lng` | number |  | 经度值。 | 116.30762232672 |
| `result.precise` | integer |  | 是否精确查找。1为精确查找（准确打点），0为不精确（模糊打点）。 | 1 |
| `status` | integer |  | 本次API访问状态，成功返回0，失败返回其他数字。<br/><br/>**枚举值说明：**<br/>`0`: ok: 正常<br/>`1`: Server Internal Error: 服务器内部错误。<br/>`2`: Parameter Invalid: 请求参数非法，如必要参数拼写错误或漏传。<br/>`3`: Verify Failure: 权限校验失败。<br/>`4`: Quota Failure: 配额校验失败，服务当日调用次数已超限。<br/>`5`: AK Failure: ak不存在或者非法，如未传入ak或ak已被删除。<br/>`101`: AK Missing: AK参数不存在，请求消息没有携带AK参数。<br/>`102`: Whitelist/Security Code Error: 不通过白名单或者安全码不对。<br/>`240`: APP Service Disabled: APP 服务被禁用，用户在控制台中禁用了某项服务。 | 0 |

### 常见问题

**Q: 地址应该怎么填写精度最高？**

A: 推荐使用完整的结构化地址信息，如“省+市+区+街道+门牌号”。地址结构越完整，解析精度越高。也支持“*路与*路交叉口”格式，但后者不保证总有返回结果。

**Q: ret_coordtype 参数应该怎么选？**

A: 该参数控制返回的坐标系。bd09ll（默认）为百度经纬度坐标；gcj02ll为国测局坐标（如高德、腾讯地图使用）；bd09mc为百度墨卡托坐标。请根据您的下游应用需求选择。

**Q: 如何判断解析结果的准确性？**

A: 建议主要参考返回字段中的 `comprehension`（理解度）和 `confidence`（精度）。`comprehension` 分值越高（最高100），表示服务对地址的理解越准确；`confidence` 分值越高，表示坐标的绝对误差范围越小。`precise` 字段为1表示精确查找。

**Q: city 参数是必须的吗？它起什么作用？**

A: city 参数不是必须的。它的主要作用是当同一个地址名称出现在多个城市时（例如“北京路”），用于过滤和优先指定目标城市，但最终返回的坐标不一定限制在该城市内。

**Q: 什么是 sn 参数？什么时候需要它？**

A: sn 参数是用于签名校验的。只有在您申请AK时，在API控制台选择了“SN校验”方式，才需要在请求时计算并传入sn参数。如果选择的是“IP白名单”校验方式，则不需要此参数。
