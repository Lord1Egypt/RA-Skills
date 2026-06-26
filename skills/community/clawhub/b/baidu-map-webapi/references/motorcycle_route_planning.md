# 百度地图摩托车路线规划 API

## 服务概述

摩托车路线规划为开放平台高级服务，需申请开通权限后才能访问。该接口提供摩托车出行路线规划，支持起点终点经纬度、途径点、车牌号限行规避、摩托车排量等多种参数，返回包含距离、耗时、收费、限行信息、详细路段及路况等丰富规划结果。

- **版本**: 2.0.0
- **服务标识**: `motorcycle`
- **官方文档**: <https://lbs.baidu.com/faq/api?title=webapi/webservice-direction/motorcycle>

### API调用

**GET** `https://api.map.baidu.com/direction/v2/motorcycle`

### 输入参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 | 示例 |
|--------|------|------|--------|------|------|
| ak | string | T | - | 用户的访问权限AK，需申请开通摩托车路线规划服务权限。 | 您的AK |
| origin | string | T | - | 起点经纬度，格式："纬度,经度"，小数点后不超过6位。若使用POI导航坐标可提升准确性。起点和终点的直线距离不得超过400km。 | 40.056878,116.30815 |
| destination | string | T | - | 终点经纬度，格式："纬度,经度"，小数点后不超过6位。若使用POI导航坐标可提升准确性。起点和终点的直线距离不得超过400km。 | 40.063597,116.364973 |
| origin_uid | string |  | - | 起点POI的uid，已知时请尽量填写，可提升路线规划准确性。可通过地点检索服务或地点输入提示服务获取。 | xxxxx |
| destination_uid | string |  | - | 终点POI的uid，已知时请尽量填写，可提升路线规划准确性。可通过地点检索服务或地点输入提示服务获取。 | xxxxx |
| waypoints | string |  | - | 途径点坐标串，支持18个以内的有序途径点。多个途径点坐标按顺序以英文竖线符号分隔。示例："40.465,116.314\|40.232,116.352\|40.121,116.453" | 40.465,116.314|40.232,116.352 |
| coord_type | string (enum: bd09ll, bd09mc, gcj02, wgs84) |  | bd09ll | 输入坐标类型，默认为bd09ll。可选值：bd09ll（百度经纬度坐标）、bd09mc（百度墨卡托坐标）、gcj02（国测局加密坐标）、wgs84（GPS设备获取的坐标）。 | bd09ll |
| ret_coordtype | string (enum: bd09ll, gcj02) |  | bd09ll | 返回结果坐标类型，默认为bd09ll。允许的值：bd09ll（百度经纬度坐标）、gcj02（国测局加密坐标）。 | bd09ll |
| tactics | integer (enum: 0, 3, 4, 5, 6...) |  | 0 | 路线策略，默认为0（默认策略）。可选值：0:默认，3:不走高速，4:高速优先，5:躲避拥堵，6:少收费，7:躲避拥堵&高速优先，8:躲避拥堵&不走高速，9:躲避拥堵&少收费，10:躲避拥堵&不走高速&少收费，11:不走高速&少收费。 | 0 |
| alternatives | integer (enum: 0, 1) |  | 0 | 是否返回备选路线。0:返回一条推荐路线（默认），1:返回1-3条路线供选择。 | 0 |
| plate_number | string |  | - | 车牌号，如"京A00022"，用于规避车牌号限行路段。若有规避限行区域的可选路线，则返回规避后的路线；若无规避限行的可选路线，则返回限行路线中最优路线，并在返回字段restriction中提示。 | 京A00022 |
| displacement | integer |  | - | 摩托车排量，单位cc。取值范围 [0,10000]。 | 250 |
| gps_direction | integer |  | - | 起点的车头方向，取值范围0-359。为与正北方向顺时针夹角，用于辅助判断起点所在正逆向车道。当speed>1.5米/秒且gps_direction存在时，采用该方向。 | 90 |
| radius | number |  | - | 起点的定位精度，单位米，取值范围 [0,2000]。配合gps_direction字段使用。 | 100 |
| speed | number |  | - | 起点车辆的行驶速度，单位：米/秒。配合gps_direction字段使用，当speed>1.5米/秒且gps_direction存在时，采用gps_direction的方向。 | 5.5 |
| output | string (enum: xml, json) |  | json | 输出类型，可设置为xml或json，默认为json。 | json |
| sn | string |  | - | 用户的权限签名，当AK设置为SN校验时，该参数必填。 | 您的SN |
| timestamp | integer |  | - | 时间戳，与SN配合使用，SN存在时必填。 | 1640966400 |
| callback | string |  | - | 回调函数，仅当output=json时该参数有效。 | callbackFunction |

### 响应结果

#### 响应字段定义 (基于 Schema)

| 字段路径 | 类型 | 必填 | 说明 | 示例 |
|----------|------|------|------|------|
| `message` | string | T | 状态码对应的信息 | 成功 |
| `result` | object |  | 返回的结果对象 | None |
| `result.restriction` | string |  | 限行结果提示信息。1: 若无限行路线，则返回空；2: 若无法规避限行，则返回限行提示信息。 | 已为您避开北京限行区域 |
| `result.routes` | array |  | 返回的方案集数组 | None |
| `result.routes[].destination` | object |  | 终点坐标对象 | None |
| `result.routes[].destination.lat` | number |  | 终点纬度 | 40.063597 |
| `result.routes[].destination.lng` | number |  | 终点经度 | 116.364973 |
| `result.routes[].distance` | integer |  | 方案距离，单位:米 | 19337 |
| `result.routes[].duration` | integer |  | 线路耗时，单位:秒 | 1850 |
| `result.routes[].origin` | object |  | 起点坐标对象 | None |
| `result.routes[].origin.lat` | number |  | 起点纬度 | 40.056878 |
| `result.routes[].origin.lng` | number |  | 起点经度 | 116.30815 |
| `result.routes[].restriction_info` | object |  | 限行状态详细信息 | None |
| `result.routes[].restriction_info.desc` | string |  | 限行提示语。当限行status为1或2时，会有相应的限行描述信息。若该路线有多条提示信息，则以英文竖线分隔符分隔。 | 已为您避开北京限行区域 |
| `result.routes[].restriction_info.status` | integer (enum: 0, 1, 2... (共4个值)) |  | 限行状态。取值范围【0,3】。0：无限行；1:已规避限行，路线合法；2:无法规避限行，路线非法；3：疫情相关的信息。 | 1 |
| `result.routes[].steps` | array |  | 路线分段数组 | None |
| `result.routes[].steps[].adcodes` | string |  | 分段途经的城市编码。若途经多个城市，则adcode以英文半角逗号相隔。如：110000,120000 | 110000 |
| `result.routes[].steps[].direction` | integer (enum: 0, 1, 2... (共12个值)) |  | 进入道路的角度。返回值在0-11之间，共12个枚举值，以30度递进。0代表345度到15度（正北方向），以此类推。 | 0 |
| `result.routes[].steps[].distance` | integer |  | step的距离信息，单位:米 | 1000 |
| `result.routes[].steps[].end_location` | object |  | 分段终点坐标 | None |
| `result.routes[].steps[].end_location.lat` | number |  | 分段终点纬度 | 40.057 |
| `result.routes[].steps[].end_location.lng` | number |  | 分段终点经度 | 116.31 |
| `result.routes[].steps[].leg_index` | integer |  | 途径点序号。从0开始的整数，用于标识step所属的途径点路段。如：若该step属于起点至第一个途径中的路段，则其leg_index为0。 | 0 |
| `result.routes[].steps[].path` | string |  | 分段坐标串 | 116.30815,40.056878;116.309,40.057;116.31,40.0571 |
| `result.routes[].steps[].road_name` | string |  | 分段的道路名称，如“信息路”。若道路未命名或百度地图未采集到该道路名称，则返回"无名路"。 | 信息路 |
| `result.routes[].steps[].road_type` | integer (enum: 0, 1, 2... (共10个值)) |  | 分段的道路类型。枚举值0-9：0:高速路，1:城市高速路，2:国道，3:省道，4:县道，5:乡镇村道，6:其他道路，7:九级路，8:航线(轮渡)，9:行人道路。 | 0 |
| `result.routes[].steps[].start_location` | object |  | 分段起点坐标 | None |
| `result.routes[].steps[].start_location.lat` | number |  | 分段起点纬度 | 40.056878 |
| `result.routes[].steps[].start_location.lng` | number |  | 分段起点经度 | 116.30815 |
| `result.routes[].steps[].toll` | integer |  | 分段道路收费，单位:元。因一个收费路段可能覆盖多个step，部分情况下费用无法按step准确拆分，故分段step收费可能存在不准确情况。 | 10 |
| `result.routes[].steps[].toll_distance` | integer |  | 分段道路收费路程，单位:米 | 2000 |
| `result.routes[].steps[].toll_gate_location` | object |  | 收费站位置坐标。只有在进收费站和出收费站时才有。 | None |
| `result.routes[].steps[].toll_gate_location.lat` | number |  | 收费站位置纬度 | 40.12 |
| `result.routes[].steps[].toll_gate_location.lng` | number |  | 收费站位置经度 | 116.35 |
| `result.routes[].steps[].toll_gate_name` | string |  | 收费站名称。只有在进收费站和出收费站时才返回。 | 京哈高速收费站 |
| `result.routes[].steps[].traffic_condition` | array |  | 分分段路况详情数组 | None |
| `result.routes[].steps[].traffic_condition[].distance` | number |  | 距离，从当前坐标点开始path中路况相同的距离，单位:米。注：单条线路中所有distance的和会与route的distance字段存在差异，不是完全一致。 | 500.5 |
| `result.routes[].steps[].traffic_condition[].geo_cnt` | integer |  | 从当前坐标点开始，path中路况相同的坐标点个数 | 10 |
| `result.routes[].steps[].traffic_condition[].status` | integer (enum: 0, 1, 2... (共5个值)) |  | 路况指数。0: 无路况；1: 畅通；2: 缓行；3: 拥堵；4: 非常拥堵。 | 1 |
| `result.routes[].tag` | string |  | 方案标签 | 推荐路线 |
| `result.routes[].taxi_fee` | integer |  | 出租车费用，单位:元 | 45 |
| `result.routes[].toll` | integer |  | 此路线道路收费，单位:元。此高速费为预估价格，与实际高速收费并不完全一致。 | 20 |
| `result.routes[].toll_distance` | integer |  | 收费路段里程，单位:米。此高速费为预估价格，与实际高速收费并不完全一致。 | 5000 |
| `result.total` | integer |  | 返回方案的总数 | 1 |
| `status` | integer | T | 状态码。0:成功；1:服务内部错误；2:参数无效；7:无返回结果。<br/><br/>**枚举值说明：**<br/>`0`: 成功<br/>`1`: 服务内部错误<br/>`2`: 参数无效<br/>`7`: 无返回结果 | 0 |

### 常见问题

**Q: 起点和终点的直线距离限制是多少？**

A: 起点和终点的直线距离不得超过400km。

**Q: 最多支持添加多少个途径点？**

A: 支持18个以内的有序途径点。

**Q: 如何规避限行路段？**

A: 通过plate_number参数传入车牌号，接口会自动规避限行路段。若无法完全规避，会返回限行路线并给出restriction提示。

**Q: 摩托车排量参数displacement的作用是什么？**

A: 用于根据排量差异进行更精准的路线规划和耗时计算，取值范围0-10000cc。

**Q: 返回结果中的direction（进入道路的角度）如何解读？**

A: 返回0-11的枚举值，每个值代表30度范围，0代表345°-15°（正北方向），以此类推。
