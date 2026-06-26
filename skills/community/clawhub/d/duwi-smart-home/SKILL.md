---
name: duwi-smart-home
displayName: Duwi Smart Home
version: 1.0.6
summary: 迪惟智能家居控制技能，支持灯光、窗帘、空调、地暖等设备控制
description: 迪惟智能家居技能，基于 Duwi 开放平台 API，支持设备控制、场景执行、状态查询等功能
author: 迪惟科技
tags: [duwi,smart-home, iot, device-control, home-automation]
---

# Duwi 迪惟智能家居技能

基于 Duwi 开放平台 API，支持设备控制、场景执行、状态查询等功能。

## 功能特性

### 房屋管理
- 多房屋支持
- 楼层管理
- 房间管理

### 状态查询
- 设备在线状态
- 设备实时数值（温度、湿度、光照度、电压、电流等）
- 传感器历史统计数据
- 用电量统计数据

### 设备控制
- **电源断路器控制**：开关控制等
- **灯光控制**：开关、亮度调节 (0-100%)、色温调节 (2700-6200K)、颜色调整（HSV 格式）等
- **窗帘控制**：开/关/停、百分比 (0-100%)、角度调节等
- **空调控制**：开关、温度设置 (5-35℃)、模式设置、风速设置、风向设置等
- **地暖控制**：开关、温度设置 (10-30℃) 等
- **新风控制**：开关、湿度设置（0-100%）、风速设置、工作模式设置等
- **热泵控制**：开关、温度设置、模式设置等
- **二联供控制**：开关、模式设置、温度设置（5-35℃）、湿度设置（0-100%）、风速控制等

### 场景控制
- 场景列表查询
- 场景执行

## 快速开始

### 1. 配置应用凭证

**配置前确认：**
- ✅ 你已从迪惟开放平台获取了 APPKEY 和 SECRET

**方式 1：非交互模式（适合大模型）**
```bash
python init_config.py --appkey <APPKEY> --secret <SECRET>
```

**方式 2：交互模式**
```bash
python init_config.py
```
按提示输入 APPKEY 和 SECRET（输入时 SECRET 会隐藏显示）。

### 2. 登录账户

**方式 1：提供密码**
```bash
python duwi_cli.py login <手机号> <密码>
```

**方式 2：不输入密码（会提示输入，隐藏显示）**
```bash
python duwi_cli.py login <手机号>
```

### 3. 选择房屋

**方式 1：交互选择**
```bash
python duwi_cli.py choose-house
```
按提示选择房屋。

**方式 2：直接指定房屋编号（推荐，无需交互）**
```bash
python duwi_cli.py choose-house --house_no <房屋编号>
```

### 4. 开始控制
```bash
python duwi_cli.py device-operate switch on --room 客厅 --device_name 顶灯
```

---

## 功能参考

### 账户管理
| 功能 | CLI 指令 |
|------|---------|
| 登录 | `python duwi_cli.py login <手机号> [密码]` |
| 退出 | `python duwi_cli.py logout` |

**💡 提示**：登录成功后 token 会自动保存，下次使用无需重新登录。Token 过期时会自动刷新。

### 房屋管理
| 功能 | CLI 指令 |
|------|---------|
| 房屋列表 | `python duwi_cli.py houses` |
| 选择房屋 | `python duwi_cli.py choose-house --house_no <编号>` |
| 楼层列表 | `python duwi_cli.py floors` |
| 房间列表 | `python duwi_cli.py rooms [--floor <楼层名>]` |

**大模型提示：** 通过楼层名称查找房间列表，未找到相应的楼层时，先查找楼层列表，匹配相似的楼层名称，再通过精准楼层名称查找房间列表。

### 设备查询
| 功能 | CLI 指令 |
|------|---------|
| 设备列表 | `python duwi_cli.py devices [--room <房间>] [--floor <楼层>] [--online]` |
| 设备详情 | `python duwi_cli.py device-info <设备编号>` |
| 设备状态 | `python duwi_cli.py device-value <设备编号>` |

**大模型提示：** 设备列表的查询支持 `--floor`（楼层）、`--room`（房间）、`--online`（是否在线）、`--type`（设备类型编号）参数来精确定位设备，参数可选，可同时传入多个参数。

### 设备控制

**命令格式：** `python duwi_cli.py device-operate <动作> <值> [定位参数]`

**定位参数优先级：** `--device_no` > `--floor + --room + --device_name` > `--room + --device_name` > `--device_name`

| 设备类型(类型前缀) | 动作 | 动作说明 | 值说明 | 示例 |
|---------|------|---------|--------|------|
| **电源** (1-*) | `switch` | 开关 | `on`/`off` | `switch on --room 客厅 --device_name 断路器` |
| **灯光** (3-*) | `switch` | 开关 | `on`/`off` | `switch off --room 卧室 --device_name 顶灯` |
| | `light` | 调光 | 亮度 (0-100) | `light 80 --room 客厅 --device_name 灯带` |
| | `color_temp` | 调色温 | 色温 (2700-6200K) | `color_temp 4000 --room 书房 --device_name 台灯` |
| | `color` | 调色 | HSV 格式 (H:S:V) | `color 180:100:100 --room 卧室 --device_name 灯` |
| **窗帘** (4-*) | `control` | 开关停 | `open`/`close`/`stop` | `control open --room 客厅 --device_name 窗帘` |
| | `control_percent` | 设开合度 | 百分比 (0-100) | `control_percent 50 --room 主卧 --device_name 窗帘` |
| **空调** (5-001) | `ac_switch` | 开关 | `on`/`off` | `ac_switch on --room 客厅 --device_name 空调` |
| | `ac_set_temp` | 设温度 | 温度 (5-35℃) | `ac_set_temp 26 --room 客厅 --device_name 空调` |
| | `ac_mode` | 设模式 | `auto`/`cold`/`hot`/`fan`/`wet` | `ac_mode cold --room 卧室 --device_name 空调` |
| | `ac_wind_speed` | 设风速 | `auto`/`high`/`mid`/`low` | `ac_wind_speed mid --room 客厅 --device_name 空调` |
| | `ac_wind_direction` | 设风向 | `auto`/`stop`/`swing`/`up_down`/`left_right` | `ac_wind_direction auto --room 客厅 --device_name 空调` |
| | `ac_lock_mode` | 设锁定模式 | `lock`/`half_lock`/`unlock` | `ac_lock_mode lock --room 客厅 --device_name 空调` |
| **地暖** (5-002) | `fh_switch` | 开关 | `on`/`off` | `fh_switch on --device_name 地暖` |
| | `fh_set_temp` | 设温度 | 温度 (10-30℃) | `fh_set_temp 25 --device_name 地暖` |
| | `fh_lock_mode` | 设锁定模式 | `lock`/`half_lock`/`unlock` | `fh_lock_mode lock --device_name 地暖` |
| **新风** (5-003) | `fa_switch` | 开关 | `on`/`off` | `fa_switch on --device_name 新风机` |
| | `fa_work_mode` | 设模式 | `fresh`/`auto`/`manual`/`sleep` | `fa_work_mode fresh --device_name 新风机` |
| | `fa_wind_speed` | 设风速 | `auto`/`high`/`mid`/`low` | `fa_wind_speed mid --device_name 新风机` |
| | `fa_set_humidity` | 设湿度 | 湿度 (0-100%) | `fa_set_humidity 60 --device_name 新风机` |
| | `fa_clean_switch` | 开关UV 杀菌 | `on`/`off` | `fa_clean_switch on --device_name 新风机` |
| | `fa_fan_speed` | 设排风风速 | `auto`/`high`/`mid`/`low` | `fa_fan_speed mid --device_name 新风机` |
| **热泵** (5-004) | `hp_switch` | 开关 | `on`/`off` | `hp_switch on --device_name 热泵` |
| | `hp_set_temp` | 设温度 | 温度 (5-55℃) | `hp_set_temp 45 --device_name 热泵` |
| | `hp_mode` | 设模式 | `cold`/`hot` | `hp_mode hot --device_name 热泵` |
| **温控** (5-005) | `tc_switch` | 开关 | `on`/`off` | `tc_switch on --device_name 温控器` |
| | `tc_set_temp` | 设温度 | 温度 (5-35℃) | `tc_set_temp 26 --device_name 温控器` |
| | `tc_set_humidity` | 设湿度 | 湿度 (0-100%) | `tc_set_humidity 26 --device_name 温控器` |
| | `tc_mode` | 设模式 | `auto`/`cold`/`hot` | `tc_mode cold --device_name 温控器` |
| | `tc_wind_speed` | 设风速 | `auto`/`high`/`mid`/`low` | `tc_wind_speed auto --device_name 温控器` |
| | `tc_lock_mode` | 设锁定模式 | `mix`/`lock`/`mode_wind`/`floorheat` | `tc_lock_mode lock --device_name 温控器` |


**颜色 HSV 参考：** 红色=`0:100:100` | 绿色=`120:100:100` | 蓝色=`240:100:100` | 白色=`0:0:100` | 黄色=`60:100:100`<br>
**空调模式说明：** `auto` (自动)、`cold` (制冷)、`hot` (制热)、`fan` (送风)、`wet` (除湿)、`air` (换气)<br>
**空调风速说明：** `auto` (自动)、`super_strong` (超强)、`super_high` (超高)、`high` (高)、`mid` (中)、`low` (低)、`super_low` (超低)、`super_quiet` (超静)<br>
**空调风向说明：** `auto` (自动)、`stop` (停止)、`swing` (摇摆)、`up_down` (上下)、`left_right` (左右)<br>
**空调锁定模式说明：** `lock` (全锁)、`half_lock` (半锁)、`unlock` (解锁)<br>
**地暖锁定模式说明：** `lock` (全锁)、`half_lock` (半锁)、`unlock` (解锁)<br>
**新风风速和新风排风风速说明：** `auto` (自动)、`extreme_strong` (极强)、`super_high` (超高)、`high` (高)、`mid` (中)、`low` (低)、`super_low` (超低)、`super_quiet` (超静)<br>
**新风工作模式说明：** `fresh` (新风)、`wet` (除湿)、`auto` (自动)、`manual` (手动)、`indoor_loop` (内循环)、`sleep` (睡眠)、`pass` (旁通)、`common` (普通)、`smart` (智能)、`ventilate` (通风)、`outdoor_loop` (外循环)、`smart_auto` (智慧自动)、`eco_fresh` (节能新风)、`normal_air` (普通换气)、`cold_wet` (制冷除湿)、`hot_humidify` (制热加湿)、`cold_hot_auto` (冷暖自动)、`smart_humidify` (智慧调湿)、`timing` (定时)、`air` (换气)、`clean` (净化)、`program` (编程)、`exhaust` (排风)、`heat_exchange` (热交换)、`powerful` (强力)、`cold_room` (冷房)、`hot_room` (暖房)、`energy_recycle` (能量回收)、`night` (夜间)、`holiday` (假日)<br>
**热泵模式说明：** `cold` (制冷)、`hot` (制热)<br>
**温控模式说明：** `auto` (自动)、`cold` (制冷)、`hot` (制热)、`ventilate` (通风)、`floorheat` (地暖)、`mix` (一体)、`smart_floorheat` (智能地暖)、`cold_floorcold` (制冷制热)<br>
**温控风速说明：** `auto` (自动)、`super_strong` (超强)、`strong` (强劲)、`super_high` (超高)、`high` (高)、`mid` (中)、`low` (低)、`super_low` (超低)、`super_quiet` (超静)<br>
**温控锁定模式说明：** `mode` (锁定模式)、`mode_wind` (锁定模式&风速)、`mode_wind_temp` (锁定模式&风速&温度)、`unlock` (解锁)、`floorheat` (地暖)、`mix` (一体)、`lock` (锁定)<br>

### 场景控制
| 功能 | CLI 指令 |
|------|---------|
| 场景列表 | `python duwi_cli.py scenes [--room <房间>] [--floor <楼层>]` |
| 执行场景 | `python duwi_cli.py execute-scene --scene_no <编号>` 或 `--scene_name <名称>` |

### 统计数据
| 功能 | CLI 指令 |
|------|---------|
| 传感器统计 | `python duwi_cli.py sensor-stats <设备编号> --type <类型> --days <天数>` |
| 电量统计 | `python duwi_cli.py elec-stats [--device_no <编号>] --days <天数>` |

**传感器类型：** 1=温度，2=湿度，3=光照度，4=甲醛，5=PM2.5，6=CO2，7=AQI，8=人体感应 <br>

### 缓存管理
| 功能 | CLI 指令 |
|------|---------|
| 缓存统计 | `python duwi_cli.py cache stats` |
| 清理缓存 | `python duwi_cli.py cache clean` |
| 清空缓存 | `python duwi_cli.py cache clear` |

---

## 大模型集成指南

### 意图识别 → CLI 命令映射

| 用户说法 | 识别要素 | 生成的 CLI 命令 |
|---------|---------|----------------|
| "打开客厅的灯" | 房间=客厅，设备=灯，动作=开 | `python duwi_cli.py device-operate switch on --room 客厅 --device_name 灯` |
| "关闭一楼卧室的空调" | 楼层=一楼，房间=卧室，设备=空调 | `python duwi_cli.py device-operate ac_switch off --floor 一楼 --room 卧室 --device_name 空调` |
| "把主卧窗帘开到 50%" | 房间=主卧，设备=窗帘，值=50 | `python duwi_cli.py device-operate control_percent 50 --room 主卧 --device_name 窗帘` |
| "客厅空调 26 度制冷" | 房间=客厅，温度=26，模式=制冷 | `python duwi_cli.py device-operate ac_set_temp 26 --room 客厅 --device_name 空调` |
| "把灯调成红色" | 设备=灯，颜色=红色 | `python duwi_cli.py device-operate color 0:100:100 --device_name 灯` |

---

## 房屋结构

```
房屋 → 楼层 → 房间 → 设备/场景
```

```
房屋 (House)
├── 一楼 (Floor)
│   ├── 客厅 (Room)
│   │   ├── 顶灯 (Device)
│   │   ├── 会客模式 (Scene)
│   │   └── 客厅群组 (Group)
│   └── 厨房 (Room)
└── 二楼 (Floor)
    └── 次卧 (Room)
```

| 层级 | 说明 | 示例 |
|------|------|------|
| 房屋 | 最高层级 | 北京的家 |
| 楼层 | 房屋的楼层 | 一楼、二楼 |
| 房间 | 楼层下的房间 | 客厅、卧室 |
| 设备 | 智能设备 | 灯、窗帘、空调 |
| 场景 | 预设场景 | 会客模式、睡眠模式 |

---

## 注意事项

1. **Token 管理：** 登录后自动缓存，过期自动刷新
2. **房屋选择：** 首次使用需选择房屋，配置保存到 `config.json`
3. **设备在线：** 控制前请确认设备在线
4. **参数范围：** 亮度 0-100%，色温 2700-6200K，空调温度 5-35℃，地暖温度 10-30℃
5. **缓存刷新：** 设备控制后自动刷新缓存，如需手动刷新执行 `cache clear`
6. **安全：** 配置文件仅本地保存，不要分享或提交到 Git
7. **控制反馈**：如果控制失败，请反馈给用户相关控制失败原因
8. **设备缓存**：设备列表会自动缓存 5 分钟，如需刷新请等待或调用 `cache clear`
9. **用户反馈处理**：如果提出设备状态和实际设备状态不一致，请及时调用 `cache clear`

---

## 错误码

| 返回码 | 说明 |
|-------|------|
| 10000 | 操作成功 |
| 10001 | 请求参数不正确 |
| 10002 | accessToken 异常或过期 |
| 10003 | 暂无访问权限 |
| 11000 | 账户名或者密码错误 |
| 99001 | appKey 异常 |
| 99002 | 签名错误 |
| 99003 | 时间戳请求超时 |
| 19999 | 系统错误 |

---

## 依赖

```bash
pip install requests
```
