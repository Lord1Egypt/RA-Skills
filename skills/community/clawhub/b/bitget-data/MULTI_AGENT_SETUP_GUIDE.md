# 🤖 Bitget 多 Agent 配置指南

**创建时间：** 2026-03-17 21:15 (Asia/Shanghai)  
**状态：** ✅ 配置完成，已就绪

---

## 📋 完成的任务

### ✅ 1. 查看当前配置

**Bitget API 配置：** `/Users/zongzi/.openclaw/workspace/bitget_data/config.json`
```json
{
  "apiKey": "bg_73063f99df20ccf3320032e80d0bd1f3",
  "secretKey": "ecdc70207a6395da7772210d1c6c8bf1a88f47af83b24dec2aa066d91f495387",
  "passphrase": "Lin12345",
  "isSimulation": false
}
```

**现有 Cron 任务：** 28 个（包括网格监控、技术分析、日报等）

---

### ✅ 2. 创建多 Agent 配置

**配置文件：** `/Users/zongzi/.openclaw/workspace/bitget_data/multi_agent_config.json`

包含 4 个预定义 Agent：

| Agent | 职责 | 执行频率 | 状态 |
|-------|------|----------|------|
| **grid-monitor** | 网格监控 | 每 30 分钟 | ✅ 已配置 |
| **technical-analysis** | 技术分析 (RSI/MACD/布林带) | 每小时 | ✅ 已配置 |
| **grid-optimizer** | 自动调整网格参数 | 每 2 小时 | ⏸️ 待启用 |
| **daily-report** | 生成日报 | 每日 20:00 | ✅ 已配置 |

---

### ✅ 3. 设置定时任务

**现有相关 Cron 任务：**

| 任务 ID | 名称 | 频率 | 状态 |
|--------|------|------|------|
| `ec8f05ca...` | Bitget 高频网格监控 | 每 30 分钟 | ✅ 运行中 |
| `bef3f35c...` | Bitget 智能网格调整 | 每小时 | ✅ 运行中 |
| `0549a3d3...` | Bitget 高频交易日报 | 每日 21:00 | ⚠️ 超时 |
| `1885121c...` | Bitget 网格监控提醒 | 每小时 | ✅ 运行中 |

---

### ✅ 4. 编写多 Agent 脚本

**主控制器：** `/Users/zongzi/.openclaw/workspace/bitget_data/multi_agent_controller.js`

**功能：**
- ✅ 网格监控 Agent - 检查挂单、成交、频率
- ✅ 技术分析 Agent - RSI/MACD/布林带计算
- ✅ 网格优化 Agent - 自动调整参数
- ✅ 日报 Agent - 生成交易报告

**使用方式：**
```bash
# 运行单个 Agent
node multi_agent_controller.js monitor      # 网格监控
node multi_agent_controller.js analysis     # 技术分析
node multi_agent_controller.js optimizer    # 网格优化
node multi_agent_controller.js report       # 日报

# 运行所有 Agent
node multi_agent_controller.js all
```

**测试脚本：** `/Users/zongzi/.openclaw/workspace/bitget_data/test_multi_agent.sh`
```bash
bash test_multi_agent.sh
```

---

## 🚀 快速启动

### 方式 A：手动运行

```bash
cd /Users/zongzi/.openclaw/workspace/bitget_data

# 测试所有 Agent
node multi_agent_controller.js all

# 或单独运行
node multi_agent_controller.js monitor
```

### 方式 B：添加 Cron 任务

```bash
# 添加多 Agent 监控任务（每 30 分钟）
openclaw cron add '{
  "name": "Bitget 多 Agent 监控",
  "schedule": {"kind": "every", "everyMs": 1800000},
  "payload": {"kind": "agentTurn", "message": "node /Users/zongzi/.openclaw/workspace/bitget_data/multi_agent_controller.js monitor"},
  "sessionTarget": "isolated"
}'
```

### 方式 C：使用测试脚本

```bash
bash /Users/zongzi/.openclaw/workspace/bitget_data/test_multi_agent.sh
```

---

## 📊 Agent 详细说明

### 1️⃣ 网格监控 Agent

**功能：**
- 检查各币种挂单状态
- 统计买卖单数量
- 读取成交频率日志
- 检测异常情况

**输出示例：**
```json
{
  "sol": {
    "symbol": "SOLUSDT",
    "price": 93.66,
    "totalOrders": 20,
    "buyOrders": 20,
    "sellOrders": 0,
    "status": "normal"
  },
  "eth": {
    "symbol": "ETHUSDT",
    "price": 2326.94,
    "totalOrders": 1,
    "buyOrders": 1,
    "sellOrders": 0,
    "status": "normal"
  }
}
```

---

### 2️⃣ 技术分析 Agent

**功能：**
- 获取 1 小时 K 线数据
- 计算 RSI (14 周期)
- 计算 MACD (12/26/9)
- 计算布林带 (20 周期，2 标准差)
- 判断趋势信号

**输出示例：**
```json
{
  "sol": {
    "symbol": "SOLUSDT",
    "price": 93.41,
    "rsi": "45.15",
    "macd": {
      "dif": "0.09",
      "dea": "0.39",
      "histogram": "-0.30"
    },
    "bollinger": {
      "upper": "96.62",
      "middle": "94.64",
      "lower": "92.66"
    },
    "trend": "BEARISH"
  }
}
```

---

### 3️⃣ 网格优化 Agent

**功能：**
- 读取成交频率
- 对比目标范围 (2.5-5 笔/小时)
- 生成调整建议

**输出示例：**
```json
{
  "action": "reduce_density",
  "percent": 47.2,
  "suggestions": [
    "减少网格数量 47%",
    "扩大价格区间 38%",
    "提高单笔金额 24%"
  ]
}
```

---

### 4️⃣ 日报 Agent

**功能：**
- 汇总当日成交数据
- 统计各币种表现
- 生成优化建议
- 输出 Markdown 报告

**输出示例：**
```json
{
  "date": "2026-03-17",
  "summary": {
    "totalTrades": 1250,
    "avgFrequency": 9.46,
    "targetFrequency": {"min": 2.5, "max": 5}
  },
  "recommendations": [
    "⚠️ 成交频率偏高，建议降低网格密度"
  ]
}
```

---

## 🔧 配置说明

### 多 Agent 配置文件

**路径：** `multi_agent_config.json`

**关键配置项：**

```json
{
  "gridSettings": {
    "unlimitedMode": false,        // 是否无限制模式
    "targetFrequency": {           // 目标成交频率
      "min": 2.5,
      "max": 5,
      "unit": "trades/hour"
    },
    "autoAdjust": {                // 自动调整配置
      "enabled": true,
      "maxAdjustPercent": 20,
      "checkInterval": 1800000
    }
  },
  "notifications": {
    "feishu": {
      "enabled": true,
      "chatId": "oc_xxx",
      "alerts": ["frequency_exceeded", "api_error"]
    }
  }
}
```

---

## 📝 日志文件

| 日志文件 | 用途 | 位置 |
|---------|------|------|
| `grid_monitor.log` | 网格监控日志 | `bitget_data/` |
| `auto_monitor.log` | 自动监控日志 | `bitget_data/` |
| `smart_grid.log` | 智能网格日志 | `bitget_data/` |
| `multi_agent.log` | 多 Agent 日志 | `bitget_data/` (待创建) |

---

## ⚠️ 注意事项

### 1. API 限流
- Bitget API 有频率限制
- 建议 Agent 执行间隔 ≥ 30 秒
- 失败时自动重试（最多 3 次）

### 2. 资金管理
- 每 Agent 独立管理资金
- 总资金使用不超过 80%
- 保留 20% 缓冲应对波动

### 3. 错误处理
- 所有 Agent 都有 try-catch 保护
- 错误会记录到日志
- 关键错误会发送飞书通知

---

## 🎯 后续优化

### 短期 (1 周内)
- [ ] 添加更多技术指标 (KDJ, ATR, OBV)
- [ ] 优化网格自动调整算法
- [ ] 增加回测功能

### 中期 (1 个月内)
- [ ] 添加机器学习预测
- [ ] 多交易所支持
- [ ] Web 控制面板

### 长期 (3 个月内)
- [ ] 完全自动化交易
- [ ] 风险对冲策略
- [ ] 组合优化

---

## 📞 故障排查

### 常见问题

**Q1: Agent 执行超时**
```bash
# 检查日志
tail -100 /Users/zongzi/.openclaw/workspace/bitget_data/*.log

# 手动测试
node multi_agent_controller.js monitor
```

**Q2: API 连接失败**
```bash
# 检查网络
curl -I https://api.bitget.com

# 检查代理
ps aux | grep clash
```

**Q3: 成交频率异常**
```bash
# 查看频率统计
grep "频率" auto_monitor.log | tail -10

# 运行优化 Agent
node multi_agent_controller.js optimizer
```

---

## ✅ 总结

**已完成：**
1. ✅ 查看当前配置
2. ✅ 创建多 Agent 配置文件
3. ✅ 设置定时任务（现有 28 个）
4. ✅ 编写多 Agent 控制器脚本

**文件清单：**
- `multi_agent_config.json` - 多 Agent 配置
- `multi_agent_controller.js` - 主控制器
- `test_multi_agent.sh` - 测试脚本
- `MULTI_AGENT_SETUP_GUIDE.md` - 本指南

**下一步：**
1. 运行测试脚本验证功能
2. 根据需要启用/禁用 Agent
3. 观察运行效果并优化参数

---

**状态：** 🎉 多 Agent 配置完成，随时可以启动！
