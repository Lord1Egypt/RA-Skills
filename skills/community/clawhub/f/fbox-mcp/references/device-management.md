# 设备管理工具详细参考

## get_user_box_stats

获取当前用户的设备统计概览。

**参数：** 无

**返回字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| BoxCount | int | 设备总数 |
| OnlineBoxCount | int | 在线设备数 |
| AlarmBoxCount | int | 存在报警的设备数 |
| AlarmCount | int | 当前报警总数 |

---

## get_user_box_list

获取用户所有设备，按分组返回。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| OnlyOnline | bool? | 否 | 是否仅返回在线设备，默认 true |

**返回：** 设备分组列表，每组包含组名和设备列表。

**设备字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| Id | long | 设备 ID |
| BoxNo | string | 设备序列号（唯一标识，后续操作的关键） |
| Alias | string | 设备别名（用户自定义名称） |
| BoxType | enum | 型号：Standard / Mini / Lite / Vpn / FLink / FL3 / HMI / Lite_V5 / Q0 / Desktop |
| Net | enum | 上网方式：Ethernet(1) / WIFI(4) / 4G(5) / 5G(9) |
| ConnState | enum | 连接状态：Online / Offline / TimedOut / Unavailable / Undetermined |
| AlarmCount | int | 当前报警数量 |
| Owned | bool | 是否自有设备 |
| Given | bool | 是否来自他人分享 |
| OwnerUserName | string? | 分享者用户名 |
| AllowUpgrade | bool | 是否可固件升级 |
| SoftwareVersions | dict? | 固件版本信息 |
| Memo | string? | 备注 |

---

## get_user_box_info

获取单个设备的详细信息。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| BoxNo | string? | 二选一 | 设备序列号 |
| BoxAlias | string? | 二选一 | 设备别名（支持模糊匹配） |
| OnlyOnline | bool? | 否 | 是否要求设备在线 |

**模糊匹配机制：** 当无法精确匹配时，服务返回 Code=300 + 候选列表。AI 应将候选项展示给用户选择，然后使用选中项的 `value`（BoxNo）重新调用。

**返回字段：** 同 get_user_box_list 中的设备字段。

---

## get_user_box_settings

获取设备系统级配置信息。

**参数：** 同 get_user_box_info

**返回：** 配置类型和值的键值对列表，包含：
- IP 地址、子网掩码、网关、DNS
- 固件版本、网络类型
- 双网口信息等

---

## get_user_box_location

获取设备地理位置。

**参数：** 同 get_user_box_info

**返回字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| Longitude / Latitude | double? | 设备上报的经纬度 |
| Address | string? | 设备上报的详细地址 |
| LocationFetchType | enum | 位置来源：Box（设备自动定位）/ User（人工标注） |
| UseLongitude / UseLatitude | double? | 用户手动设置的经纬度 |
| UseAddress | string? | 用户手动设置的地址 |

根据 `LocationFetchType` 决定使用哪组坐标。

---

## get_sim_card_info

获取物联网 SIM 卡信息。一个设备可能有主卡和副卡，返回值为列表。

**参数：** 同 get_user_box_info

**返回字段（每张卡）：**

| 字段 | 类型 | 说明 |
|------|------|------|
| TotalDataVolume | double | 本月可用流量（MB） |
| DataUsage | double | 本月已用流量（MB） |
| ExpireDate | DateTime | 套餐过期时间（UTC） |
| Status | string? | 业务状态 |
| DeviceStatus | string? | 联网状态 |
| Carrier | string? | 运营商 |
| RatePlanName | string? | 套餐名称 |

---

## get_user_box_plc_list

获取 FBox 盒子连接的 PLC 控制器列表。

**参数：** 同 get_user_box_info

**返回字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| PlcId | int | PLC 编码 |
| PlcName | string? | PLC 名称 |
| Alias | string? | PLC 别名 |
| Type | enum | 通讯方式：Serial（串口）/ Ethernet（以太网） |
| Class | enum | 主从类型：Master / Slave / MasterSlave |
| Ip | string? | PLC IP（以太网时） |
| Port | int | 端口号 |

