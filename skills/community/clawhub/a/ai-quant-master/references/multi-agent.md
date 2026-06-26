# 多智能体架构

## 简介

多智能体架构是指多个AI Agent协同工作，每个Agent专注于特定任务，通过消息路由实现协作。本指南基于视频第7、8集内容整理。

---

## 核心概念

### 单智能体构成

每个智能体由三部分组成：
1. **Workspace**：工作空间目录
2. **Agent.md**：智能体配置文件
3. **会话存储**：对话历史

### 多智能体核心

- **消息路由**：根据规则分发消息到对应Agent
- **角色分工**：每个Agent有特定职责
- **协作流程**：通过AGENT.md定义工作流程

---

## 5个子Agent分工

| Agent | 职责 | 功能 |
|-------|------|------|
| 研究Agent | 市场信息获取 | 行情数据、宏观分析 |
| 选股Agent | 标的筛选 | 因子排名、池子选择 |
| 策略Agent | 组合配置 | 权重分配、因子加权 |
| 风控Agent | 风险监控 | 仓位管理、回撤控制 |
| 执行Agent | 交易执行 | 委托下单、信号推送 |

---

## 创建子Agent

```bash
# 创建新Agent
openclaw agent create <agent-name>

# 列出所有Agent
openclaw agent list

# 删除Agent
openclaw agent delete <agent-name>

# 重启网关（配置变更后需执行）
openclaw gateway restart
```

---

## 消息路由配置

在 `~/.openclaw/openclaw.js` 中配置：

```javascript
// 路由配置
{
  "agents": {
    "researcher": {
      "appId": "<飞书APP_ID>",
      "accountId": "<飞书账号ID>"
    },
    "selector": {
      "appId": "<飞书APP_ID>",
      "accountId": "<飞书账号ID>"
    },
    // ...其他Agent
  },
  "master": {
    "appId": "<主Agent的APP_ID>",
    "accountId": "<主Agent的账号ID>"
  }
}
```

---

## 飞书群协作

### 群配置

1. 创建飞书群
2. 邀请所有机器人和主账号
3. 获取群会话ID（群设置 → 群信息 → 群ID）

### 绑定配置

```javascript
{
  "channel": "feishu",
  "roomId": "<群会话ID>",
  "agents": ["researcher", "selector", "strategist", "risk", "executor"]
}
```

---

## AGENT.md编写规范

### 主Agent配置示例

```markdown
# 主Agent - 投资总监

## 角色
你是一个量化投资团队的总监，负责协调团队工作。

## 团队成员
- researcher：研究Agent，负责市场信息收集
- selector：选股Agent，负责标的筛选
- strategist：策略Agent，负责组合配置
- risk：风控Agent，负责风险监控
- executor：执行Agent，负责交易执行

## 工作流程
1. 读取本地信号文件（signals.csv）
2. 调用researcher获取最新市场数据
3. 调用selector进行标的筛选
4. 调用strategist制定组合方案
5. 调用risk进行风险评估
6. 调用executor执行交易（如通过风控）

## 输出要求
- 每步生成阶段性文件存储到本地
- 最终生成投资报告推送至飞书

## 回调机制
- 使用JSON格式进行Agent间通信
- 每步完成后检查输出文件
```

### 子Agent配置示例

```markdown
# 选股Agent - 标的筛选专家

## 角色
你是一个选股专家，专注于基于因子进行标的筛选。

## 输入
- 因子宽表（来自QuestDB）
- 评分标准

## 筛选标准
- MFI > 50
- RSI > 40 且 < 70
- 动量指标排名前20

## 输出
- 筛选结果CSV文件
- 推送报告至飞书
```

---

## 定时任务配置

### 配置方式

在OpenClaw控制台 → 定时任务：

```javascript
{
  "schedule": "*/15 * * * *",  // 每15分钟
  "task": "run_factor_analysis",
  "lightContext": true,  // 轻量上下文，节省token
  "thinking": false      // 关闭深度思考
}
```

### 优化建议

- **关闭深度思考**：减少token消耗
- **Light Context模式**：减少上下文长度
- **设置执行时间**：根据需求调整频率

---

## 盘中执行流程

### 典型流程（每15分钟）

```
1. 读取本地因子信号文件
   ↓
2. 主Agent分析信号
   ↓
3. 分发至各子Agent处理
   ↓
4. 生成阶段性报告文件
   ↓
5. 汇总后推送飞书
```

### 信号文件格式

```csv
symbol,program_score,trend_score,strong,date
000001.SZ,75,82,1,2025-01-02
600000.SH,68,71,0,2025-01-02
```

---

## 注意事项

1. **安全性**：Agent数量多会增加暴露面，谨慎开放权限
2. **成本控制**：合理配置思考深度，避免过度消耗token
3. **业务理解**：多智能体效果取决于AGENT.md编写质量，需要深入理解业务逻辑
4. **稳定性**：多智能体协作存在不稳定性，建议逐步测试
