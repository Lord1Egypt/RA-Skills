# 监控点命令参考

## 数据层级

```
用户 → 设备(BOX_ID) → 监控点分组 → 监控点(ID/Name) → 值(Value)
```

操作监控点需先通过 `box list` 获取 `BOX_ID`，再通过 `dmon list` 获取监控点 ID。

---

## dmon list

列出 FBox 的所有监控点（按分组），显示 ID、名称、数据类型、读写权限。

```bash
fboxcli dmon list <BOX_ID> [--json]
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| BOX_ID | long | 是 | FBox ID（数字） |

**返回字段（每个监控点）：**

| 字段 | 类型 | 说明 |
|------|------|------|
| id | long | 监控点 ID |
| name | string | 监控点名称 |
| groupName | string | 所属分组 |
| dataType | enum | 数据类型：Bit / UInt16 / Int16 / Int32 / UInt32 / Single / Double / String 等 |
| unit | string? | 单位（℃、V、A、rpm 等） |
| privilege | enum | 读写权限：Read(4) / Write(2) / ReadWrite(6) |
| intDigits | int | 整数位数 |
| fracDigits | int | 小数位数 |
| memo | string? | 备注 |

---

## dmon get-value

获取监控点的实时值。可按 ID 或名称查询。

```bash
fboxcli dmon get-value <BOX_ID> [OPTIONS] [--json]
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| BOX_ID | long | 是 | FBox ID（数字） |
| --ids | string | 二选一 | 逗号分隔的监控点 ID |
| --names | string | 二选一 | 逗号分隔的监控点名称 |
| --timeout | int | 否 | 超时时间，毫秒 [默认: 5000] |

**返回字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| id | long | 监控点 ID |
| name | string | 监控点名称 |
| value | object? | 当前值（Bit→bool，数值→number，String→string） |
| status | enum | 状态：Normal(0) / NoValue(1) / Timeout(2) / Error(3) |
| timestamp | DateTime? | 值更新时间 |

**注意：** 先检查 `status` 是否为 Normal，非正常状态下 value 可能无意义。

**示例：**

```bash
# 按 ID 获取
fboxcli dmon get-value 12345 --ids 1001,1002 --json

# 按名称获取
fboxcli dmon get-value 12345 --names "温度,压力" --json
```

---

## dmon set-value

向监控点写入值。⚠️ 写操作，需用户确认。

```bash
fboxcli dmon set-value <BOX_ID> --value <VALUE> [OPTIONS]
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| BOX_ID | long | 是 | FBox ID（数字） |
| --id | long | 二选一 | 监控点 ID |
| --name | string | 二选一 | 监控点名称 |
| --value | string | **是** | 写入值（Bit 传 true/false，数值传数字） |

**安全要求：**
1. 监控点 `privilege` 必须包含 Write 权限
2. 写入前先通过 `dmon get-value` 读取当前值展示给用户
3. **用户确认后才能执行**

**示例：**

```bash
# 按 ID 写值
fboxcli dmon set-value 12345 --id 1001 --value 100

# 按名称写值
fboxcli dmon set-value 12345 --name "目标温度" --value 75.5
```

---

## dmon start

开启数据推送。省略 `--uid` 时开启 FBox 下所有监控点的推送。

```bash
fboxcli dmon start <BOX_ID> [--uid <UID>]
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| BOX_ID | long | 是 | FBox ID（数字） |
| --uid | long | 否 | 指定单个监控点 UID（省略则全部） |

---

## dmon stop

停止数据推送。省略 `--uid` 时停止 FBox 下所有监控点的推送。

```bash
fboxcli dmon stop <BOX_ID> [--uid <UID>]
```

**参数：** 同 dmon start。

---

## dmon groups

列出监控点分组。

```bash
fboxcli dmon groups <BOX_ID> [--json]
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| BOX_ID | long | 是 | FBox ID（数字） |

---

## dmon delete

删除监控点。⚠️ 需用户确认。

```bash
fboxcli dmon delete <BOX_ID> --ids <IDS>
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| BOX_ID | long | 是 | FBox ID（数字） |
| --ids | string | 是 | 逗号分隔的监控点 ID |

**示例：**

```bash
fboxcli dmon delete 12345 --ids 1001,1002
```
