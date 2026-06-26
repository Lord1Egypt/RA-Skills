# 百度地图驾车路线规划 API

## 服务概述

根据起终点坐标检索符合条件的驾车路线规划方案，支持一次请求返回多条路线（备用路线）、18个以内的途径点、传入车牌规避限行路段、传入起点车头方向辅助算路、未来7天任意出发时刻预测路况规划路线等功能。

- **版本**: 2.0.0
- **服务标识**: `direction_v2_driving`
- **官方文档**: <https://lbs.baidu.com/faq/api?title=webapi/webservice-direction/dirve>

### API调用

**GET** `https://api.map.baidu.com/direction/v2/driving`

### 输入参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 | 示例 |
|--------|------|------|--------|------|------|
| ak | string | T | - | 用户的访问权限AK，申请地址：https://lbs.baidu.com/apiconsole/key | 您的AK |
| origin | string | T | - | 起点经纬度，格式为：纬度,经度；小数点后不超过6位 | 40.01116,116.339303 |
| destination | string | T | - | 终点经纬度，格式为：纬度,经度；小数点后不超过6位 | 39.936404,116.452562 |
| origin_uid | string |  | - | 起点POI的uid，通过地点检索或地点输入提示服务获取，填写可提升路线规划准确性 | b057d2b7a1f8c8b1b7f0a1b2 |
| destination_uid | string |  | - | 终点POI的uid，通过地点检索或地点输入提示服务获取，填写可提升路线规划准确性 | c157e3c8b2f9d9c2c8e1b2c3 |
| waypoints | string |  | - | 途径点坐标串，支持18个以内的有序途径点。多个途径点坐标按顺序以英文竖线符号分隔 | 40.465,116.314|40.232,116.352|40.121,116.453 |
| coord_type | string (enum: bd09ll, bd09mc, gcj02, wgs84) |  | bd09ll | 输入坐标类型，默认为bd09ll | bd09ll |
| ret_coordtype | string (enum: bd09ll, gcj02) |  | bd09ll | 返回结果坐标类型，默认为bd09ll | bd09ll |
| tactics | integer (enum: 0, 2, 3, 4, 5...) |  | 0 | 路线规划策略，0：默认，2：距离最短（只返回一条路线，不考虑限行和路况，距离最短且稳定，用于估价场景），3：不走高速，4：高速优先，5：躲避拥堵，6：少收费，7: 躲避拥堵 & 高速优先，8: 躲避拥堵 & 不走高速，9: 躲避拥堵 & 少收费，10: 躲避拥堵 & 不走高速 & 少收费，11: 不走高速 & 少收费，12: 距离优先（考虑限行和路况，距离相对短且不一定稳定），13：时间优先 | 5 |
| alternatives | integer (enum: 0, 1) |  | 0 | 是否返回备选路线，0：返回一条推荐路，1：返回1-3条路线供选择 | 1 |
| cartype | integer (enum: 0, 1) |  | 0 | 车辆类型，用于结合plate_number规避限行，0：普通汽车，1：纯电动汽车 | 1 |
| plate_number | string |  | - | 车牌号，用于规避车牌号限行路段，1、若有规避限行区域的可选路线，则返回规避后的路线，不会返回限行路线2、若无规避限行的可选路线（如：起终点在限行区域内，或所有符合偏好的路线都无法规避限行区域），则返回限行路线中最优路线，并在返回字段 restriction 中提示用户路段被限行 | 京A00022 |
| departure_time | string |  | - | 出发时间，UNIX时间戳。支持未来7天任意时刻。设置后将依据设定时间预测路况和限行规则计算路线和耗时（高级权限服务）。 | 1609459200 |
| ext_departure_time | string |  | - | 更多出发时间，UNIX时间戳。支持过去7天内一个或多个（≤12个）时间戳，多个用英文逗号分隔。设置后将返回ext_duration字段（高级权限服务）。 | 1526527619,1526525384 |
| expect_arrival_time | string |  | - | 预期到达时间，UNIX时间戳。取值范围：当前时间之后15分钟任意时刻。设置后将返回suggest_departure_time字段（高级权限服务）。 | 1609462800 |
| gps_direction | integer |  | - | 起点的车头方向，与正北方向顺时针夹角，取值范围0-359。当speed>1.5米/秒且gps_direction存在时采用该方向辅助算路。 | 90 |
| radius | number |  | - | 起点的定位精度，单位：米，取值范围[0,2000]。配合gps_direction字段使用。 | 10.5 |
| speed | number |  | - | 起点车辆的行驶速度，单位：米/秒。配合gps_direction字段使用，当speed>1.5且gps_direction存在时采用gps_direction方向。 | 5.2 |
| output | string (enum: xml, json) |  | json | 输出类型 | json |
| sn | string |  | - | 用户的权限签名，当AK设置为SN校验时该参数必填。SN计算方法参见文档。 | 5ce449e0e6e3c4e8d9f8a1b2c3d4e5f6 |
| timestamp | integer |  | - | 时间戳，与SN配合使用。当sn参数存在时必填。 | 1609459200 |
| callback | string |  | - | 回调函数，仅在output=json时有效。 | handleResponse |
| intelligent_plan | integer (enum: 0, 1) |  | 0 | 是否执行途经点智能规划，综合考虑路况、限行、途经点相对位置及绕路成本，支持智能调整途经点顺序可选值：0（默认值）：不执行途经点智能规划1：执行途经点智能规划（高级权限服务）。 | 1 |
| walkinfo | integer (enum: 0, 1) |  | 0 | 是否下发起终点步导路线 | 1 |
| steps_info | integer (enum: 0, 1) |  | - | 是否下发step详情 | 1 |
| origin_bind_stategy | integer (enum: 0, 1) |  | 0 | 起点绑路策略，是否剔除封闭道路 | 1 |
| dest_bind_stategy | integer (enum: 0, 1) |  | 0 | 终点绑路策略，是否剔除封闭道路 | 1 |
| origin_road_type | integer (enum: 0, 1, 2, 3, 4) |  | 0 | 起点道路类型 | 3 |

### 高级权限

| 权限名称 | 描述 | 参数 | 参数示例 | 参数说明 | 高级能力文档 |
|----------|------|------|----------|----------|--------------|
| 驾车路线历史耗时 | 设置驾车路线历史耗时 | ext_departure_time | 1609459200 | 更多出发时间，UNIX时间戳。该字段将影响ext_duration字段的返回，用于返回驾车路线历史耗时（路线在指定出发时间的耗时）。目前支持输入过去7天内一个或多个出发时间戳（不超过12个），多个时间戳之间用','英文半角逗号隔开。ext_departure_time=1526527619,1526525384,1526523654 目前出发时间仅影响ext_duration字段，还不会影响路线计算和选择。即仍按照现在的路况计算并推荐路线，但将增加返回该路线在其他时间的耗时。不填则不返回ext_duration字段 | references/capabilities/driving_route_duration.md |
| 未来驾车路线规划 | 预测未来驾车路线耗时 | departure_time | 1609459200 | 出发时间，UNIX时间戳。支持未来7天任意时刻。设置后将依据设定时间预测路况和限行规则计算路线和耗时（高级权限服务）。 | references/capabilities/future_driving_route.md |
| 建议出发时间 | 高级权限出行时间建议 | expect_arrival_time | 1609462800 | 预期到达时间，UNIX时间戳。取值范围：当前时间之后15分钟任意时刻。设置后将返回suggest_departure_time字段, （小于这个时间则不做处理）若设置此参数，则路线规划服务将依据设定时间计算路线和耗时，并给出建议出发时间, 若算出的suggest_departure_time小于当前时间，则设置suggest_departure_time为-1 | references/capabilities/suggested_departure_time.md |
| 途经点智能路线规划 | 智能优化途经点路线 | intelligent_plan | 1 | 是否执行途经点智能规划，综合考虑路况、限行、途经点相对位置及绕路成本，支持智能调整途经点顺序可选值：0（默认值）：不执行途经点智能规划1：执行途经点智能规划（高级权限服务）。 | references/capabilities/waypoint_route_planning.md |

### 响应结果

#### 响应字段定义 (基于 Schema)

| 字段路径 | 类型 | 必填 | 说明 | 示例 |
|----------|------|------|------|------|
| `message` | string |  | 状态码对应的信息 | 成功 |
| `result` | object |  | 返回的结果 | None |
| `result.destination` | object |  | 请求的终点经纬度（确认值） | None |
| `result.destination.lat` | number |  | 终点纬度 | 39.936404 |
| `result.destination.lng` | number |  | 终点经度 | 116.452562 |
| `result.end_walkinfo` | array |  | 终点步导路线 | None |
| `result.end_walkinfo[].distance` | integer |  | 终点步导路线距离,单位米 | None |
| `result.end_walkinfo[].path` | string |  | 终点步导路线坐标点 | None |
| `result.origin` | object |  | 请求的起点经纬度（确认值） | None |
| `result.origin.lat` | number |  | 起点纬度 | 40.01116 |
| `result.origin.lng` | number |  | 起点经度 | 116.339303 |
| `result.restriction` | string |  | 限行结果提示信息。若无限行路线则返回空；若无法规避限行则返回限行提示信息。 | 无法为您避开北京限行区域，请合理安排出行 |
| `result.routes` | array |  | 返回的方案集 | None |
| `result.routes[].destination` | object |  | 终点坐标（实际用于算路的点） | None |
| `result.routes[].destination.lat` | number |  | 终点纬度 | 39.936404 |
| `result.routes[].destination.lng` | number |  | 终点经度 | 116.452562 |
| `result.routes[].distance` | integer |  | 方案距离，单位：米 | 10000 |
| `result.routes[].duration` | integer |  | 未来驾车路线耗时（若请求参数设置了符合规则的departure_time，则按照设定出发时间的预测路况计算路线耗时。若未设置departure_time，则按照当前时刻的路况计算路线耗时）或当前路况耗时，单位：秒 | 600 |
| `result.routes[].ext_duration` | integer \| string \| null |  | 驾车路线历史耗时（扩展），单位：秒。当设置了ext_departure_time时返回，多个时间戳对应多个耗时以英文逗号分隔，计算失败返回-1。 | 500,520,-1 |
| `result.routes[].origin` | object |  | 起点坐标（实际用于算路的点） | None |
| `result.routes[].origin.lat` | number |  | 起点纬度 | 40.01116 |
| `result.routes[].origin.lng` | number |  | 起点经度 | 116.339303 |
| `result.routes[].restriction_info` | object |  | 限行状态详细信息 | None |
| `result.routes[].restriction_info.desc` | string |  | 限行提示语，多条提示以英文竖线分隔 | 已为您避开北京限行区域|起点在北京限行区域，请合理安排出行 |
| `result.routes[].restriction_info.status` | integer (enum: 0, 1, 2... (共4个值)) |  | 限行状态，取值范围0-3 | 1 |
| `result.routes[].route_id` | string |  | 如无特殊需要，开发者无需关注 | xxxx |
| `result.routes[].steps` | array |  | 路线分段 | None |
| `result.routes[].steps[].adcodes` | string |  | 分段途经的城市编码，多个以英文逗号分隔 | 110000,120000 |
| `result.routes[].steps[].direction` | integer (enum: 0, 1, 2... (共12个值)) |  | 进入道路的角度，枚举值0-11，每个值代表30度范围 | 1 |
| `result.routes[].steps[].distance` | integer |  | step的距离信息，单位：米 | 500 |
| `result.routes[].steps[].end_location` | object |  | 分段终点坐标 | None |
| `result.routes[].steps[].end_location.lat` | number |  | 终点纬度 | 40.01136 |
| `result.routes[].steps[].end_location.lng` | number |  | 终点经度 | 116.339503 |
| `result.routes[].steps[].leg_index` | integer |  | 途径点序号（从0开始），标识step所属的途径点路段 | 0 |
| `result.routes[].steps[].path` | string |  | 分段坐标串 | 116.339303,40.01116;116.339503,40.01136;... |
| `result.routes[].steps[].road_name` | string |  | 分段的道路名称，未命名或未采集则返回'无名路' | 信息路 |
| `result.routes[].steps[].road_type` | integer (enum: 0, 1, 2... (共10个值)) |  | 分段的道路类型，枚举值0-9，枚举值：返回0-9之间的值，0：高速路，1：城市高速路，2：国道，3：省道，4：县道，5：乡镇村道，6：其他道路，7：九级路，8：航线(轮渡)9：行人道路 | 1 |
| `result.routes[].steps[].start_location` | object |  | 分段起点坐标 | None |
| `result.routes[].steps[].start_location.lat` | number |  | 起点纬度 | 40.01116 |
| `result.routes[].steps[].start_location.lng` | number |  | 起点经度 | 116.339303 |
| `result.routes[].steps[].toll` | integer |  | 分段道路收费，单位：元（可能不准确） | 0 |
| `result.routes[].steps[].toll_distance` | integer |  | 分段道路收费路程，单位：米 | 0 |
| `result.routes[].steps[].toll_gate_location` | object |  | 收费站位置，仅在进/出收费站时存在 | None |
| `result.routes[].steps[].toll_gate_location.lat` | number |  | 收费站纬度 | 40.12345 |
| `result.routes[].steps[].toll_gate_location.lng` | number |  | 收费站经度 | 116.12345 |
| `result.routes[].steps[].toll_gate_name` | string |  | 收费站名称，仅在进/出收费站时存在 | 北京收费站 |
| `result.routes[].steps[].traffic_condition` | array |  | 分段路况详情 | None |
| `result.routes[].steps[].traffic_condition[].status` | integer (enum: 0, 1, 2) |  | 路况指数：0-无路况，1-畅通，2-（文档未完整列举） | 1 |
| `result.routes[].suggest_departure_time` | integer \| null |  | 建议出发时间，单位：秒。当设置了expect_arrival_time时返回，按照预计到达时间预测路况计算路线，并给出建议出发时间，若计算出的时间小于当前时间则返回-1。 | 1609459200 |
| `result.routes[].tag` | string |  | 方案标签 | 推荐 |
| `result.routes[].taxi_fee` | integer |  | 出租车费用，单位：元 | 35 |
| `result.routes[].toll` | integer |  | 此路线道路收费（预估价格），单位：元 | 15 |
| `result.routes[].toll_distance` | integer |  | 收费路段里程，单位：米 | 5000 |
| `result.routes[].traffic_light` | integer |  | 红绿灯数量 | 12 |
| `result.start_walkinfo` | array |  | 起点步导路线 | None |
| `result.start_walkinfo[].distance` | integer |  | 起点步导路线距离,单位米 | None |
| `result.start_walkinfo[].path` | string |  | 起点步导路线坐标点 | None |
| `result.total` | integer |  | 返回方案的总数 | 3 |
| `status` | integer |  | 本次API访问状态码<br/><br/>**枚举值说明：**<br/>`0`: 成功<br/>`1`: 服务内部错误<br/>`2`: 参数无效<br/>`7`: 无返回结果 | 0 |
| `type` | integer |  | 默认返回2，开发者无需关注 | 2 |

### 常见问题

**Q: 一次请求最多支持多少个途径点？**

A: 支持18个以内的有序途径点，通过waypoints参数传入，多个点用英文竖线分隔。

**Q: 是否支持未来出行规划？**

A: 支持。通过departure_time参数设置未来7天内任意出发时刻（UNIX时间戳），系统将依据智能预测路况和道路限行规划合理路线并返回预测耗时。

**Q: 如何规避限行路段？**

A: 通过plate_number参数传入车牌号，并可选cartype区分燃油车/电动车，系统将自动规避限行路段。若无法完全规避，将在响应restriction字段中提示。

**Q: 返回结果支持哪些坐标类型？**

A: 支持bd09ll（百度经纬度坐标）和gcj02（国测局加密坐标），通过ret_coordtype参数指定。
