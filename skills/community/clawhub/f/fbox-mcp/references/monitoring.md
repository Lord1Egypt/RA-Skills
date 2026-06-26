# 监控点工具详细参考

## 数据层级

```
用户 → 设备(BoxNo) → 监控点分组(GroupName) → 监控点(Name) → 值(Value)
```

操作监控点需逐级定位，每一级都支持模糊匹配和候选建议。

---

## get_user_box_dmon_group_list

获取设备下所有监控点分组。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| BoxNo | string? | 二选一 | 设备序列号 |
| BoxAlias | string? | 二选一 | 设备别名 |
| OnlyOnline | bool? | 否 | 是否要求设备在线 |

**返回字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| Id | long | 分组 ID |
| Name | string | 分组名称 |
| Count | int | 该分组下监控点数量 |

---

## get_user_box_dmon_list

获取指定分组下的所有监控点。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| BoxNo | string? | 二选一 | 设备序列号 |
| BoxAlias | string? | 二选一 | 设备别名 |
| GroupName | string? | 是 | 分组名称（支持模糊匹配） |
| OnlyOnline | bool? | 否 | 是否要求设备在线 |

**返回字段（每个监控点）：**

| 字段 | 类型 | 说明 |
|------|------|------|
| Id | long | 监控点 ID |
| Name | string | 监控点名称 |
| GrpName | string | 所属分组名称 |
| DataType | enum | 数据类型：Bit / UInt16 / Int16 / Int32 / UInt32 / Single / Double / String 等 |
| Unit | string? | 单位（℃、V、A、rpm 等） |
| Privilege | enum | 读写权限：Read(4) / Write(2) / ReadWrite(6) |
| IntDigits | int | 整数位数 |
| FracDigits | int | 小数位数 |
| DeadValue | float | 死区值 |
| Memo | string? | 备注 |
| DevAlias | string? | PLC 设备别名 |
| AddrDesc | string? | 地址描述 |
| ExecuteOnEdge | bool | 是否开启边缘运算 |

---

## get_user_box_dmon_info

获取单个监控点的详细配置信息。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| BoxNo | string? | 二选一 | 设备序列号 |
| BoxAlias | string? | 二选一 | 设备别名 |
| GroupName | string? | 是 | 分组名称 |
| Name | string? | 是 | 监控点名称（支持模糊匹配） |
| OnlyOnline | bool? | 否 | 是否要求设备在线 |

**返回：** 同 get_user_box_dmon_list 中的监控点字段。

---

## get_user_box_dmon_value

读取监控点的当前实时值。

**参数：** 同 get_user_box_dmon_info

**返回字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| Id | long | 监控点 ID |
| Name | string? | 监控点名称 |
| DataType | enum | 数据类型 |
| Value | object? | 当前值（Bit→bool，数值→number，String→string） |
| Status | enum | 状态：Normal(0) / NoValue(1) / Timeout(2) / Error(3) |
| Timestamp | DateTime? | 值更新时间（UTC） |
| BoxId | long | 设备 ID |
| ConnState | enum | 设备连接状态 |
| ConnStateTimestamp | DateTime? | 设备上线时间（UTC） |

**注意：** 先检查 `Status` 是否为 Normal，非正常状态下 Value 可能无意义。

---

## write_user_box_dmon_value

向监控点写入新值。**直接影响现场设备运行状态。**

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| BoxNo | string? | 二选一 | 设备序列号 |
| BoxAlias | string? | 二选一 | 设备别名 |
| GroupName | string? | 是 | 分组名称 |
| Name | string? | 是 | 监控点名称 |
| Value | string | **是** | 写入值（字符串形式，Bit 传 "true"/"false"，数值传数字字符串） |
| Confirmed | bool | **是** | 必须为 true 才执行写入 |
| OnlyOnline | bool? | 否 | 是否要求设备在线 |

**安全要求：**
1. 监控点 `Privilege` 必须包含 Write 权限
2. `Confirmed` 必须显式设为 `true`
3. 只有在线设备才能写入
4. **写入前必须先读取当前值展示给用户，获得明确确认后才执行**
