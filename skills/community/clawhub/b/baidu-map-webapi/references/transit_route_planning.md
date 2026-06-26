# 百度地图公交路线规划 API

## 服务概述

提供公交、地铁、步行等多种交通方式组合的路线规划服务，支持同城与跨城出行方案。

- **版本**: 2.0.0
- **服务标识**: `direction_v2_transit`
- **官方文档**: <https://lbs.baidu.com/faq/api?title=webapi/webservice-direction/transit>

### API调用

**GET** `https://api.map.baidu.com/direction/v2/transit`

### 输入参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 | 示例 |
|--------|------|------|--------|------|------|
| origin | string | T | - | 起点坐标，格式为：纬度,经度，小数点后不超过6位，如：“40.056878,116.30815” | 40.056878,116.30815 |
| destination | string | T | - | 终点坐标，格式为：纬度,经度，小数点后不超过6位，如：“40.056878,116.30815” | 31.222965,121.505821 |
| origin_uid | string |  | - | POI 的 uid（在已知起点POI 的 uid 情况下，请尽量填写uid，将提升路线规划的准确性） | - |
| destination_uid | string |  | - | POI 的 uid（在已知终点POI 的 uid 情况下，请尽量填写uid，将提升路线规划的准确性） | - |
| coord_type | string (enum: bd09ll, bd09mc, gcj02, wgs84) |  | bd09ll | 起终点的坐标类型，默认为bd09ll | - |
| departure_date | string |  | - | 出发日期。若不填默认规则如下：1. 若为起终点为同城：则默认为当天 2. 若为起终点为跨城：则默认第二天 | - |
| departure_time | string |  | - | 出发时间区间，格式为：1. hh:mm-hh:mm，如”08:00-14:00” 2. hh:mm，如”08:00” | - |
| tactics_incity | integer (enum: 0, 1, 2, 3, 4...) |  | 0 | 市内公交换乘策略，默认为0,0:推荐,1:少换乘,2:少步行,3:不坐地铁,4:时间短,5:地铁优先 | - |
| tactics_intercity | integer (enum: 0, 1, 2) |  | 0 | 跨城公交换乘策略，默认为0,0:时间短,1:出发早,2:价格低 | - |
| trans_type_intercity | integer (enum: 0, 1, 2) |  | 0 | 跨城交通方式策略，默认为0,0:火车优先,1 :飞机优先,2:大巴优先 | - |
| ret_coordtype | string (enum: bd09ll, gcj02) |  | bd09ll | 返回值的坐标类型，默认为bd09ll | - |
| output | string (enum: json, xml) |  | json | 输出类型，默认为json | - |
| page_size | integer |  | 10 | 返回每页几条路线，默认为10 | 10 |
| page_index | integer |  | 1 | 返回第几页，默认为1 | 1 |
| ak | string | T | - | 开发者密钥AK | 您的AK |
| sn | string |  | - | 用户的权限签名，当AK设置为SN校验时，该参数必填 | - |
| timestamp | integer |  | - | 时间戳，与SN配合使用，SN存在时必填 | - |
| callback | string |  | - | 回调函数，用于解决浏览器请求跨域问题，仅再output=json时，该参数有效 | - |

### 响应结果

#### 响应字段定义 (基于 Schema)

| 字段路径 | 类型 | 必填 | 说明 | 示例 |
|----------|------|------|------|------|
| `message` | string |  | 状态码对应的文本描述 | ok |
| `result` | object \| null |  | 返回结果，如果status为1001 或1002，此字段为null | None |
| `result.destination` | object |  |  | None |
| `result.destination.city_id` | string |  | 城市id | None |
| `result.destination.city_name` | string |  | 城市名字 | None |
| `result.destination.location` | object |  |  | None |
| `result.destination.location.lat` | number |  | 坐标系由ret_coordtype设置 | None |
| `result.destination.location.lng` | number |  | 坐标系由ret_coordtype设置 | None |
| `result.origin` | object |  |  | None |
| `result.origin.city_id` | string |  | 城市id | None |
| `result.origin.city_name` | string |  | 城市名字 | None |
| `result.origin.location` | object |  |  | None |
| `result.origin.location.lat` | number |  | 坐标系由ret_coordtype设置 | None |
| `result.origin.location.lng` | number |  | 坐标系由ret_coordtype设置 | None |
| `result.routes` | array |  | 请求中指定的page_index 和page_size 的部分。数组元素个数为page_size，每个元素代表从起点到终点的一条路线。 | None |
| `result.routes[].arrive_time` | string |  |  | 2016-04-05 17:06:10 |
| `result.routes[].distance` | integer |  |  | None |
| `result.routes[].duration` | integer |  |  | None |
| `result.routes[].price` | number |  | 境外地区此字段值为null | None |
| `result.routes[].price_detail` | array |  | 起终点为境内同城时此字段为一个数组，数组中的每一项都有ticket_type 和ticket_price 两个字段；起终点为境内跨城时，该字段为一个空的数组。 | None |
| `result.routes[].price_detail[].ticket_price` | number |  | 本类型的票的总价 | None |
| `result.routes[].price_detail[].ticket_type` | integer (enum: 0, 1) |  | 0 公交票价；1 地铁票价 | None |
| `result.routes[].steps` | array |  | 数组，数组中的每一项是一步（step）。每条路线都由多个step组成。 | None |
| `result.taxi` | object |  | 仅在同城请求时才完整返回 | None |
| `result.taxi.detail` | array |  | 详细信息 | None |
| `result.taxi.detail[].desc` | string |  | 仅在同城请求时才返回 | None |
| `result.taxi.detail[].km_price` | number |  | 仅在同城请求时才返回 | None |
| `result.taxi.detail[].start_price` | number |  | 仅在同城请求时才返回 | None |
| `result.taxi.detail[].total_price` | number |  | 仅在同城请求时才返回 | None |
| `result.total` | integer |  | 符合条件的所有routes 的总数 | None |
| `status` | integer |  | 本次API访问状态码<br/><br/>**枚举值说明：**<br/>`0`: 成功<br/>`1`: 服务器内部错误<br/>`2`: 参数无效<br/>`1001`: 没有公交方案<br/>`1002`: 不支持跨域 | 0 |

### 常见问题

**Q: 起点和终点的坐标格式是什么？**

A: 格式为纬度,经度，小数点后不超过6位，例如：40.056878,116.30815

**Q: 如何提升路线规划的准确性？**

A: 在已知起点或终点POI的情况下，请尽量填写对应的origin_uid或destination_uid参数。

**Q: 如何区分同城和跨城查询的返回结果？**

A: 同城时，taxi字段下的desc、km_price等字段会返回；跨城时，price_detail字段可能为空数组，且交通方式可能包含火车、飞机等。
