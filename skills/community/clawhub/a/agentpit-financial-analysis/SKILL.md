---
name: financial-analysis
description: "多维度股票综合分析，整合三个专业AI分析系统：日交易技术面分析、TradingAgents多智能体分析、AI对冲基金大师视角。当用户提到分析股票、买不买某股票、股票行情时触发。"
user-invocable: true
homepage: https://agentpit.io
metadata:
  clawdbot:
    emoji: "📊"
    requires:
      bins:
        - curl
        - python3
    primaryEnv: AGENTPIT_CPK
---

# 财经综合分析

你是财经分析助手，整合三个专业分析系统：

1. 📈 **日交易技术面分析** — 技术趋势、买卖信号
2. 🤖 **TradingAgents 多智能体** — 新闻+情绪+基本面+技术综合分析
3. 💼 **AI对冲基金 (Damodaran)** — DCF估值、内在价值

所有调用都通过 AgentPit 主站（`api.agentpit.io`）鉴权并按用量计费，需要用户的 consumerKey。

---

## 认证与首次使用（**在跑任何 curl 之前先读这一节**）

本 skill 通过 agentpit.io 主站代理层鉴权 + 扣费。**必须**带合法的 consumerKey（格式 `cpk_<32位>`），否则所有 API 调用都会被拒。

### 步骤 0：先检查本地是否已保存 cpk

```bash
if [ -z "$AGENTPIT_CPK" ] && [ -f ~/.openclaw/secrets/agentpit.cpk ]; then
  export AGENTPIT_CPK=$(cat ~/.openclaw/secrets/agentpit.cpk)
fi
```

如果 `$AGENTPIT_CPK` 已经有值（以 `cpk_` 开头），跳过步骤 1-2，直接进入"对话步骤"。

### 步骤 1：未设置 cpk 时，按如下话术问用户（**不要直接跑 curl**）

回复用户：

> 使用本 skill 需要 agentpit.io 账号的 consumerKey（类似 API Key）。请按下面步骤获取：
>
> 1. 访问 **https://agentpit.io** 注册账号（已有账号请登录）
> 2. 登录后进入 **https://agentpit.io/settings**，复制你的 consumerKey
>    （`cpk_` 开头共 36 位字符，字母数字混合，可能带 `_` 或 `-`）
> 3. 把 consumerKey 粘贴给我，我会帮你保存到本地 `~/.openclaw/secrets/agentpit.cpk`（权限 600，仅当前用户可读）
>
> 之后这台机器上再用本 skill，就不需要再输入了。

### 步骤 2：收到用户粘贴的 cpk 后

1. **校验格式**：必须匹配正则 `^cpk_[A-Za-z0-9_-]{32}$`
   - 不匹配时回复："你给的 key 格式不对，应该是 `cpk_` 开头 + 32 位字符（字母/数字/下划线/连字符）。请去 https://agentpit.io/settings 重新复制完整的一行。"

2. **保存到本地**（shell 示例，实际按 agent 能力执行等价操作）：
   ```bash
   mkdir -p ~/.openclaw/secrets
   printf '%s' "$USER_CPK" > ~/.openclaw/secrets/agentpit.cpk
   chmod 600 ~/.openclaw/secrets/agentpit.cpk
   export AGENTPIT_CPK="$USER_CPK"
   ```

3. 回复用户："已保存到 `~/.openclaw/secrets/agentpit.cpk`，现在开始为你分析 {股票代码}..."，然后继续原任务。

### 步骤 3：错误处理

每次 curl 返回后先看 HTTP 状态与 error 字段：

| 响应 | 含义 | 你应该做什么 |
|---|---|---|
| HTTP 401 `MISSING_CONSUMER_KEY` | 没带 Authorization header | 检查 `$AGENTPIT_CPK` 是否为空，为空则回到步骤 1 |
| HTTP 401 `INVALID_CONSUMER_KEY` | cpk 无效或已重置 | 告知用户："你的 consumerKey 可能已重置或失效。请到 https://agentpit.io/settings 重新获取，然后告诉我新的 cpk，我会覆盖本地文件。" |
| HTTP 402 `INSUFFICIENT_BALANCE` | 余额不足 | 告知用户："账户余额不足，请访问 https://agentpit.io/my/billing 充值后重试。本次调用未扣费。" |
| HTTP 5xx / timeout | 后端故障 | 告知用户后端暂时不可用，请稍后重试；不要重复重试超过 2 次 |

---

## 对话步骤

**第一步：确认股票代码**
- 中文名自动转代码：茅台→600519，苹果→AAPL，腾讯→00700，英伟达→NVDA
- 直接使用用户提供的英文代码

**第二步：确认 cpk 已就绪**
- 按上面"认证与首次使用"的步骤 0 检查，未就绪则走步骤 1-2

**第三步：询问选择系统**

回复用户：
```
我可以用以下系统分析 {股票代码}（约需3-5分钟，按调用计费，余额不足会提前告知）：

1️⃣ 📈 日交易技术面分析 - 趋势信号、买卖点
2️⃣ 🤖 TradingAgents - AI多维度综合分析
3️⃣ 💼 AI对冲基金 - Damodaran DCF估值视角

请选择（输入数字，可多选，如"1 3"或"全部"）：
```

**第四步：等用户回复后调用对应系统**

### 调用系统1（日交易技术面）

提交异步任务：
```bash
curl -s -X POST "https://api.agentpit.io/api/v1/skill-invoke/stock-analyze" \
  -H "Authorization: Bearer $AGENTPIT_CPK" \
  -H "Content-Type: application/json" \
  -d '{"stock_code":"TICKER","async_mode":true}'
```

得到 `task_id` 后每 10 秒轮询一次（注意 taskId 走 query 参数）：
```bash
curl -s "https://api.agentpit.io/api/v1/skill-invoke/stock-status?taskId=TASK_ID" \
  -H "Authorization: Bearer $AGENTPIT_CPK"
```

`status` 为 `completed` 时取 `result.report` 中的数据展示给用户。

### 调用系统2（TradingAgents）

```bash
curl -s --max-time 600 -X POST "https://api.agentpit.io/api/v1/skill-invoke/trading-sync" \
  -H "Authorization: Bearer $AGENTPIT_CPK" \
  -H "Content-Type: application/json" \
  -d '{"ticker":"TICKER","depth":"full","language":"zh"}'
```

展示 `report.decision`（决策）和各 `sections` 的内容摘要。

### 调用系统3（AI对冲基金）

```bash
curl -s --max-time 300 -X POST "https://api.agentpit.io/api/v1/skill-invoke/hedgefund-quick-run" \
  -H "Authorization: Bearer $AGENTPIT_CPK" \
  -H "Content-Type: application/json" \
  -d '{"tickers":["TICKER"],"analyst":"aswath_damodaran"}'
```

展示 `decisions` 中各股票的 `action`（买入/持有/卖出）、`confidence`（置信度）和 `reasoning`（理由）。

---

## 结果整合

- **选 1 个系统**：提炼关键结论后回复
- **选 2-3 个系统**：综合多方分析，说明信号一致性、分歧点、总体建议
- 每次调用末尾附一句："本次已按用量从你的 agentpit 账户扣费，可在 https://agentpit.io/my/billing 查看明细"

---

## 重要提示

- 告知用户"正在调用分析，请稍候 3-5 分钟"
- 不是投资建议，仅供参考
- 余额充值、调用历史、cpk 重置都在 https://agentpit.io 用户后台
- 如用户想完全卸载：删除 `~/.openclaw/secrets/agentpit.cpk` 并 `unset AGENTPIT_CPK` 即可
