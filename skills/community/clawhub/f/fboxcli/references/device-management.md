# 设备管理命令参考

## box list

列出所有 FBox 设备（按分组），显示 ID、别名、序列号、连接状态。

```bash
fboxcli box list [--json]
```

**参数：** 无

**返回字段（每个设备）：**

| 字段 | 类型 | 说明 |
|------|------|------|
| id | long | 设备 ID（后续操作的关键） |
| alias | string | 设备别名 |
| boxNo | string | 设备序列号 |
| connState | enum | 连接状态：Online / Offline / TimedOut / Unavailable |
| alarmCount | int | 当前报警数量 |
| boxType | enum | 型号：Standard / Mini / Lite / Vpn / FLink 等 |

**示例：**

```bash
fboxcli box list --json
```

---

## box get

按序列号获取单个 FBox 信息。

```bash
fboxcli box get <BOX_NO> [--json]
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| BOX_NO | string | 是 | FBox 序列号 |

**返回：** 同 box list 中的设备字段。

**示例：**

```bash
fboxcli box get FB001234 --json
```

---

## box add

添加新的 FBox 到账号下。

```bash
fboxcli box add <BOX_NO> <PASSWORD> [OPTIONS]
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| BOX_NO | string | 是 | FBox 序列号 |
| PASSWORD | string | 是 | FBox 密码 |
| --alias | string | 否 | 设备别名 |
| --group | string | 否 | 分组名称 |

**示例：**

```bash
fboxcli box add FB001234 fboxpassword --alias "车间1号" --group "生产车间"
```

---

## box rename

重命名 FBox 设备。

```bash
fboxcli box rename <BOX_ID> <ALIAS>
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| BOX_ID | long | 是 | FBox ID（数字） |
| ALIAS | string | 是 | 新别名 |

---

## box delete

删除 FBox 设备。⚠️ 需用户确认。

```bash
fboxcli box delete <BOX_ID>
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| BOX_ID | long | 是 | FBox ID（数字） |

---

## box info

获取 FBox 详细配置信息（IP、DNS、固件版本等）。

```bash
fboxcli box info <BOX_ID> [--json]
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| BOX_ID | long | 是 | FBox ID（数字） |

**返回：** 配置类型和值的键值对列表，包含 IP 地址、子网掩码、网关、DNS、固件版本等。

---

## box memo

设置 FBox 备注信息。

```bash
fboxcli box memo <BOX_ID> <CONTENT>
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| BOX_ID | long | 是 | FBox ID（数字） |
| CONTENT | string | 是 | 备注内容 |

---

## group list

列出所有 FBox 分组。

```bash
fboxcli group list [--json]
```

**返回字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| id | long | 分组 ID |
| name | string | 分组名称 |

> 注：分组信息也包含在 `box list` 的返回中。

---

## group add

新增 FBox 分组。

```bash
fboxcli group add <NAME> [OPTIONS]
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| NAME | string | 是 | 分组名称 |
| --parent | long | 否 | 父分组 ID |

---

## group rename

重命名分组。

```bash
fboxcli group rename <GROUP_ID> <NAME>
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| GROUP_ID | long | 是 | 分组 ID |
| NAME | string | 是 | 新名称 |

---

## group delete

删除分组。⚠️ 需用户确认。

```bash
fboxcli group delete <GROUP_ID>
```

---

## device list

列出 FBox 连接的 PLC/设备列表。

```bash
fboxcli device list <BOX_ID> [--json]
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| BOX_ID | long | 是 | FBox ID（数字） |

**返回字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| id | long | 设备 ID |
| name | string | 设备名称 |
| alias | string | 设备别名 |
| type | enum | 通讯方式：Serial / Ethernet |
| class | enum | 主从类型：Master / Slave / MasterSlave |
| ip | string? | PLC IP（以太网时） |
| port | int | 端口号 |

---

## device drivers

列出服务器支持的驱动列表。

```bash
fboxcli device drivers [BOX_TYPE] [--json]
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| BOX_TYPE | int | 否 | 盒子类型：0=标准, 1=Mini, 2=Lite, 3=VPN [默认: 0] |

---

## device registers

获取指定设备的寄存器详细信息。

```bash
fboxcli device registers <DEVICE_ID> [--json]
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| DEVICE_ID | long | 是 | 设备 ID |

---

## location

获取一个或多个 FBox 的地理位置信息。

```bash
fboxcli location <IDS> [--json]
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| IDS | string | 是 | 逗号分隔的 FBox ID |

**返回字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| longitude / latitude | double? | 经纬度 |
| address | string? | 详细地址 |
