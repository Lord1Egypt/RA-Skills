# 百度地图步行路线规划 API

## 服务概述

根据起终点坐标检索符合条件的步行路线规划方案

- **版本**: 2.0.0
- **服务标识**: `direction_v2_walking`
- **官方文档**: <https://lbs.baidu.com/faq/api?title=webapi/webservice-direction/walking>

### API调用

**GET** `https://api.map.baidu.com/direction/v2/walking`

### 输入参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 | 示例 |
|--------|------|------|--------|------|------|
| origin | string | T | - | 起点经纬度，格式为：纬度,经度；小数点后不超过6位 | 40.01116,116.339303 |
| destination | string | T | - | 终点经纬度，格式为：纬度,经度；小数点后不超过6位 | 39.936404,116.452562 |
| origin_uid | string |  | - | 起点POI的uid(请尽量填写uid，将提升路线规划的准确性。使用地点检索服务获取uid 使用地点输入提示服务获取uid ) | - |
| destination_uid | string |  | - | 终点POI的uid(请尽量填写uid，将提升路线规划的准确性。使用地点检索服务获取uid 使用地点输入提示服务获取uid ) | - |
| coord_type | string (enum: bd09ll, bd09mc, gcj02, wgs84) |  | bd09ll | 输入坐标类型 | - |
| ret_coordtype | string (enum: bd09ll, gcj02) |  | bd09ll | 输出坐标类型 | - |
| output | string |  | json | 表示输出类型，可设置为xml或json | - |
| ak | string | T | - | 用户的访问权限，AK申请 | 您的AK |
| sn | string |  | - | 用户的权限签名，当AK设置为SN校验时，该参数必填 SN计算方法 | - |
| timestamp | integer |  | - | 时间戳，与SN配合使用 | - |
| callback | string |  | - | 回调函数，用于解决浏览器请求跨域问题 | - |

### 响应结果

#### 响应字段定义 (基于 Schema)

| 字段路径 | 类型 | 必填 | 说明 | 示例 |
|----------|------|------|------|------|
| `info` | object |  | 版权信息 | None |
| `info.copyright` | object |  |  | None |
| `info.copyright.imageUrl` | string |  |  | http://api.map.baidu.com/images/copyright_logo.png |
| `info.copyright.text` | string |  |  | @2026 Baidu - Data |
| `message` | string |  | 状态码对应的信息 | ok |
| `result` | object |  | 返回的结果 | None |
| `result.destination` | object |  |  | None |
| `result.destination.destinationPt` | object |  |  | None |
| `result.destination.destinationPt.lat` | number |  |  | 39.936404 |
| `result.destination.destinationPt.lng` | number |  |  | 116.452562 |
| `result.origin` | object |  |  | None |
| `result.origin.originPt` | object |  |  | None |
| `result.origin.originPt.lat` | number |  |  | 40.01116 |
| `result.origin.originPt.lng` | number |  |  | 116.339303 |
| `result.routes` | array |  |  | None |
| `result.routes[].distance` | integer |  | 方案距离，单位：米 | 16748 |
| `result.routes[].duration` | integer |  | 线路耗时，单位：秒 | 15491 |
| `result.routes[].steps` | array |  |  | None |
| `result.routes[].steps[].area` | integer |  |  | 0 |
| `result.routes[].steps[].direction` | integer |  | 当前道路方向角 | 176 |
| `result.routes[].steps[].distance` | integer |  | 路段距离，单位：米 | 197 |
| `result.routes[].steps[].duration` | integer |  | 路段耗时，单位：秒 | 168 |
| `result.routes[].steps[].guidance` | array |  | 诱导信息,有高级权限才能返回 | None |
| `result.routes[].steps[].guidance[].verbal_instructions` | array |  | 播报详细信息 | None |
| `result.routes[].steps[].guidance[].verbal_instructions[].cloud_guide_version` | string |  | 云导版本 | None |
| `result.routes[].steps[].guidance[].verbal_instructions[].details` | array |  | 播报点详情 | None |
| `result.routes[].steps[].guidance[].verbal_instructions[].details[].distance_to_gdpt` | integer |  | 播报点与诱导点的距离 | None |
| `result.routes[].steps[].guidance[].verbal_instructions[].details[].speak_text` | string |  | 播报内容 | None |
| `result.routes[].steps[].guidance[].verbal_instructions[].details[].voice_level` | integer |  | 音量级别 | None |
| `result.routes[].steps[].guidance[].verbal_instructions[].distance_to_origin` | Integer |  | 播报点与起点的距离 | None |
| `result.routes[].steps[].instructions` | string |  | 路段描述 | 向正南方向出发,走200米,<b>右转</b> |
| `result.routes[].steps[].leg_index` | integer |  |  | 0 |
| `result.routes[].steps[].links` | array |  |  | None |
| `result.routes[].steps[].links[].attr` | integer |  | link属性，0x01表示禁行 | None |
| `result.routes[].steps[].links[].length` | integer |  | link长度，单位：米 | None |
| `result.routes[].steps[].name` | string |  | 该路段道路名称，如“信息路“；若道路未命名或百度地图未采集到该道路名称，则返回'无名路' |  |
| `result.routes[].steps[].path` | string |  | 路段位置坐标描述 | 116.339966,40.011156;116.340006,40.010546;116.3... |
| `result.routes[].steps[].pois` | array |  |  | None |
| `result.routes[].steps[].stepDestinationInstruction` | string |  |  |  |
| `result.routes[].steps[].stepDestinationLocation` | object |  |  | None |
| `result.routes[].steps[].stepDestinationLocation.lat` | number |  |  | 40.009366288399 |
| `result.routes[].steps[].stepDestinationLocation.lng` | number |  |  | 116.34006725922 |
| `result.routes[].steps[].stepOriginInstruction` | string |  |  |  |
| `result.routes[].steps[].stepOriginLocation` | object |  |  | None |
| `result.routes[].steps[].stepOriginLocation.lat` | number |  |  | 40.011156487369 |
| `result.routes[].steps[].stepOriginLocation.lng` | number |  |  | 116.33996582559 |
| `result.routes[].steps[].turn_type_id` | integer |  | 行驶转向类型<br/><br/>**枚举值说明：**<br/>`0`: 无效<br/>`1`: 直行<br/>`2`: 右前方转弯<br/>`3`: 右转<br/>`4`: 右后方转弯<br/>`5`: 左后方转弯<br/>`6`: 左转<br/>`7`: 左前方转弯<br/>`15`: 到斜对面，右前方转弯<br/>`17`: 到斜对面，左前方转弯<br/>`21`: 到斜对面，左前方转弯<br/>`23`: 到斜对面，右前方转弯<br/>`26`: 过马路左转<br/>`27`: 过马路右转<br/>`28`: 进入左侧道路继续向前<br/>`29`: 进入右侧道路继续向前<br/>`30`: 进入左侧道路往回走<br/>`31`: 进入右侧道路往回走 | 3 |
| `result.routes[].steps[].type` | integer |  |  | 5 |
| `status` | integer |  | 本次API访问状态码<br/><br/>**枚举值说明：**<br/>`0`: ok: 正常<br/>`1`: 服务内部错误<br/>`2`: 参数无效<br/>`101`: AK参数不存在<br/>`2001`: 无骑行路线 | 0 |
| `type` | integer |  | 返回数据类型 | 2 |

### 常见问题

**Q: 如何提升路线规划的准确性？**

A: 请尽量填写起点和终点的POI uid参数（origin_uid, destination_uid），使用地点检索或输入提示服务获取。

**Q: 支持哪些输入坐标类型？**

A: 支持 bd09ll（百度经纬度坐标）、bd09mc（百度墨卡托坐标）、gcj02（国测局加密坐标）、wgs84（GPS设备坐标）。

**Q: 返回的坐标类型可以更改吗？**

A: 可以，通过 ret_coordtype 参数指定，可选 bd09ll 或 gcj02。

**Q: 返回的转向类型(turn_type_id)有哪些？**

A: 包含直行、左右转、过马路、进入左右侧道路等30多种精细化的转向类型枚举。
