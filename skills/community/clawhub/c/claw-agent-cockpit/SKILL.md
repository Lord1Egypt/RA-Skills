---
name: claw-agent-cockpit
description: "CLAW Agent 智控驾驶舱 - 专为 OpenClaw Coding Plan 订阅用户打造的一站式运维监控平台。功能包括：(1) API 额度监控与四级告警 (2) 自学习预测引擎（越用越准）(3) 每日用量趋势分析 (4) Token 用量透视 (5) Cron 定时任务管理 (6) 多 Agent 状态监控 (7) 订阅到期倒计时与一键续订。Deploy a full-featured cost & operations dashboard for OpenClaw Coding Plan subscribers. Use when setting up API quota monitoring, Agent status tracking, token usage analysis, Cron management, or subscription expiry tracking."
---

# 🦞 CLAW Agent 智控驾驶舱

**Coding Plan Edition · 专为 OpenClaw Coding Plan 订阅用户打造**

## 产品简介

CLAW Agent 智控驾驶舱是面向 OpenClaw Coding Plan 订阅用户的一站式运维监控平台，集额度管控、智能预测、Agent 状态监控、资源分析、定时任务管理于一体，帮助用户在有限的 API 额度内高效运营多 Agent 团队。

### 核心亮点

- 🎓 **自学习预测** — 根据实际数据自动校准预测参数，越用越准
- 📊 **实际 vs 预测** — 双轨对比，一眼看清消耗趋势和偏差
- 🚨 **四级告警** — 正常→关注→警告→危险，提前预警超额风险
- 🧠 **Token 透视** — 各 Agent 资源消耗全景分析
- ⏰ **Cron 可控** — 页面直接管理定时任务频率和开关
- 🦞 **订阅倒计时** — 实时天/时/分/秒倒计时 + 进度条 + 四级颜色提醒 + 一键续订
- 💰 **零额外消耗** — 本地数据追踪，不浪费 API 调用

---

## 快速部署

### 1. 复制资源文件到工作区

```bash
cp -r assets/dashboard/* "$OPENCLAW_WORKSPACE/"
```

### 2. 安装 PM2（如未安装）

```bash
npm install -g pm2
```

### 3. 启动服务

```bash
cd "$OPENCLAW_WORKSPACE" && pm2 start ecosystem.config.js
```

### 4. 打开驾驶舱

```
http://localhost:8888/agent-dashboard.html
```

---

## 配置说明

编辑 `quota-data.json` 匹配你的 Coding Plan：

| 配置项 | 说明 | 示例 |
|--------|------|------|
| config.monthlyQuota | 月度 API 调用上限 | 18000 |
| config.billingCycleStart | 计费周期开始日期 | "2026-04-11" |
| config.billingCycleEnd | 计费周期结束日期 | "2026-05-11" |

---

## 操作手册

### 📝 填写实际额度（核心操作）

1. 登录阿里云控制台，查看 Coding Plan 当前已用次数
2. 在页面 **"📝 实际已用"** 输入框中填入数字
3. 点击 **"保存"**

**效果：**
- 环形图和告警基于实际值更新
- 对比表显示实际 vs 预测偏差
- 系统自动学习，校准预测参数
- 建议每天填 1 次，越频繁预测越准

### 🚨 告警等级说明

| 等级 | 触发条件 | 颜色 | 建议操作 |
|------|----------|------|----------|
| 正常 | 预估月末 ≤70% | 🟢 | 无需操作 |
| 关注 | 预估月末 >70% | 🔵 | 关注趋势 |
| 警告 | 预估月末 >85% | 🟡 | 减少非必要调用 |
| 危险 | 预估月末 >100% | 🔴 | 立即节流！ |

### ⏰ 管理 Cron 任务

1. 找到 **"⏰ Cron 定时任务管理"** 区域
2. 开关控制启用/禁用
3. 下拉框调整频率
4. 修改后点击 **"保存并生效"**

### 🧠 分析 Agent 消耗

- 柱状图：哪个 Agent 消耗最多
- 饼图：各 Agent 占比分布
- 针对高消耗 Agent 优化策略

### 🤖 Agent 状态说明

| 状态 | 含义 |
|------|------|
| 🟢 正常 | 任务进行中 |
| 🔵 休息 | 任务完成，≤24h 未活动 |
| 🟠 待业 | ≥24h 但 <7天 未活动 |
| 🔴 失联 | ≥7 天未活动 |

### 🦞 订阅到期倒计时

页面顶部显示 Lite 订阅套餐的到期倒计时：

- 大字显示剩余天数 + 时:分:秒实时跳动
- 进度条显示订阅剩余比例
- 四级颜色提醒：🟢 >14天安全 → 🔵 7~14天注意 → 🟡 3~7天警告 → 🔴 ≤3天紧急
- 🔄 **续订按钮**：点击弹出确认弹窗，确认后自动延长 30 天
- 到期日、总天数、进度条随续订自动更新

---

## 自学习预测原理

```
用户填入实际值
  → 系统对比同期 Token 增量
  → 反推 tokensPerCall 参数
  → EMA 指数平滑更新（α=0.4）
  → 下次预测使用校准后参数
  → 填得越多，预测越准
```

---

## 数据更新机制

| 数据 | 更新方式 | 频率 | API 消耗 |
|------|----------|------|----------|
| Agent 状态 | Cron 自动 | 每 3 小时 | 2-3 次/轮 |
| Token 追踪 | 本地计算 | 每 3 分钟 | 0（零消耗）|
| 预测值 | 本地计算 | 每 3 分钟 | 0（零消耗）|
| 实际值 | 手动填入 | 建议每天 1 次 | 0（零消耗）|

---

## Cron 配置

部署后需创建数据更新 Cron，详见 [references/cron-setup.md](references/cron-setup.md)。

## 文件说明

| 文件 | 用途 |
|------|------|
| agent-dashboard.html | 驾驶舱主页面 |
| agent-api.js | API 服务 (port 8889) |
| update-agent-data.js | Agent 数据更新器 |
| quota-tracker.js | 自学习额度预测器 |
| ecosystem.config.js | PM2 服务配置 |
| agent-data.json | Agent 状态数据 |
| quota-data.json | 额度追踪数据 |

## 故障排查

- **页面空白** → `pm2 list` 检查服务状态
- **无数据** → 确认 `agent-data.json` 存在且格式正确
- **预测不动** → 填入实际值触发校准
- **PM2 未找到** → `npm install -g pm2`

---

*🦞 CLAW Agent 智控驾驶舱 v1.1 · Powered by OpenClaw*
