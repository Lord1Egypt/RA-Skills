---
name: config-monitor
version: 1.0.0
description: OpenClaw 配置监控 - 实时监控 Gateway 状态、配置变更、备份健康度。Triggers: "监控配置"、"配置报告"、"Gateway 状态"、"配置健康"。
---

# Config Monitor - OpenClaw 配置监控

**创建时间**: 2026-04-22  
**背景**: 防止配置崩溃，建立主动监控机制  
**定位**: 配置安全体系的"眼睛"，实时掌握系统健康状态

---

## 🎯 核心能力

| 能力 | 说明 | 触发词 | 脚本 |
|------|------|--------|------|
| **Gateway 监控** | 实时监控 Gateway 运行状态 | "Gateway 状态" | config-monitor.sh |
| **变更监控** | 跟踪配置变更频率，防止频繁修改 | "变更频率" | config-monitor.sh |
| **备份监控** | 检查备份数量和健康度 | "备份状态" | config-monitor.sh |
| **技能监控** | 检查配置相关技能是否安装 | "技能状态" | config-monitor.sh |
| **日志监控** | 统计日志错误数，发现潜在问题 | "日志错误" | config-monitor.sh |
| **生成报告** | 输出完整配置健康报告 | "配置报告" | config-monitor.sh report |

---

## 📊 监控指标

### Gateway 状态监控

| 状态 | 说明 | 处理 |
|------|------|------|
| ✅ running | 正常运行 | 无需操作 |
| ⚠️ restarting | 重启中 | 等待完成 |
| 🚨 down | 已停止 | 立即恢复 |

### 配置变更频率

| 频率 | 状态 | 建议 |
|------|------|------|
| <5 次/天 | ✅ 正常 | 继续观察 |
| 5-10 次/天 | ⚠️ 注意 | 谨慎修改 |
| >10 次/天 | 🚨 过高 | 暂停修改，审查原因 |

### 备份健康度

| 备份数 | 状态 | 建议 |
|--------|------|------|
| ≥5 个 | ✅ 健康 | 保持 |
| 3-5 个 | ⚠️ 偏低 | 增加备份 |
| <3 个 | 🚨 危险 | 立即备份 |

### 日志错误数

| 错误数/天 | 状态 | 建议 |
|-----------|------|------|
| <10 | ✅ 正常 | 保持 |
| 10-100 | ⚠️ 注意 | 检查原因 |
| >100 | 🚨 异常 | 立即排查 |

---

## 🔧 使用方法

### 1. 查看配置状态报告

```bash
# 快速状态检查
~/.openclaw/workspace/scripts/config-monitor.sh status

# 详细监控报告
~/.openclaw/workspace/scripts/config-monitor.sh report
```

### 2. 实时监控 Gateway

```bash
# 每 60 秒检查一次 Gateway 状态
~/.openclaw/workspace/scripts/config-monitor.sh watch 60

# 每 30 秒检查一次（更密集）
~/.openclaw/workspace/scripts/config-monitor.sh watch 30

# 按 Ctrl+C 停止监控
```

### 3. 设置定时监控（推荐）

```bash
# 每天早上 9 点自动生成配置健康报告
openclaw cron add \
  --name "配置健康日报" \
  --cron "0 9 * * *" \
  --message "~/.openclaw/workspace/scripts/config-monitor.sh report" \
  --tz "Asia/Shanghai"

# 每小时检查一次 Gateway 状态
openclaw cron add \
  --name "Gateway 状态检查" \
  --cron "0 * * * *" \
  --message "openclaw gateway status" \
  --tz "Asia/Shanghai"
```

---

## 📋 监控报告内容

### 标准报告包含

```
======================================================================
  OpenClaw 配置监控报告
  时间：2026-04-22 13:44:12
======================================================================

✅ Gateway 状态：正常运行

✅ 配置变更频率：1 次/天（正常）
   本周总变更：1 次

✅ 备份健康度：12 个（健康）
   最新备份：2026-04-22 13:42
   备份文件：openclaw.json.backup.20260422_134245

✅ 配置技能状态：
   - config-safety: 已安装
   - config-optimizer: 已安装

📋 最近 5 次变更:
  1. [2026-04-22 13:42:45] [optimize] by 迪豆：建立配置安全防护体系

📊 今日日志错误数：6979
   ⚠️ 错误数过多，建议检查日志

======================================================================
```

---

## 🚨 告警处理流程

### Gateway 崩溃告警

```bash
# 1. 确认 Gateway 状态
openclaw gateway status

# 2. 查看最近日志
tail -100 /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log

# 3. 找到最近备份
ls -lt ~/.openclaw/backups/config/openclaw.json.* | head -3

# 4. 执行恢复
~/.openclaw/workspace/scripts/config-change-logger.sh rollback \
  ~/.openclaw/backups/config/openclaw.json.backup.<时间戳>

# 5. 重启 Gateway
openclaw gateway restart

# 6. 记录紧急恢复
~/.openclaw/workspace/scripts/config-change-logger.sh log \
  emergency "Gateway 崩溃紧急恢复" "系统"
```

### 变更频率过高告警

```bash
# 1. 查看变更历史
~/.openclaw/workspace/scripts/config-change-logger.sh history

# 2. 分析变更原因
# - 是否在进行大规模配置调整？
# - 是否在反复测试某个配置项？
# - 是否有自动化脚本在频繁修改？

# 3. 暂停变更，审查原因
# - 如果是测试，建议改为批量测试后一次性应用
# - 如果是自动化脚本，建议增加间隔时间
# - 如果是手动修改，建议先规划再执行

# 4. 记录审查结果
~/.openclaw/workspace/scripts/config-change-logger.sh log \
  fix "审查变更频率过高" "迪豆" "原因：xxx，措施：xxx"
```

### 备份不足告警

```bash
# 1. 立即备份当前配置
~/.openclaw/workspace/scripts/config-change-logger.sh log \
  modify "手动备份" "迪豆" "备份数量不足，手动增加"

# 2. 检查备份目录
ls -lh ~/.openclaw/backups/config/

# 3. 考虑清理过期备份（保留最近 10 个）
ls -t ~/.openclaw/backups/config/openclaw.json.* | tail -n +11 | xargs rm
```

---

## 📈 监控数据分析

### 每周分析（建议）

```bash
# 1. 统计本周变更次数
grep "$(date +%Y-%m)" ~/.openclaw/workspace/logs/config-changes.log | wc -l

# 2. 统计本周 Gateway 重启次数
grep -c "restart\|start" /tmp/openclaw/openclaw/openclaw-*.log

# 3. 分析最常见变更类型
cat ~/.openclaw/workspace/logs/config-changes.log | \
  awk -F'[][]' '{print $2}' | sort | uniq -c | sort -rn

# 4. 生成周报
# (可以扩展为自动脚本)
```

### 每月审查（建议）

| 审查项目 | 说明 |
|----------|------|
| 变更趋势 | 对比上月，变更次数增加/减少？ |
| 崩溃次数 | 本月是否发生 Gateway 崩溃？ |
| 备份策略 | 备份数量是否足够？是否需要调整？ |
| 技能使用 | config-safety 是否被正确使用？ |
| 日志错误 | 错误数是否有异常波动？ |

---

## 🔗 相关 Skills

- **config-safety** - 配置安全防护
- **config-optimizer** - Token 优化、性能调优
- **skill-monitor** - 技能使用监控
- **evolution-monitor** - 系统进化监控
- **healthcheck** - 系统健康检查

---

## 📚 监控最佳实践

### ✅ 推荐做法

1. **每日检查** - 每天早上查看配置状态
2. **变更前检查** - 每次修改前跑安全检查
3. **变更后验证** - 修改后确认 Gateway 正常
4. **定期报告** - 每周/每月生成监控报告
5. **告警响应** - 收到告警立即处理

### ❌ 避免做法

1. **不监控直接修改** - 盲目修改配置
2. **忽略告警** - 看到告警不处理
3. **不记录变更** - 修改不留痕迹
4. **不检查备份** - 崩溃时发现备份不可用
5. **不分析数据** - 监控数据不用于改进

---

## 🎯 成功标准

- ✅ **实时感知** - Gateway 状态变化 1 分钟内发现
- ✅ **主动告警** - 异常情况主动通知用户
- ✅ **数据驱动** - 基于监控数据优化配置策略
- ✅ **零意外** - 没有"突然崩溃"的情况

---

**维护者**: 迪豆 🫘  
**最后更新**: 2026-04-22  
**版本**: 1.0.0  
**状态**: 已激活
