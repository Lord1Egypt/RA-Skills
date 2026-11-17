---
name: daily-stock-analysis
description: 调用 daily_stock_analysis API 进行股票智能分析。当用户询问「分析茅台」「analyze AAPL」「帮我看看 600519」等时使用。仅支持股票代码，不支持中文名称。
metadata:
  {"openclaw": {"requires": {"env": ["DSA_BASE_URL"]}, "primaryEnv": "DSA_BASE_URL"}}
---

# Daily Stock Analysis

调用 daily_stock_analysis（DSA）REST API，在对话中触发股票智能分析。

> 原作者：ZhuLinsen  
> 原项目：https://github.com/ZhuLinsen/daily_stock_analysis  
> 本 Skill 按官方集成文档封装：https://github.com/ZhuLinsen/daily_stock_analysis/blob/main/docs/openclaw-skill-integration.md

## 触发条件

当用户请求分析某只股票时（如「分析茅台」「analyze AAPL」「帮我看看 600519」），使用本 Skill。

## 前置条件

- daily_stock_analysis 已运行：`python main.py --serve-only` 或 Docker 部署
- `DSA_BASE_URL` 已配置（见下方配置说明）

## 工作流程

### 1. 提取股票代码

从用户消息中识别股票代码。若用户仅提供中文名称（如「茅台」），需提示用户提供股票代码，或使用常见映射（茅台→600519）。

**代码格式**：

| 市场 | 格式 | 示例 |
|------|------|------|
| A股 | 6位数字 | 600519、000001、300750 |
| 北交所 | 8/4/92 开头 6 位，支持 BJ 前缀或 .BJ 后缀 | 920748、BJ920493、920493.BJ |
| 港股 | hk + 5位数字 | hk00700、hk09988 |
| 美股 | 1-5 字母（可选 .X 后缀） | AAPL、TSLA、BRK.B |
| 美股指数 | SPX/DJI/IXIC 等 | SPX、DJI、NASDAQ、VIX |

### 2. 调用 API

向 `{DSA_BASE_URL}/api/v1/analysis/analyze` 发送 POST 请求：

```json
{
  "stock_code": "<提取的代码>",
  "report_type": "detailed",
  "force_refresh": true,
  "async_mode": false,
  "skills": ["bull_trend"]
}
```

- `skills` 为可选策略 ID 数组；历史字段 `strategies` 仍保留兼容，建议优先使用 `skills`
- `force_refresh`、`async_mode` 为**布尔类型**，非字符串

**等待响应**：同步模式下分析约需 2–5 分钟，请确保 HTTP 客户端超时足够（建议 ≥300 秒）。

### 3. 解析结果

从响应的 `report.summary` 中提取：
- `operation_advice`（操作建议）
- `trend_prediction`（趋势预测）
- `analysis_summary`（分析摘要）

从 `report.strategy` 中提取：
- `ideal_buy`（理想买入价）
- `stop_loss`（止损价）
- `take_profit`（止盈价）

结构化展示优先读取可选的 `action` / `action_label`（八态：buy|add|hold|reduce|sell|watch|avoid|alert）。旧历史缺字段时可回退到 `operation_advice` 文本展示。

### 4. 错误处理

| 状态码 | error 字段 | 说明 | 处理 |
|--------|-----------|------|------|
| 400 | validation_error | 参数错误（如缺少 stock_code） | 检查代码格式 |
| 409 | duplicate_task | 该股票正在分析中 | 稍后重试或查询任务状态 |
| 500 | internal_error / analysis_failed | 分析过程发生错误 | 查看 DSA 日志排查 |

连接失败：提示检查 DSA 是否运行、DSA_BASE_URL 是否正确。

## Agent 策略问股（可选）

若 DSA 已启用 `AGENT_MODE=true`，可调用 Agent 策略问股接口，支持多轮对话与多种策略（缠论、均线金叉等）：

```bash
curl -X POST {DSA_BASE_URL}/api/v1/agent/chat \
  -H 'Content-Type: application/json' \
  -d '{"message": "用缠论分析 600519", "session_id": "optional-session-id"}'
```

响应包含 `content`（分析结论）和 `session_id`（用于多轮对话）。

## 配置说明

在 `~/.openclaw/openclaw.json` 中配置（OpenClaw 官方 skill env 注入机制）：

```json
{
  "skills": {
    "entries": {
      "daily-stock-analysis": {
        "enabled": true,
        "env": {
          "DSA_BASE_URL": "http://localhost:8000"
        }
      }
    }
  }
}
```

- 本地部署：`http://localhost:8000` 或 `http://127.0.0.1:8000`
- 远程部署：替换为实际 URL
- 建议：`DSA_BASE_URL` 勿以 `/` 结尾

## 认证说明

默认情况下 DSA API 无需认证。若在 `.env` 中启用了 `ADMIN_AUTH_ENABLED=true`，则需在 Skill 调用时携带登录后获得的 Cookie（当前 API 仅支持 Cookie 认证，不支持 Bearer Token）。

## 异步模式

`async_mode: true` 时返回 202 + `task_id`，需轮询 `GET /api/v1/analysis/status/{task_id}` 直至 `status: completed`。
