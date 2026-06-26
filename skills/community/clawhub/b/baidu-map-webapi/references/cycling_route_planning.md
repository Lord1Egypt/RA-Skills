# 百度地图骑行路线规划 API

## 服务概述

根据起终点坐标检索符合条件的骑行路线规划方案，支持普通自行车和电动自行车出行方式。

- **版本**: 2.0.0
- **服务标识**: `direction_v2_riding`
- **官方文档**: <https://lbs.baidu.com/faq/api?title=webapi/webservice-direction/cycling>

### API调用

**GET** `https://api.map.baidu.com/direction/v2/riding`

### 输入参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 | 示例 |
|--------|------|------|--------|------|------|
| origin | string | T | - | 起点经纬度，格式为：纬度,经度；小数点后不超过6位，40.056878,116.30815 | 40.01116,116.339303 |
| destination | string | T | - | 终点经纬度，格式为：纬度,经度；小数点后不超过6位，40.056878,116.30815 | 39.936404,116.452562 |
| origin_uid | string |  | - | 起点POI的uid（请尽量填写uid，将提升路线规划的准确性。使用地点检索服务或地点输入提示服务获取uid） | - |
| destination_uid | string |  | - | 终点POI的uid（请尽量填写uid，将提升路线规划的准确性。使用地点检索服务或地点输入提示服务获取uid） | - |
| coord_type | string (enum: bd09ll, bd09mc, gcj02, wgs84) |  | bd09ll | 输入坐标类型，默认bd09ll。允许的值为：bd09ll（百度经纬度坐标）、bd09mc（百度墨卡托坐标）、gcj02（国测局加密坐标）、wgs84（gps设备获取的坐标）。 | - |
| ret_coordtype | string (enum: bd09ll, gcj02) |  | bd09ll | 输出坐标类型，默认为百度经纬度坐标：bd09ll。可选值：bd09ll：百度经纬度坐标；gcj02：国测局坐标。 | - |
| output | string (enum: json, xml) |  | json | 表示输出类型，可设置为xml或json | - |
| riding_type | string (enum: 0, 1) |  | 0 | 骑行类型。默认0：0-普通 1-电动车 | - |
| road_prefer | integer (enum: 0, 3) |  | 0 | 算路方案。默认0：0-默认路线；3-无逆行且无阶梯的算路方案（不传默认0） | - |
| ak | string | T | - | 用户的访问权限，AK申请 | 您的AK |
| sn | string |  | - | 用户的权限签名，当AK设置为SN校验时，该参数必填。SN计算方法请参考相关文档。 | - |
| timestamp | integer |  | - | 时间戳，与SN配合使用，SN存在时必填 | - |
| callback | string |  | - | 回调函数，用于解决浏览器请求跨域问题。仅在output=json时，该参数有效。 | - |

### 响应结果

#### 响应字段定义 (基于 Schema)

| 字段路径 | 类型 | 必填 | 说明 | 示例 |
|----------|------|------|------|------|
| `info` | object |  | 版权信息 | None |
| `info.copyright` | object |  |  | None |
| `info.copyright.imageUrl` | string |  |  | http://api.map.baidu.com/images/copyright_logo.png |
| `info.copyright.text` | string |  |  | @2023 Baidu - Data |
| `message` | string |  | 状态码对应的信息 | ok |
| `result` | object |  | 返回的结果 | None |
| `result.destination` | object |  |  | None |
| `result.destination.destinationPt` | object |  |  | None |
| `result.destination.destinationPt.lat` | number |  | 终点纬度 | None |
| `result.destination.destinationPt.lng` | number |  | 终点经度 | None |
| `result.origin` | object |  |  | None |
| `result.origin.originPt` | object |  |  | None |
| `result.origin.originPt.lat` | number |  | 起点纬度 | None |
| `result.origin.originPt.lng` | number |  | 起点经度 | None |
| `result.routes` | array |  | 返回的方案集 | None |
| `result.routes[].destinationLocation` | object |  |  | None |
| `result.routes[].destinationLocation.lat` | number |  | 路线终点纬度 | None |
| `result.routes[].destinationLocation.lng` | number |  | 路线终点经度 | None |
| `result.routes[].distance` | integer |  | 方案距离，单位：米 | 17279 |
| `result.routes[].duration` | integer |  | 线路耗时，单位：秒 | 5969 |
| `result.routes[].originLocation` | object |  |  | None |
| `result.routes[].originLocation.lat` | number |  | 路线起点纬度 | None |
| `result.routes[].originLocation.lng` | number |  | 路线起点经度 | None |
| `result.routes[].restrictions_info` | string |  | 限行信息，如 '包含禁行路段\|包含逆行路段' |  |
| `result.routes[].restrictions_status` | integer |  | 限行类型，0x01表示禁行；0x02表示逆行 | 0 |
| `result.routes[].steps` | array |  | 路段信息集合 | None |
| `result.routes[].steps[].area` | integer |  |  | 0 |
| `result.routes[].steps[].direction` | integer |  | 当前道路方向角 | 176 |
| `result.routes[].steps[].distance` | integer |  | 路段距离，单位：米 | 200 |
| `result.routes[].steps[].duration` | integer |  | 路段耗时，单位：秒 | 60 |
| `result.routes[].steps[].guidance` | array |  | 诱导信息,有高级权限才能返回 | None |
| `result.routes[].steps[].guidance[].verbal_instructions` | array |  | 播报详细信息 | None |
| `result.routes[].steps[].guidance[].verbal_instructions[].cloud_guide_version` | string |  | 云导版本 | None |
| `result.routes[].steps[].guidance[].verbal_instructions[].details` | array |  | 播报点详情 | None |
| `result.routes[].steps[].guidance[].verbal_instructions[].details[].distance_to_gdpt` | integer |  | 播报点与诱导点的距离 | None |
| `result.routes[].steps[].guidance[].verbal_instructions[].details[].speak_text` | string |  | 播报内容 | None |
| `result.routes[].steps[].guidance[].verbal_instructions[].details[].voice_level` | integer |  | 音量级别 | None |
| `result.routes[].steps[].guidance[].verbal_instructions[].distance_to_origin` | Integer |  | 播报点与起点的距离 | None |
| `result.routes[].steps[].instructions` | string |  | 路段描述，如'骑行50米' | 骑行200米 |
| `result.routes[].steps[].leg_index` | integer |  |  | 0 |
| `result.routes[].steps[].links` | array |  | link信息集合 | None |
| `result.routes[].steps[].links[].attr` | integer |  | link属性，0x01表示禁行；0x02表示逆行 | 0 |
| `result.routes[].steps[].links[].length` | integer |  | link长度，单位：米 | 70 |
| `result.routes[].steps[].name` | string |  | 该路段道路名称，如'信息路'。若道路未命名或百度地图未采集到该道路名称，则返回'无名路'。 |  |
| `result.routes[].steps[].path` | string |  | 路段位置坐标描述 | 116.339966,40.011176;116.340006,40.010546;116.3... |
| `result.routes[].steps[].restrictions_info` | string |  | 限行信息 |  |
| `result.routes[].steps[].restrictions_status` | integer |  | 限行类型，0x01表示禁行；0x02表示逆行 | 0 |
| `result.routes[].steps[].stepDestinationInstruction` | string |  |  |  |
| `result.routes[].steps[].stepDestinationLocation` | object |  |  | None |
| `result.routes[].steps[].stepDestinationLocation.lat` | number |  | 路段终点纬度 | None |
| `result.routes[].steps[].stepDestinationLocation.lng` | number |  | 路段终点经度 | None |
| `result.routes[].steps[].stepOriginInstruction` | string |  |  |  |
| `result.routes[].steps[].stepOriginLocation` | object |  |  | None |
| `result.routes[].steps[].stepOriginLocation.lat` | number |  | 路段起点纬度 | None |
| `result.routes[].steps[].stepOriginLocation.lng` | number |  | 路段起点经度 | None |
| `result.routes[].steps[].turn_type` | string |  | 行驶转向方向，如'直行'、'左前方转弯' | 左转 |
| `result.routes[].steps[].type` | integer |  |  | 5 |
| `status` | integer |  | 本次API访问状态码<br/><br/>**枚举值说明：**<br/>`0`: 成功<br/>`1`: 服务内部错误<br/>`2`: 参数无效<br/>`2001`: 无骑行路线 | 0 |
| `type` | integer |  | 返回数据类型 | 2 |

### 常见问题

**Q: 起点和终点的坐标格式是什么？小数点后支持几位？**

A: 格式为：纬度,经度（例如：40.01116,116.339303）。小数点后不超过6位。

**Q: 如何提升路线规划的准确性？**

A: 建议填写起点和终点的POI uid（通过地点检索或输入提示服务获取），可显著提升准确性。

**Q: 支持哪些输入和输出的坐标系？**

A: 输入支持bd09ll、bd09mc、gcj02、wgs84；输出支持bd09ll和gcj02。

**Q: 电动车和普通自行车规划有什么区别？**

A: 选择电动车骑行类型（riding_type=1）时，路线规划算法会考虑电动车的通行规则和偏好。

**Q: “无逆行且无阶梯”的算路方案是什么意思？**

A: 选择road_prefer=3时，系统会尽量避免规划包含逆行路段和人行阶梯的路线。
