---
name: garmin-connect
version: 1.0.0
description: "Garmin Connect integration for OpenClaw: sync fitness data (steps, HR, calories, workouts, sleep) using OAuth. Supports China (garmin.cn) and Global (garmin.com) regions. Data is stored in SQLite database for fast access."
---

# Garmin Connect Skill

同步你的佳明手表数据到 OpenClaw，支持中国大陆和全球账号。

## 🎯 新架构（2026-03-13更新）

**核心变化：**

- ✅ 单一SQLite数据库存储所有数据
- ✅ 三种同步触发方式（定时/按需/手动）
- ✅ 龙虾直接读取数据库（快速响应）
- ✅ 完整数据支持（Body Battery、HRV、VO2 Max等）
- ✅ 数据库字段从26个扩展到58个（2026-03-13下午重大升级）
- ✅ 时序数据表支持（心率曲线、身体电量曲线等）

```
佳明服务器 → 统一同步脚本 → SQLite数据库
                              ├─ 龙虾skill（读取）
                              └─ 网页前端（读取）
```

## 🚀 2026-03-13 重大升级

### 问题发现
用户发现身体电量显示不一致（服务器79 vs 手表28），发现数据库同步不完整。

### 解决方案

**1. 数据库Schema升级**
- 新增35个字段：时长类、压力详细值、呼吸/血氧详细值、wellness字段等
- 修复关键字段：`body_battery_current`从存最高值改为存最新值
- 创建5个时序数据表：心率、身体电量、步数、压力、呼吸率曲线
- 创建1个动态反馈事件表
- 运动记录新增15个高级指标字段

**2. 同步策略优化**
- **完整版（sync_all.py v2.0）**：包含所有字段和时序数据，适合手动完整同步
- **简化版（sync_daily.py）**：只同步核心每日指标，适合定时任务

**3. 数据完整度提升**
- 标量字段：26% → 95%+
- 核心指标：100%完整
- 时序数据：表已创建，待后台同步

### 关键Bug修复
```python
# 旧逻辑（错误）
body_battery_current = bodyBatteryHighestValue  # 79

# 新逻辑（正确）
body_battery_current = bodyBatteryMostRecentValue  # 29
```

## 快速开始

### 1. 认证（一次性）

**中国大陆账号：**

```bash
cd ~/openclaw/skills/garmin-connect
python3 scripts/garmin-auth.py your-email@qq.com password --cn
```

**全球账号：**

```bash
python3 scripts/garmin-auth.py your-email@gmail.com password
```

认证成功后，凭证会加密保存到 `~/.garth/session.json`。

### 2. 启动自动同步

**systemd timer（推荐）：**

```bash
# 已自动配置，每1小时同步一次
sudo systemctl status garmin-sync.timer
```

**手动触发：**

```bash
python3 ~/.clawdbot/garmin/sync_all.py --source=manual
```

### 3. 测试数据读取

**从数据库读取（快速）：**

```bash
python3 scripts/garmin_db_reader.py
```

**从API读取（慢速，用于测试）：**

```bash
python3 scripts/garmin-sync.py
```

## 📊 数据结构

### 数据库位置

```
/home/roots/.clawdbot/garmin/data.db
```

### 包含的数据

**每日健康指标 (daily_metrics)：**

- 基础：步数、距离、卡路里、活动时长、爬楼
- 心率：静息/最低/最高
- 身体电量：当前/最高/最低/充电/消耗
- 压力：平均/最高
- HRV：昨晚HRV
- 呼吸率
- VO2 Max
- 健身年龄

**睡眠数据 (sleep_data)：**

- 时长、睡眠分数、质量百分比
- 深/REM/浅睡、清醒时间
- 午睡详情

**运动记录 (workouts)：**

- 时间戳、类型、名称、距离、时长、卡路里、心率

## 🔄 同步触发方式

### 1. 系统定时（自动）

每1小时自动同步一次（systemd timer）：

```bash
sudo systemctl start garmin-sync.timer
sudo systemctl enable garmin-sync.timer
```

查看下次同步时间：

```bash
systemctl list-timers | grep garmin
```

### 2. 龙虾按需触发

当你问"我刚才跑的咋样？"时：

```python
from scripts.garmin_db_reader import trigger_sync_if_needed

# 如果数据超过5分钟，自动触发同步
trigger_sync_if_needed(max_age_minutes=5)
```

然后读取数据库回答。

### 3. 手动触发

```bash
# 从命令行
python3 ~/.clawdbot/garmin/sync_all.py --source=manual

# 从网页（前端API）
POST /api/sync
```

## 📝 使用示例

### 在OpenClaw中使用

**方式1：从数据库读取（推荐）**

```python
import sys
sys.path.insert(0, '~/openclaw/skills/garmin-connect/scripts')
from garmin_db_reader import GarminDataReader, trigger_sync_if_needed

# 检查数据新鲜度，必要时触发同步
trigger_sync_if_needed(max_age_minutes=5)

# 读取数据
reader = GarminDataReader()
today = reader.get_today_metrics()
print(f"今日步数: {today['steps']}")
print(f"身体电量: {today['body_battery_current']}")
```

**方式2：直接API调用（兼容旧代码）**

```python
from garmin_db_reader import get_daily_summary, get_workouts
# garmin_client 参数会被忽略，直接读数据库
data = get_daily_summary(None, '2026-03-13')
```

### 查看同步状态

```python
reader = GarminDataReader()
status = reader.get_sync_status()
print(f"最后同步: {status['last_sync_time']}")
print(f"每日记录: {status['daily_metrics_count']} 条")
print(f"运动记录: {status['workouts_count']} 条")
```

## 🔧 故障排除

### 数据库不存在

```bash
# 手动运行一次同步
python3 ~/.clawdbot/garmin/sync_all.py --source=manual
```

### 同步失败

检查凭证：

```bash
cat ~/.garth/session.json
```

重新认证：

```bash
cd ~/openclaw/skills/garmin-connect
python3 scripts/garmin-auth.py your-email password
```

### 查看同步日志

```bash
# systemd日志
sudo journalctl -u garmin-sync.service -f

# 数据库同步日志
sqlite3 ~/.clawdbot/garmin/data.db "SELECT * FROM sync_log ORDER BY sync_time DESC LIMIT 10"
```

## 📁 文件结构

```
~/.clawdbot/garmin/
├── data.db                    # SQLite数据库
├── sync_daemon.py             # 数据库管理
└── sync_all.py                # 完整同步脚本

~/openclaw/skills/garmin-connect/
├── scripts/
│   ├── garmin_db_reader.py    # 数据库读取（新增）
│   ├── garmin-auth.py         # 认证
│   ├── garmin-sync.py         # API获取（兼容）
│   └── ...
└── SKILL.md                   # 本文件
```

## 🆕 vs 旧版本

| 特性       | 旧版本        | 新版本                   |
| ---------- | ------------- | ------------------------ |
| 数据存储   | 无            | SQLite数据库             |
| 响应速度   | API调用（慢） | 数据库读取（快）         |
| 同步触发   | cron（5分钟） | timer（1小时）+ 按需     |
| 数据完整性 | 基础指标      | 完整（含Body Battery等） |
| 消费者     | 仅skill       | skill + 网页前端         |

## 🔗 相关项目

- 佳明健康仪表盘：`/home/roots/garmin-dashboard/`
- 数据库：`~/.clawdbot/garmin/data.db`
