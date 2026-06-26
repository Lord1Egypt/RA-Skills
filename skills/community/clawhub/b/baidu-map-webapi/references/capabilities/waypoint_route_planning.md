# 驾车路线规划-途经点智能路线规划

## 服务概述

该功能需要开通高级权限，传入多个途经点，综合考虑路况、交规限行、 途经点的相对位置以及路线整体的绕路成本等，支持智能调整途经点顺序，给出最优路线。

- **版本**: 2.0.0
- **服务标识**: `waypoint_route_planning`
- **官方文档**: <https://lbs.baidu.com/faq/api?title=webapi/webservice-direction-aiplan>

### API调用

**GET** `https://api.map.baidu.com/direction/v2/driving`

### 输入参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 | 示例 |
|--------|------|------|--------|------|------|
| intelligent_plan | integer (enum: 0, 1) |  | 0 | 是否执行途经点智能规划，综合考虑路况、限行、途经点相对位置及绕路成本，支持智能调整途经点顺序可选值：0（默认值）：不执行途经点智能规划1：执行途经点智能规划（高级权限服务）。 | 1 |

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
