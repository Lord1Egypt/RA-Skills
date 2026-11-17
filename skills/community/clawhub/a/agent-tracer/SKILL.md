---
name: agent-tracer
description: Record every tool call into agent-tracer (self-hosted FastAPI), then run regression testing (golden case → drift detection), attribute token costs by tool/model/agent, and surface recurring error root causes across sessions. Use when an agent must log its actions, verify behavior hasn't drifted, report spend, or debug repeated failures.
---

# agent-tracer · Agent 调用追踪 + 回归测试闭环

把 Agent 的每一次工具调用记录到 **agent-tracer**（自托管 FastAPI，轻量自建，SQLite 存储），然后获得三层能力：

1. **回归测试闭环** — 把一次成功运行提升为黄金用例（golden case），后续每次运行自动对比，行为漂移 / 回归一眼可见
2. **成本归因** — span 带上 `model` + token 数，自动按工具 / 模型 / agent 汇总成本（内置 20+ 模型定价表）
3. **多会话错误归因** — 跨 trace 按归一化指纹聚桶，找出"哪个错误天天在犯"的根因

## 前置条件

- agent-tracer 服务已运行：`http://localhost:8770`（默认，可用环境变量 `TRACER_BASE_URL` 覆盖）
- 快速启动：`pip install -r requirements.txt && python3 -m uvicorn src.api:app --host 0.0.0.0 --port 8770`

## 工作流 1：记录一次运行（trace + spans）

```bash
# 1. 创建 trace，拿到 trace_id
TRACE_ID=$(curl -s -X POST $TRACER_BASE_URL/traces \
  -H 'Content-Type: application/json' \
  -d '{"agent":"market-bot","task":"收盘汇总","session_id":"sess-001"}' \
  | python3 -c "import sys,json;print(json.load(sys.stdin)['trace_id'])")

# 2. 每次工具调用记一条 span（model/tokens 可选，带上才有成本分析）
curl -s -X POST $TRACER_BASE_URL/traces/$TRACE_ID/spans \
  -H 'Content-Type: application/json' \
  -d '{"tool_name":"web_search","arguments":{"query":"上证指数"},
       "result":"上证 3200.15 +0.85%","duration_ms":850,
       "model":"deepseek-v4-flash","input_tokens":12500,"output_tokens":800}'

# 3. 结束
curl -s -X POST $TRACER_BASE_URL/traces/$TRACE_ID/finish
```

## 工作流 2：回归测试闭环（golden case → drift）

```bash
# 把一次成功运行提升为黄金用例
curl -s -X POST $TRACER_BASE_URL/traces/$TRACE_ID/promote

# 新运行结束后，自动对照该 agent 的黄金用例检测
curl -s -X POST $TRACER_BASE_URL/traces/$NEW_TRACE_ID/check
# → verdict: match ✅ | drift ⚠️ | regression 🔴

# 批量漂移趋势（某 agent 最近 N 次 vs 黄金用例，适合 cron）
curl -s "$TRACER_BASE_URL/agents/market-bot/drift-report?limit=20"
```

判定语义：
- ✅ **match** — 与黄金用例结构一致
- ⚠️ **drift** — 行为变了但没坏（工具顺序 / 参数结构变化）
- 🔴 **regression** — 原来成功的步骤开始失败

对比基于**结构签名**（工具序列 + 参数 key 集合 + 成败状态），不依赖具体返回值，能发现"参数悄悄多了一个字段"这类静默变化。

## 工作流 3：成本归因

```bash
# 单次 trace 成本明细（per tool / per model）
curl -s $TRACER_BASE_URL/cost/traces/$TRACE_ID

# 汇总：按 agent 过滤 + 只看最近 7 天
curl -s "$TRACER_BASE_URL/cost/summary?agent=market-bot&days=7"
# → totals + per_tool + per_model + per_agent（按成本降序）
```

## 工作流 4：多会话错误归因

```bash
curl -s "$TRACER_BASE_URL/errors/aggregate?limit=500"
# → buckets: [{fingerprint, count, tool, sample_error, trace_ids}]
```

错误指纹会归一化变量部分：数字 / 超时秒数（`30s`、`60s` → `N`）/ 十六进制地址 / 引号内容。`timeout after 30s` 和 `timeout after 60s` 归到同一桶，按出现次数排序——直接暴露反复出现的根因。

## 完整 API 速查

| Method | Path | 说明 |
|--------|------|------|
| POST | `/traces` | 创建 trace（agent / task / session_id） |
| POST | `/traces/{id}/spans` | 记录工具调用（含可选 model/tokens） |
| POST | `/traces/{id}/finish` | 结束 trace |
| GET | `/traces` | 列 traces（`?agent=` 过滤） |
| GET | `/traces/{id}` | 完整 trace + spans |
| GET | `/spans/errors` | 只看失败 spans |
| POST | `/traces/{id}/promote` | 提升为黄金用例 |
| POST | `/traces/{id}/check` | 对照黄金用例检测 |
| GET | `/agents/{agent}/drift-report` | 批量漂移报告 |
| GET | `/cost/traces/{id}` | 单 trace 成本 |
| GET | `/cost/summary` | 成本汇总（agent/days 过滤） |
| GET | `/errors/aggregate` | 错误指纹聚桶 |

## 注意事项（pitfalls）

- **token 字段全部可选**：不给 model/tokens 也能记录，只是成本按 0 计；未知模型按默认估算价（`src/cost.py` 的 `DEFAULT_PRICE`）
- **老库自动迁移**：v0.4 起启动时自动 `ALTER TABLE` 补 `model/input_tokens/output_tokens` 列，无需手工迁移
- **回归检测需要先 promote**：没有黄金用例时 `/check` 返回 `found: false`，提示先 promote
- **漂移报告适合挂 cron**：每天定时跑 `drift-report`，行为漂移第一时间暴露
- **本地模型 $0**：定价表内置 qwen2.5:7b / llama3.2:3b 等本地模型为 $0，NAS 跑本地 LLM 时成本归因仍准确

## 相关链接

- 源码：https://github.com/wholegale39/agent-tracer
- 中文 README 含完整使用示例；MIT 协议，可直接自托管
