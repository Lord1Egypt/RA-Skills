<!-- License: MIT License (c) 2024 perrykono-debug -->

# SKILL.md

**License:** MIT  
**Copyright:** 2026 perrykono-debug

---

---
name: computer-efficiency-skill
description: |
  电脑运行效率助手核心技能 - 跨平台系统状态监控与安全优化。
  支持 macOS/Windows/Linux，提供系统诊断、性能评估、智能清理、内存优化、定时巡检。
---

# Computer Efficiency Skill

## 跨平台支持

自动检测系统类型（macOS/Windows/Linux），执行对应平台命令。

### 平台检测
```bash
uname -s  # Darwin/macOS, Linux, MINGW/Windows
```

### 命令对照

| 功能 | macOS | Windows (PowerShell) | Linux |
|------|-------|---------------------|-------|
| CPU | `top -l 1` | `Get-Counter` | `top -bn1` |
| 内存 | `vm_stat` | `Get-WmiObject Win32_OperatingSystem` | `free -m` |
| 磁盘 | `df -h` | `Get-WmiObject Win32_LogicalDisk` | `df -h` |
| 电池 | `pmset -g batt` | `Get-WmiObject Win32_Battery` | `/sys/class/power_supply/` |
| 进程 | `ps aux` | `Get-Process` | `ps aux` |

---

## 核心能力

### 1. 系统诊断

#### macOS
```bash
top -l 1 -n 1 | grep "CPU usage"
vm_stat
df -h
pmset -g batt
```

#### Windows
```powershell
Get-Counter '\Processor(_Total)\\% Processor Time'
$os = Get-WmiObject Win32_OperatingSystem
Get-WmiObject Win32_LogicalDisk
Get-WmiObject Win32_Battery
```

#### Linux
```bash
top -bn1 | grep "Cpu(s)"
free -m
df -h
cat /sys/class/power_supply/BAT0/capacity
```

### 2. 性能评估（100分制）

| 指标 | 权重 | 评分标准 |
|------|------|---------|
| CPU 负载 | 20% | <3:20, <5:15, <8:10, >8:5 |
| 内存空闲 | 25% | >70%:25, >50%:20, >30%:15, <30%:10 |
| 磁盘空间 | 20% | <50%:20, <70%:15, <85%:10, >85%:5 |
| 电池状态 | 15% | >50%:15, >20%:10, <20%:5 |
| 系统温度 | 10% | <70°C:10, <80°C:7, <90°C:5, >90°C:3 |
| 进程健康 | 10% | 正常:10, 异常:5 |

评级：90-100🟢 70-89🟡 50-69🟠 <50🔴

### 3. 智能清理

**⚠️ 必须用户确认后方可执行**

#### 清理流程
1. 扫描识别可清理项
2. 报告（项目+空间+风险等级）
3. 获得明确"确认"/"执行"
4. 备份→执行→报告

#### 清理路径

| 项目 | macOS | Windows | Linux | 风险 |
|------|-------|---------|-------|:--:|
| 应用缓存 | `~/Library/Caches/` | `%LOCALAPPDATA%\Temp\` | `~/.cache/` | 🟢 |
| 系统日志 | `~/Library/Logs/` | `%PROGRAMDATA%\Logs\` | `/var/log/` | 🟢 |
| 临时文件 | `/tmp/` | `%TEMP%\` | `/tmp/` | 🟡 |
| 浏览器历史 | - | - | - | 🔴 不清理 |
| 系统缓存 | `/System/Library/Caches/` | `C:\Windows\Temp\` | `/var/cache/` | 🔴 不清理 |

#### 确认话术
```
🧹 扫描完成，发现以下可清理项目：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. QClaw 更新缓存          1.1GB  🟢 安全
2. 系统日志(7天+)            50MB  🟢 安全
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💾 预估可释放空间: 1.15GB
📦 将自动备份到: ~/.trash/backup_YYYYMMDD/

⚠️ 请确认是否执行清理？
回复 "确认" 或 "执行" 开始清理
回复 "取消" 放弃清理
```

### 4. 内存优化

**⚠️ 终止进程前必须确认**

#### 查看内存大户

**macOS/Linux:**
```bash
ps aux | sort -nrk 6 | head -10
```

**Windows:**
```powershell
Get-Process | Sort-Object WorkingSet -Descending | Select -First 10
```

#### 话术
```
🧠 内存占用 TOP 5：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. WeChat          1,747 MB  📱 用户应用
2. Chrome            980 MB  📱 用户应用
3. WindowServer      433 MB  ⚙️ 系统进程（不可终止）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 优化建议：
• WeChat 占用较高，建议重启可释放 ~1GB
⚠️ 是否需要终止某个应用？
回复应用名称（如"终止 WeChat"）
回复"取消"不执行
```

### 5. 定时巡检

```json
{
  "daily_check": { "schedule": "0 9 * * *", "content": "系统健康简报" },
  "weekly_check": { "schedule": "0 9 * * 1", "content": "详细优化建议" }
}
```

告警阈值：CPU>80%, 内存>90%, 磁盘<10%, 电池<20%

---

## 安全规则

### 核心原则：用户确认制

**任何影响系统的操作，必须获得明确确认后方可执行。**

✅ **有效确认**："确认"、"执行"、"同意"、"是的，执行清理"
❌ **无效确认**："好"、"行"、"OK" 等模糊回复需再次询问

### 禁止自动执行
- 删除任何文件
- 终止任何进程
- 修改系统配置
- 清空废纸篓

### 可自动执行（只读类）
- 扫描系统状态
- 生成诊断报告
- 列出清单
- 给出建议

---

## 输出格式

### 系统健康报告
```
📊 系统健康报告 [评分: 85/100 良好]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🖥️ CPU
   负载: 3.5 (良好)
   使用率: 15% 用户 / 18% 系统 / 67% 空闲
🧠 内存
   已用: 11GB / 16GB (69%)
   空闲率: 72% (良好)
💾 磁盘
   已用: 199GB / 926GB (23%)
   状态: 优秀
🔋 电池
   电量: 35%
   状态: ⚠️ 建议充电
🎯 优化建议
1. WindowServer CPU 偏高，建议重启
2. 可清理缓存释放 1.2GB
```

### 清理报告
```
✅ 清理完成
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
已清理项目:
  • QClaw 缓存: 1.1GB
  • 系统日志: 50MB
总计释放: 1.15GB
备份位置: ~/.trash/backup_20260606/
```

---

## 依赖

- `qclaw-text-file` — 生成报告文件
- `qclaw-cron-skill` — 定时任务

---

*版本: v1.0.0 | 创建时间: 2026-06-06*
