---
name: focus-master
description: ""
version: "1.0.0"
---


- 🍅 **番茄钟计时器**: 可配置专注/休息时间
- ⏱️ **任务时间记录**: 追踪每个任务的实际用时
- 📊 **时间分配分析**: 分类统计、趋势分析
- 🔒 **专注模式**: 屏蔽干扰，提高效率
- 📈 **效率报告生成**: 日/周/月报告

## 安装

```bash
# 添加到 PATH
ln -s ~/.openclaw/workspace/skills/focus-master/time-management ~/.local/bin/time-management
```

## 使用

### 番茄钟

```bash
# 开始25分钟番茄钟
time-management pomodoro --task "写代码"

# 自定义时长
time-management pomodoro --task "阅读" --duration 45

# 指定分类
time-management pomodoro --task "学英语" --category study
```

### 任务计时

```bash
# 开始任务计时
time-management task-start "项目开发" --category work

# 结束当前任务
time-management task-stop

# 查看任务记录
time-management tasks --limit 20
```

### 统计与报告

```bash
# 查看番茄钟统计
time-management stats

# 生成日报
time-management report

# 指定日期报告
time-management report --date 2024-01-15
```

### 专注模式

```bash
# 开启专注模式（默认25分钟）
time-management focus

# 自定义时长
time-management focus --duration 60
```

### 配置

```bash
# 查看配置
time-management config show

# 修改配置
time-management config set pomodoro_duration 30
```

## 配置项

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| pomodoro_duration | 25 | 番茄钟时长(分钟) |
| short_break | 5 | 短休息时长(分钟) |
| long_break | 15 | 长休息时长(分钟) |
| notification_enabled | true | 启用系统通知 |

## 数据存储

数据存储在 `~/.openclaw/data/time-management/`:
- `time_management.db` - SQLite 数据库
- `config.json` - 用户配置

## 技术栈

- Python 3.8+
- SQLite
- argparse
