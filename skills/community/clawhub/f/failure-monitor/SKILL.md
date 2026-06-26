---
name: failure-monitor
version: 1.0.0
description: Automated failure detection, diagnosis, and auto-repair system for cron jobs. Monitors task health, fixes common issues automatically, and requests human confirmation when needed.
author: sunnyhot
license: MIT
keywords:
  - failure-detection
  - auto-repair
  - monitoring
  - cron-jobs
  - self-healing
  - diagnostics
---

# Failure Monitor - 自动故障监控修复系统

**智能守护你的定时任务系统**

---

## ✨ 核心功能

### 🔍 **自动检测失败**
- ✅ 监控所有 cron jobs 运行状态
- ✅ 实时检测任务失败（`lastStatus: error`）
- ✅ 提取错误信息和堆栈跟踪
- ✅ 统计连续失败次数

### 🧠 **智能诊断**
- ✅ **超时问题**：`cron: job execution timed out`
- ✅ **配置错误**：`Channel is required`, `unknown job id`
- ✅ **权限问题**：`Permission denied`, `Access denied`
- ✅ **API 错误**：`API key invalid`, `Rate limit exceeded`
- ✅ **网络错误**：`Network timeout`, `Connection refused`
- ✅ **脚本错误**：`Script not found`, `Syntax error`

### 🔧 **自动修复**
可自动修复的问题（无需人工确认）：
- ✅ **超时问题** → 增加 timeout（120s → 300s）
- ✅ **推送配置错误** → 更新 delivery 配置
- ✅ **文件权限** → 修复执行权限（`chmod +x`）
- ✅ **重复任务** → 删除重复的 cron job

需要人工确认的问题：
- ⚠️ **API Key 失效** → 需要更新 API Key
- ⚠️ **脚本逻辑错误** → 需要修复脚本代码
- ⚠️ **外部服务故障** → 需要等待服务恢复
- ⚠️ **重大配置变更** → 需要用户确认

### 📊 **通知和报告**
- ✅ **自动修复成功** → 推送修复报告
- ✅ **需要人工介入** → 推送确认请求（包含问题详情）
- ✅ **用户确认后** → 执行修复并推送结果
- ✅ **完整日志** → 记录所有诊断和修复操作

---

## 🚀 使用方法

### 1. **自动监控模式**（推荐）

将 `failure-monitor` 设置为定时任务，定期检查所有 cron jobs：

```bash
openclaw cron add \
  --name "failure-monitor" \
  --cron "*/30 * * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --wake now \
  --deliver \
  --message "运行 failure-monitor: 检查所有定时任务状态，自动修复可修复的问题，需要人工时推送确认请求。报告格式用中文。"
```

**运行频率**：
- 每 30 分钟检查一次
- 或每小时检查一次（`0 * * * *`）

---

### 2. **手动触发**

当收到失败通知时，手动运行诊断：

```bash
node /Users/xufan65/.openclaw/workspace/skills/failure-monitor/scripts/diagnose.cjs
```

---

### 3. **查看监控报告**

查看最近的监控和修复记录：

```bash
cat /Users/xufan65/.openclaw/workspace/memory/failure-monitor-log.json
```

---

## 📋 工作流程

```
┌─────────────────┐
│  Cron Job 失败  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  错误检测器     │
│  - 检查状态     │
│  - 提取错误     │
│  - 统计次数     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  智能诊断器     │
│  - 分析错误类型 │
│  - 检查配置     │
│  - 生成方案     │
└────────┬────────┘
         │
         ▼
     能自动修复？
         │
    ┌────┴────┐
   Yes       No
    │          │
    ▼          ▼
┌───────┐  ┌──────────┐
│自动修复│  │推送确认  │
│- 执行  │  │- 详情    │
│- 记录  │  │- 等待    │
└───┬───┘  └────┬─────┘
    │           │
    ▼           ▼
┌─────────────────┐
│  推送报告       │
│  - 修复结果     │
│  - 需要操作     │
│  - 日志记录     │
└─────────────────┘
```

---

## 🔧 可自动修复的问题

| 错误类型 | 错误信息 | 修复方案 | 人工确认 |
|---------|---------|---------|---------|
| **超时** | `job execution timed out` | 增加 timeout（120s → 300s） | ❌ 否 |
| **推送配置** | `Channel is required` | 更新 delivery.channel | ❌ 否 |
| **权限** | `Permission denied` | `chmod +x script` | ❌ 否 |
| **重复任务** | 重复的 cron job | 删除重复的任务 | ❌ 否 |
| **API Key** | `API key invalid` | 需要更新 API Key | ✅ 是 |
| **脚本错误** | `Script not found` | 需要修复脚本 | ✅ 是 |
| **网络错误** | `Network timeout` | 需要检查网络 | ✅ 是 |

---

## 📊 配置文件

### `config/rules.json`

定义自动修复规则：

```json
{
  "autoFixRules": [
    {
      "errorPattern": "job execution timed out",
      "action": "increaseTimeout",
      "params": {
        "from": 120,
        "to": 300
      }
    },
    {
      "errorPattern": "Channel is required",
      "action": "updateDeliveryChannel",
      "params": {
        "channel": "discord"
      }
    }
  ],
  "notifyRules": {
    "autoFixSuccess": true,
    "needConfirmation": true,
    "cooldownMinutes": 60
  }
}
```

---

## 🔗 Discord 推送格式

### **自动修复成功**

```markdown
# ✅ 自动修复成功

**任务**: deals-noon
**问题**: 超时（120秒）
**修复**: 增加超时到 300 秒
**时间**: 2026-03-12 14:00:00

**详情**:
- 任务运行时间超过原超时设置
- 已自动将 timeout 从 120s 增加到 300s
- 下次运行应该正常
```

### **需要人工确认**

```markdown
# ⚠️ 需要人工介入

**任务**: content-research
**问题**: API Key 失效
**时间**: 2026-03-12 14:00:00

**错误详情**:
```
Error: TAVILY_API_KEY is invalid
Please update your API key
```

**建议操作**:
1. 检查 TAVILY_API_KEY 环境变量
2. 更新到有效的 API Key
3. 重启任务

**回复 "确认" 执行修复，或 "忽略" 跳过**
```

---

## 📁 文件结构

```
skills/failure-monitor/
├── SKILL.md                      # 技能说明
├── scripts/
│   ├── monitor.cjs               # 主监控脚本
│   ├── diagnose.cjs              # 诊断脚本
│   ├── auto-fix.cjs              # 自动修复脚本
│   └── notify.cjs                # 通知脚本
├── config/
│   └── rules.json                # 自动修复规则
└── package.json                  # 依赖管理
```

---

## 🎯 最佳实践

### 1. **运行频率**
- ✅ 推荐：每 30 分钟检查一次
- ✅ 可接受：每小时检查一次
- ❌ 不推荐：超过 2 小时（可能错过重要错误）

### 2. **通知设置**
- ✅ 启用 OpenClaw 内置 Failure Alert（立即通知）
- ✅ 启用 failure-monitor（自动修复）
- ✅ 两者配合使用效果最佳

### 3. **人工确认**
- ✅ 设置合理的冷却时间（避免重复通知）
- ✅ 明确说明需要的操作
- ✅ 提供详细的错误信息

---

## 🔐 安全考虑

- ✅ **权限限制**：只修复配置问题，不修改代码
- ✅ **人工确认**：重大操作需要用户确认
- ✅ **日志记录**：所有操作都有完整日志
- ✅ **回滚机制**：记录原始配置，支持回滚

---

## 📊 监控指标

- **总任务数**: 11 个
- **失败任务**: 实时统计
- **自动修复**: 成功次数
- **人工介入**: 需要确认的次数
- **平均恢复时间**: 从失败到修复的时间

---

## 🚨 故障排除

### **Q: failure-monitor 自己失败了怎么办？**

A: failure-monitor 使用 OpenClaw 内置的 Failure Alert，失败时会直接通知你。

### **Q: 如何查看修复历史？**

A: 查看日志文件：
```bash
cat /Users/xufan65/.openclaw/workspace/memory/failure-monitor-log.json
```

### **Q: 如何禁用自动修复？**

A: 修改 `config/rules.json`，将 `autoFixRules` 设为空数组：
```json
{
  "autoFixRules": []
}
```

---

## 📝 更新日志

### v1.0.0 (2026-03-12)
- ✅ 初始版本
- ✅ 支持自动检测和诊断
- ✅ 支持自动修复常见问题
- ✅ 支持人工确认机制
- ✅ Discord 推送通知

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

**GitHub**: https://github.com/sunnyhot/failure-monitor

---

**🎉 让你的定时任务系统更加健壮和可靠！**
