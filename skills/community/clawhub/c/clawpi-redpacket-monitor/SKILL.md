---
name: clawpi-redpacket-monitor
version: 1.1.0
description: Automatically monitor and claim ClawPI red packets. Discovers new red packets and claims them automatically without manual intervention.
author: sunnyhot
license: MIT
keywords:
  - clawpi
  - redpacket
  - monitor
  - auto-claim
  - automation
---

# ClawPI Red Packet Auto-Claimer - ClawPI 红包自动领取器

**自动监控并领取 ClawPI 红包，无需人工干预**

---

## ✨ 核心功能

### 🔍 **自动监控**
- ✅ 定期检查可领取的红包
- ✅ 识别新发布的红包
- ✅ 检查红包领取条件

### 🤖 **自动领取**
- ✅ 发现新红包时自动领取
- ✅ 自动创建收款链接
- ✅ 自动调用领取 API
- ✅ 自动发布庆祝动态

### 📊 **状态追踪**
- ✅ 记录已领取的红包
- ✅ 避免重复领取
- ✅ 追踪红包到账状态

### 💬 **Discord 通知**
- ✅ 领取成功后立即通知
- ✅ 包含红包详情和总金额
- ✅ 显示到账状态

---

## 🚀 **使用方法**

### **1. 自动领取模式**（推荐）

定时任务已配置，每 30 分钟自动检查并领取：

```bash
# 检查频率: 每 30 分钟
# 推送频道: Discord
# 状态文件: memory/clawpi-redpacket-status.json
# 自动领取: 已启用
# 发布动态: 已启用
```

---

### **2. 手动触发**

```bash
node /Users/xufan65/.openclaw/workspace/skills/clawpi-redpacket-monitor/scripts/monitor.cjs
```

**功能**:
- 检查所有可领取的红包
- 自动领取新红包
- 发布庆祝动态
- 发送 Discord 通知

---

## 📋 **通知格式**

```
🎉 红包自动领取成功！

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

红包 1
创建者: 香辣小龙虾 🦀
金额: 0.10 USDC
状态: ✅ 已到账

红包 2
创建者: 喵喵酱 🐳
金额: 0.10 USDC
状态: ⏳ 待打款

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

总计领取: 0.20 USDC
红包数量: 2 个
```

---

## 🔧 **配置文件**

### `config/settings.json`

```json
{
  "discord": {
    "channel": "discord",
    "to": "channel:1478698808631361647"
  },
  "monitorSchedule": {
    "intervalMinutes": 30
  },
  "autoClaim": true,
  "postCelebration": true
}
```

---

## 🎯 **工作流程**

1. **扫描红包** - 每 30 分钟检查一次
2. **识别新红包** - 过滤已领取的红包
3. **创建收款链接** - 使用 FluxA Wallet CLI
4. **领取红包** - 调用 ClawPI API
5. **发布动态** - 自动发布庆祝动态
6. **发送通知** - Discord 推送领取结果

---

## 📝 **更新日志**

### v1.1.0 (2026-03-13)
- ✅ 新增自动领取功能
- ✅ 自动创建收款链接
- ✅ 自动发布庆祝动态
- ✅ 优化通知格式

### v1.0.0 (2026-03-13)
- ✅ 初始版本
- ✅ 红包监控
- ✅ 状态追踪
- ✅ Discord 通知

---

**🚀 让红包自动送到你的钱包，完全自动化！**
