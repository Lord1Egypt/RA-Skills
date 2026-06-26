# 报警管理工具详细参考

## 报警生命周期

```
正常运行 → [条件触发] → Triggered(报警中)
                         ├→ [用户确认] → Confirmed(已确认)
                         └→ [条件恢复] → Recovered(已恢复)
```

| 状态 | 含义 |
|------|------|
| Triggered | 报警已触发，等待处理 |
| Confirmed | 已被操作员确认知晓 |
| Recovered | 触发条件已恢复正常 |

---

## get_alarm_define_list

获取设备上配置的报警规则（仅返回已启用的）。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| BoxNo | string? | 二选一 | 设备序列号 |
| BoxAlias | string? | 二选一 | 设备别名 |
| OnlyOnline | bool? | 否 | 是否要求设备在线 |
| SkipCount | int | 否 | 跳过条数，默认 0 |
| MaxResultCount | int | 否 | 最大返回条数，默认 1000 |

**返回字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| Id | long | 报警定义 ID |
| Code | int | 报警编码 |
| Name | string? | 报警名称 |
| AlarmMsg | string? | 报警内容模板 |
| Memo | string? | 备注 |
| Condition1 / Condition2 | enum | 触发条件：Eq(==) / Neq(!=) / Gt(>) / Gte(>=) / Lt(<) / Lte(<=) |
| Operand1 / Operand2 | double | 比较值 |
| CondMethod | enum | 组合方式：None / And / Or |

---

## get_current_alarm_list

获取设备当前正在触发的报警。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| BoxNo | string? | 二选一 | 设备序列号 |
| BoxAlias | string? | 二选一 | 设备别名 |
| OnlyOnline | bool? | 否 | 是否要求设备在线 |

**返回字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| Id | long | 报警实例 ID |
| Code | int | 报警编码 |
| Name | string? | 报警名称 |
| AlarmMsg | string? | 报警内容 |
| AlarmState | enum | Triggered / Confirmed / Recovered |
| LastTriggeredTime | DateTime? | 最后触发时间（UTC） |
| LastRecoveredTime | DateTime? | 最后恢复时间（UTC） |
| ValueOnLastEvent | object? | 最后触发/恢复时的值 |
| DataType | enum | 值的数据类型 |
| Memo | string? | 备注 |

---

## confirm_current_alarm

确认指定报警，表示操作员已知晓。确认不会消除报警，只是标记状态。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| BoxNo | string? | 二选一 | 设备序列号 |
| BoxAlias | string? | 二选一 | 设备别名 |
| AlarmName | string? | 是 | 报警名称（需精确匹配 get_current_alarm_list 返回的 Name） |
| OnlyOnline | bool? | 否 | 是否要求设备在线 |

**操作流程：** 先调用 `get_current_alarm_list` 获取报警列表展示给用户 → 用户指定要确认的报警 → 使用报警的 `Name` 字段调用本工具。

---

## get_alarm_history_list

查询报警历史记录。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| BoxNo | string? | 二选一 | 设备序列号 |
| BoxAlias | string? | 二选一 | 设备别名 |
| AlarmName | string? | 否 | 报警名称过滤，不填查询全部 |
| BeginTime | DateTime? | 否 | 开始时间（UTC），默认 7 天前 |
| EndTime | DateTime? | 否 | 结束时间（UTC），默认当前时间 |
| Limit | ushort? | 否 | 最大返回条数，默认 20，最大 100 |
| OnlyOnline | bool? | 否 | 是否要求设备在线 |

**返回字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| Timestamp | long | 时间戳（UTC 毫秒） |
| AlarmId | long | 报警定义 ID |
| Action | enum | Trigger（触发）/ Confirm（确认）/ Recover（恢复） |
| Code | string? | 报警编码 |
| Name | string? | 报警名称 |
| Message | string? | 报警内容 |
| Value | object? | 触发时的值 |

时间参数为 UTC，先调用 `utc_now` 获取服务器时间来计算范围。结果以表格形式展示，时间转北京时间。
