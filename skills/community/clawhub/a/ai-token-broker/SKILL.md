# TokenBroker Skill — 统一AI API网关

> 智能路由 + 预算管控 + 费用统计。自动选最省钱的模型，深度任务切满血版，所有调用记入账单。

## 前置条件

本 Skill 依赖 TokenBroker 后端服务（`localhost:8766`）。安装时自动检测并启动。

如果端口8766已被占用，或无法自动启动，请手动启动：
```bash
cd ~/.openclaw/workspace/production-system/token-broker
npx ts-node src/server.ts
```

## 核心能力

### 1. 智能路由（自动执行）

Agent 调 LLM 时，自动走 TokenBroker 决策：

```
任务进来
  → 查预算（TokenBudget联动的日/月预算）
  → 选供应商（默认选最便宜的可用模型）
  → 调API
  → 记录消耗到统计
```

路由策略：
| 任务类型 | 默认模型 | 说�� |
|---------|---------|------|
| 日常问答 | DeepSeek V3 Lite（免费） | 预算友好 |
| 分析/写作 | DeepSeek V4 Fast（¥2/百万token） | 性价比优先 |
| 深度推理/代码/命理 | DeepSeek V4 Thinking（¥8/百万token） | 深度任务用满血 |
| 预算紧张 + 非关键 | 自动降级到免费模型 | 自动执行 |

### 2. 管理命令

用户可以通过对话管理 TokenBroker：

| 命令 | 行为 |
|------|------|
| `Broker状态` / `网关状态` | 检查服务是否运行、连通性 |
| `路由统计` / `API统计` | 查看所有路由调用记录 |
| `设置路由 [任务类型] [供应商]` | 自定义路由规则 |
| `今天花了多少` | 查看当日费用汇总 |
| `Broker帮助` | 显示所有可用命令 |

### 3. 与TokenBudget联动

安装 TokenBroker 后，TokenBudget 的预算查询会自动显示：
```
📊 AI额度日报 — ⚡ 已对接TokenBroker网关
━━━━━━━━━━━━━━━━━━━━
今日已用: 45,320 / 100,000 token (45%)
路由优化: 自动选最便宜模型 ✅
━━━━━━━━━━━━━━━━━━━━
```

### 4. 自动健康检查

每次初始化时自动检测：
```
检查 http://localhost:8766/api/health
  → 200 → 正常加载，LLM调用走Broker
  → 失败 → 降级到直调，提示用户启动服务
```

## 安装说明

```bash
# 从ClawHub安装
clawhub install ai-token-broker

# 或从OpenClaw
openclaw skills install ai-token-broker
```

安装后：
1. 自动编译 TypeScript 代码
2. 检测端口8766是否可用
3. 启动 TokenBroker 服务
4. 配置为 Supervisor 托管

## 不适用场景

- 未安装 TokenBudget（建议先装TokenBudget）
- 用户明确指定直调模型（不走路由）
- cron定时任务（不计入日预算单独统计）

---

*最后更新：2026-05-22*
