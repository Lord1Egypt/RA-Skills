# claw-self-evolution - 完整自我进化闭环技能

## 🎯 功能描述

完整的**安全可控自我进化闭环**，让AI智能体持续改进，同时保证不会改崩系统：

> 设计原则：**自动发现 → 自动记录 → 隔离实验 → 人工审批 → 合并改进 → 持续进化**
> 
> 绝对不直接修改生产环境，必须人工批准才会合并，安全可控！

## 🧠 核心能力

| 模块 | 功能 |
|------|------|
| 📝 **学习记录** | 分类记录错误、教训、功能需求 |
| 🧹 **每日自检** | 自动检查规范一致性、安全基线、密钥扫描 |
| 🚀 **每周架构扫描** | 自动扫描发现大文件、冗余文件、优化点 |
| 🧠 **每周自省反思** | 自动总结一周工作，提取改进点 |
| 🧪 **安全实验闭环** | 隔离实验环境，必须审批才合并，绝对不会改崩 |
| 👤 **自动用户画像** | 每天自动学习用户偏好，越来越懂用户 |
| 💓 **服务健康监控** | 每15分钟检查服务状态，异常自动恢复 |
| 💾 **自动核心备份** | 每天备份核心配置，保留30天，随时可恢复 |
| 🧹 **自动日志清理** | 每天清理30天前日志，节省空间 |
| 🔍 **目录结构验证** | 自动验证OpenClaw目录规范，清理错位文件 |

## 🔐 安全设计

| 安全原则 | 说明 |
|---------|------|
| 隔离实验 | 所有改进先在 `memory/experiments/` 隔离测试，不碰生产 |
| 必须审批 | 任何合并必须**用户明确批准**才会生效 |
| 自动备份 | 合并前自动备份原文件，随时可以回滚 |
| 核心二次确认 | 修改核心配置 (`jobs.json`/`config.json`/`MEMORY.md`) 需要二次手动确认 |
| 不批准自动删除 | 不批准自动删除实验，干干净净 |
| 最小权限 | 只操作工作区内文件，不碰系统目录 |

## 📋 完整工作流

```
1. 📝 记录学习
   - 操作失败 → 记录 ERRORS.md
   - 用户纠正 → 记录 LEARNINGS.md
   - 新需求 → 记录 FEATURE_REQUESTS.md

2. 🧹 每日自动自检（每天凌晨 UTC+8）
   - 检查目录规范
   - 检查安全基线
   - 检查密钥泄露
   - 汇总学习记录

3. 🧠 每周自省反思（每周日凌晨 UTC+8）
   - 分析一周修改
   - 从学习记录提取改进点
   - 生成自省报告推送给用户
   - 找出需要改进的地方

4. 🧪 创建安全实验
   - 用户同意后创建隔离实验
   - 在实验中修改测试，不影响生产

5. 👀 用户审批
   - 生成实验报告，列出所有修改
   - 用户批准 → 备份原文件 → 合并到生产
   - 用户不批准 → 自动删除实验

6. ✅ 持续进化
   - 改进完成，下周再找新改进
   - 每天进步一点点
```

## 🚀 安装

```bash
# 在OpenClaw环境中
./install.sh
```

安装脚本会自动：
1. 创建所有必要目录
2. 复制所有脚本到 `scripts/system/maintenance/`
3. 创建初始学习记录文件 `memory/learnings/`
4. 设置正确执行权限

安装完成后，你需要手动：
1. 添加定时任务到 `jobs.json`（按照README说明）
2. 确认权限正确

## ⚙️ 定时任务配置（UTC时间）

添加这些到你的 `jobs.json`：

```json
// 每日自我进化自检（北京时间 00:15 → UTC 16:15）
{
  "schedule": { "cron": "15 16 * * *", "timezone": "UTC", "type": "cron" },
  "task_type": "shell",
  "text": "python3 /app/working/scripts/system/maintenance/daily-self-check.py",
  "dispatch": { "mode": "failure-only" }
}

// 每日核心配置备份（北京时间 01:15 → UTC 17:15）
{
  "schedule": { "cron": "0 16 * * *", "timezone": "UTC", "type": "cron" },
  "task_type": "shell",
  "text": "python3 /app/working/scripts/system/maintenance/core-backup.py",
  "dispatch": { "mode": "silent" }
}

// 每日日志清理（北京时间 01:00 → UTC 17:00）
{
  "schedule": { "cron": "0 16 * * *", "timezone": "UTC", "type": "cron" },
  "task_type": "shell",
  "text": "python3 /app/working/scripts/system/maintenance/log-cleanup.py",
  "dispatch": { "mode": "silent" }
}

// 每日自动更新用户画像（北京时间 01:30 → UTC 17:30）
{
  "schedule": { "cron": "30 16 * * *", "timezone": "UTC", "type": "cron" },
  "task_type": "shell",
  "text": "python3 /app/working/scripts/system/maintenance/auto-update-user-profile.py",
  "dispatch": { "mode": "silent" }
}

// 每周架构优化扫描（北京时间 周日 00:00 → UTC 周六 16:00）
{
  "schedule": { "cron": "0 16 * * 0", "timezone": "UTC", "type": "cron" },
  "task_type": "shell",
  "text": "python3 /app/working/scripts/system/maintenance/weekly-architecture-scan.py",
  "dispatch": { "mode": "failure-only" }
}

// 每周自省反思（北京时间 周日 00:30 → UTC 周六 16:30）
{
  "schedule": { "cron": "0 16 * * 0", "timezone": "UTC", "type": "cron" },
  "task_type": "shell",
  "text": "python3 /app/working/scripts/system/maintenance/weekly-introspection.py",
  "dispatch": { "mode": "always" }
}

// 服务健康检查（每15分钟）
{
  "schedule": { "cron": "*/15 * * * *", "timezone": "UTC", "type": "cron" },
  "task_type": "shell",
  "text": "python3 /app/working/scripts/system/maintenance/service-health-check.py",
  "dispatch": { "mode": "failure-only" }
}

// 每日目录结构验证（北京时间 02:00 → UTC 18:00）
{
  "schedule": { "cron": "0 18 * * *", "timezone": "UTC", "type": "cron" },
  "task_type": "shell",
  "text": "python3 /app/working/scripts/system/maintenance/verify_directory_structure.py",
  "dispatch": { "mode": "silent" }
}
```

## 📦 包内文件

```
claw-self-evolution/
├── SKILL.md              # 本文件
├── _meta.json            # ClawHub元数据
├── install.sh            # 安装脚本
├── .clawhub/config.json  # ClawHub配置
└── files/               # 所有脚本文件
    ├── daily-self-check.py
    ├── weekly-architecture-scan.py
    ├── weekly-introspection.py
    ├── safe-experiment.py
    ├── auto-update-user-profile.py
    ├── service-health-check.py
    ├── core-backup.py
    ├── log-cleanup.py
    └── verify_directory_structure.py
```

## 🔑 权限声明

这个skill需要：
- **读/写权限**：`/app/working/scripts/`、`/app/working/memory/`、`/app/working/logs/`
- 目的：存放脚本、学习记录、日志、备份
- **不会**读写系统目录、不会获取系统权限
- **所有文件操作**都限定在OpenClaw工作区内

## 📝 版本历史

- v1.0.0 (2026-03-18)
  - 完整闭环整合完成
  - 安全实验设计
  - 吸收 self-improving-agent 学习记录思路
  - 保持安全可控，必须审批才合并
  - 完整打包，符合ClawHub规范

## 👤 作者

- **Author**: kenz1117
- **License**: MIT-0

## 🔗 参考

- 灵感来源于 [self-improving-agent](https://github.com/pskoett/self-improving-agent)
- 安全实验闭环设计为 OpenClaw 量身定制
- 配合 `claw-security-suite` 使用，安全+进化，完美组合
