# 驾车路线规划-建议出发时间

## 服务概述

该功能需要开通高级权限，开发者设置预期到达时间后,将返回建议出发时间

- **版本**: 2.0.0
- **服务标识**: `suggested_departure_time`
- **官方文档**: <https://lbs.baidu.com/faq/api?title=webapi/webservice-direction-suggtime>

### API调用

**GET** `https://api.map.baidu.com/direction/v2/driving`

### 输入参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 | 示例 |
|--------|------|------|--------|------|------|
| expect_arrival_time | string |  | - | 预期到达时间，UNIX时间戳。取值范围：当前时间之后15分钟任意时刻。设置后将返回suggest_departure_time字段, （小于这个时间则不做处理）若设置此参数，则路线规划服务将依据设定时间计算路线和耗时，并给出建议出发时间, 若算出的suggest_departure_time小于当前时间，则设置suggest_departure_time为-1 | 1609462800 |

### 响应结果

#### 响应字段定义 (基于 Schema)

| 字段路径 | 类型 | 必填 | 说明 | 示例 |
|----------|------|------|------|------|
| `message` | string |  | 状态码对应的信息 | 成功 |
| `result` | object |  | 返回的结果 | None |
| `result.routes` | array |  | 返回的方案集 | None |
| `result.routes[].suggest_departure_time` | integer \| null |  | 建议出发时间，单位：秒。当设置了expect_arrival_time时返回，按照预计到达时间预测路况计算路线，并给出建议出发时间，若计算出的时间小于当前时间则返回-1。 | 1609459200 |
| `status` | integer |  | 本次API访问状态码<br/><br/>**枚举值说明：**<br/>`0`: 成功<br/>`1`: 服务内部错误<br/>`2`: 参数无效<br/>`7`: 无返回结果 | 0 |

### 常见问题

**Q: 该高级功能是否可以直接使用?**

A: 需要先开通对应的高级权限
