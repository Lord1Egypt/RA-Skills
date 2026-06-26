# 历史数据工具详细参考

## 数据层级

```
设备(BoxNo) → 历史数据条目(ItemName) → 数据通道(ChannelName) → 时间序列(Timestamp + Value)
```

## 采样类型

| 类型 | 说明 |
|------|------|
| Cycle | 按固定时间间隔周期采集 |
| Trigger | 满足特定条件时触发采集 |

---

## get_history_data_define_list

获取设备上配置的历史数据采集条目。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| BoxNo | string? | 二选一 | 设备序列号 |
| BoxAlias | string? | 二选一 | 设备别名 |
| OnlyOnline | bool? | 否 | 是否要求设备在线 |

**返回字段（每个条目）：**

| 字段 | 类型 | 说明 |
|------|------|------|
| Uid | long | 条目 ID |
| Name | string? | 条目名称（后续查询用） |
| Period | int | 采样周期 |
| SampleType | enum | Cycle / Trigger |
| Channels | list | 数据通道列表 |

**通道字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| Uid | long | 通道 ID |
| Name | string? | 通道名称 |
| Unit | string? | 单位 |
| DataType | enum | 数据类型 |

---

## get_history_data_list

查询历史数据记录。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| BoxNo | string? | 二选一 | 设备序列号 |
| BoxAlias | string? | 二选一 | 设备别名 |
| ItemName | string? | 是 | 条目名称（支持模糊匹配） |
| ChannelName | string? | 否 | 通道名称，不填查询全部通道 |
| Granularity | enum | 否 | 数据粒度，默认 Raw |
| BeginTime | DateTime? | 否 | 开始时间（UTC），默认 5 天前 |
| EndTime | DateTime? | 否 | 结束时间（UTC），默认当前时间 |
| Limit | ushort? | 否 | 最大返回条数，默认 20，最大 100 |
| OnlyOnline | bool? | 否 | 是否要求设备在线 |

### 数据粒度（Granularity）

| 值 | 说明 | 场景 |
|----|------|------|
| Raw | 原始采样数据（默认） | 查看每条精确记录 |
| Minutely | 按分钟聚合 | 短期趋势 |
| Hourly | 按小时聚合 | 中期趋势 |
| Daily | 按天聚合 | 长期趋势 |

非 Raw 粒度使用 First 聚合函数（取每个时间段第一条数据）。

**返回结构：**

| 字段 | 类型 | 说明 |
|------|------|------|
| ChannelNames | string[] | 通道名称列表（表头） |
| Rows | list | 数据行列表 |

**行字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| Timestamp | long | UTC 毫秒时间戳 |
| Value | object[] | 值列表，按索引对应 ChannelNames |

**展示建议：** 以表格呈现，第一列为时间（转北京时间），后续列为各通道值。大时间范围用 Granularity 降采样获取趋势概览。
