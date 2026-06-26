# Garmin Connect Skill for OpenClaw

**Author: SQ** | 支持佳明中国 (garmin.cn) 和国际版 (garmin.com)

---

## ✨ 功能特性

- 🔐 OAuth 认证，支持中国/国际两套账号体系
- 📊 数据同步：步数、心率、睡眠、卡路里、运动记录、身体电量、HRV、压力、VO2 Max
- 💾 SQLite 本地存储，支持完整历史查询
- ⚡ 按需同步，自动检测缺失天数并补全
- 📱 支持飞书/OpenClaw/微信推送

---

## 📁 目录结构

```
scripts/
├── garmin-auth.py              # OAuth 认证（支持 garmin.cn）
├── garmin-sync.py              # API 原始数据同步
├── sync_all.py                 # SQLite 全量同步（自动检测缺失天数）⭐
├── sync_daemon.py              # 后台守护进程（每30分钟自动同步）
├── garmin_db_reader.py         # 数据库读取（推荐方式）
├── garmin_status.py            # 同步状态查看
├── daily_health_report*.py     # 健康报告（多个版本）
├── init_db.py                  # 数据库初始化（完整字段）
└── requirements.txt
```

---

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 认证（仅需一次）

```bash
# 佳明中国
python3 scripts/garmin-auth.py XXXX YOUR_PASSWORD --cn

# 佳明国际
python3 scripts/garmin-auth.py your@email.com YOUR_PASSWORD
```

### 3. 同步数据

```bash
# 自动检测缺失天数并补全（推荐）
python3 scripts/sync_all.py

# 指定同步最近7天
python3 scripts/sync_all.py --days 7
```

### 4. 查询数据

```bash
python3 scripts/garmin_db_reader.py
```

---

## 🗄️ 数据库 Schema

### daily_metrics（每日指标）

| 字段 | 说明 |
|------|------|
| steps | 步数 |
| calories | 卡路里 |
| active_seconds | 活跃秒数 |
| floors | 楼层 |
| resting_heart_rate | 静息心率 |
| vo2_max | 最大摄氧量 |
| moderate_intensity_minutes | 中等强度分钟 |
| vigorous_intensity_minutes | 高强度分钟 |
| hrv_value | 心率变异 |
| body_battery_* | 身体电量 |

### sleep_data（睡眠数据）

| 字段 | 说明 |
|------|------|
| total_sleep_hours | 总睡眠时长 |
| deep_sleep_hours | 深睡眠 |
| rem_sleep_hours | REM睡眠 |
| nap_count | 午睡次数 |
| sleep_score | 睡眠分数 |

### workouts（运动记录）

活动类型、距离、时长、心率等完整记录。

### 时序数据表

心率曲线、身体电量曲线、步数曲线、压力曲线、呼吸率曲线。

---

## ⚙️ OpenClaw 集成

在 OpenClaw 中，你可以通过对话触发：

- "查一下最近的睡眠"
- "今天的步数是多少"
- "最近有什么运动记录"

---

## 📝 数据库位置

```
~/.clawdbot/garmin/data.db
~/.garth/session.json  # 认证凭证
```
