---
name: fboxcli
description: >
  通过 FBox CLI 命令行管理工业物联网设备。
  查看设备列表和详情，读写 PLC 监控点数据，管理报警和联系人，查询历史数据，管理设备分组和统一写组。
  当用户提到 fboxcli、FBox 命令行、CLI 脚本、自动化运维、批量操作设备时使用此技能。
compatibility: >
  Requires fboxcli binary installed and available in PATH.
  Requires FBox platform credentials (developer client_id/secret or user account).
metadata:
  version: "0.1.0"
  author: flexem
  homepage: https://fbox360.com
  openclaw:
    os:
      - darwin
      - linux
      - win32
---

# FBox CLI 技能

通过 `fboxcli` 命令行工具管理 FBox 工业物联网设备。安装和配置详见 [README.md](README.md)。

## 核心规则

### JSON 输出
- **始终使用 `--json` 全局标志**，确保输出为结构化 JSON，便于解析
- 不带 `--json` 时输出人类可读表格，仅在用户明确要求表格展示时省略 `--json`

### 认证前置
- 执行业务命令前，先通过 `fboxcli auth token --json` 检查是否已登录
- 如果未登录或 Token 过期，提示用户执行 `fboxcli auth login` 登录
- **禁止在命令中自动填入用户名、密码或密钥**，由用户自行输入

### ID 获取流程
- 大部分命令需要 `BOX_ID`（数字 ID），**不是** `BOX_NO`（序列号）
- 必须先通过 `fboxcli box list --json` 获取设备列表，从返回的 JSON 中提取 `id` 字段
- **禁止猜测或编造 ID**，所有 ID 必须来自实际命令返回

### 写操作安全
- 以下命令为写操作，**必须获得用户明确确认后才能执行**：
  - `dmon set-value` — 写入监控点值
  - `control write` — 向统一写组写入值
  - `alarm confirm` — 确认报警
- 以下命令为删除操作，**必须获得用户明确确认后才能执行**：
  - `box delete` — 删除设备
  - `group delete` — 删除分组
  - `dmon delete` — 删除监控点
  - `history delete` — 删除历史记录条目
  - `alarm delete` / `alarm delete-group` — 删除报警条目/分组
  - `contact delete` — 删除联系人
  - `control delete` — 删除统一写组
- 写入前先读取当前值展示给用户对比

### 时间处理
- 历史数据和报警历史查询的 `--begin` 和 `--end` 参数为**毫秒级 Unix 时间戳**
- 展示给用户时转为北京时间（UTC+8），仅精确到秒
- 可通过 `date +%s000` 等方式计算时间戳，或让用户提供

### 数据展示
- `bool` 值展示为"是"或"否"
- 历史数据和报警记录默认以**表格形式**展示
- 展示列表数据时提取关键字段，避免原始 JSON 直接输出

## 典型工作流

### 设备状态查看
```
fboxcli auth token --json → 确认已登录
fboxcli box list --json → 获取设备列表和 ID
fboxcli box get <BOX_NO> --json → 按序列号查设备
fboxcli box info <BOX_ID> --json → 查看设备详细配置
```

### 监控点读写
```
fboxcli box list --json → 获取 BOX_ID
fboxcli dmon list <BOX_ID> --json → 列出监控点和 ID
fboxcli dmon get-value <BOX_ID> --ids 1001,1002 --json → 读取实时值
  → 用户确认后
fboxcli dmon set-value <BOX_ID> --id 1001 --value 100 → 写入值
```

### 报警处理
```
fboxcli alarm list <BOX_ID> --json → 查看报警条目
fboxcli alarm history <BOX_ID> --begin <TS> --end <TS> --json → 报警历史
  → 用户确认后
fboxcli alarm confirm <UID> → 确认报警
```

### 历史数据查询
```
fboxcli history list <BOX_ID> --json → 查看历史记录条目和通道 ID
fboxcli history query --ids <CHANNEL_IDS> --begin <TS> --end <TS> --json
  → 以表格形式展示，时间转北京时间
```

### 联系人与报警分组管理
```
fboxcli contact list --json → 查看联系人列表
fboxcli contact add "张三" --phone 13800138000 --notice-type 1 → 添加联系人
fboxcli alarm groups <BOX_ID> --json → 查看报警分组
fboxcli alarm add-group <BOX_ID> "紧急报警" --contacts <UIDS> → 添加报警分组
```
