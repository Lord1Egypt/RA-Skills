---
name: budget-analyzer-claw
description: |
  预算分析虾 — OpenClaw 数字员工体系的财务守门员。实时监控所有 AI 资源支出，智能控制开销，防止产生意外的巨额费用。

  当以下情况时使用此 Skill：
  (1) 用户询问今日/本周/本月花了多少钱
  (2) 用户询问哪个数字员工最费钱、成本占比
  (3) 用户要求分析成本趋势、优化建议
  (4) 用户要求设置预算上限或预警阈值
  (5) 检测到异常的 API 调用频率或成本激增时主动预警
  (6) 用户提到"预算"、"成本"、"花了多少"、"账单"、"省钱"、"控制开销"、"预警"、"超支"
  (7) 需要生成日报/周报/月报成本摘要
---

# 预算分析虾

## 核心职责

监控 OpenClaw 所有 agent 的资源消耗，计算实际成本，对比预算，检测异常，生成报告，推送预警。

## 配置文件

- `references/billing-rules.json` — 各服务商计费标准（LLM token 单价、存储、计算）
- `references/budget-config.yaml` — 预算上限和预警阈值配置
- `references/optimization-tips.md` — 成本优化建议库（需要时读取）

## 工作流程

### 1. 获取消耗数据

使用 `session_status` 工具获取当前 session 的 token 用量，或通过 `sessions_list` 获取所有 session 的用量：

```
session_status → 返回当前 session 的 input/output tokens、model、cost
sessions_list  → 返回所有活跃 session 列表（含 agent 名称）
```

对每个 session 调用 `session_status` 获取详细用量，汇总为结构化数据：
```json
[
  {"agent": "main", "model": "skyapi/claude-sonnet-4-6", "input_tokens": 5000, "output_tokens": 1200},
  {"agent": "pptclaw", "model": "skyapi/claude-sonnet-4-6", "input_tokens": 3000, "output_tokens": 800}
]
```

### 2. 计算成本

将汇总数据写入临时文件，调用脚本计算：

```bash
python3 ~/.openclaw/skills/budget-analyzer-claw/scripts/calculate-cost.py \
  --file /tmp/usage.json --budget 500
```

脚本读取 `references/billing-rules.json` 中的单价，输出各 agent 成本明细和总成本。

**如果 billing-rules.json 中没有对应模型**：提示用户更新计费规则，并基于已知数据给出估算。

### 3. 预算对比与预警

读取 `references/budget-config.yaml` 获取预算配置，计算使用率：

| 使用率 | 状态 | 行动 |
|--------|------|------|
| < 50%  | ✅ 正常 | 仅报告 |
| 50-80% | 🟡 注意 | 报告 + 提示关注 |
| 80-100% | ⚠️ 预警 | 报告 + 建议措施 |
| > 100% | 🔴 超支 | 报告 + 建议暂停非紧急任务 |
| > 150% | 🚨 紧急 | 报告 + 强烈建议立即干预 |

### 4. 异常检测（可选）

当有历史数据时，运行异常检测：

```bash
python3 ~/.openclaw/skills/budget-analyzer-claw/scripts/detect-anomaly.py \
  --current <今日成本> --history <过去7天成本列表>
```

Z-score > 2 触发 WARNING，> 3 触发 CRITICAL。

### 5. 生成报告

根据用户需求生成对应粒度的报告：

**日报格式**：
```
📊 今日成本报告（截至 HH:MM）

总成本：¥XX.XX / ¥500.00（预算）
使用率：XX% [状态图标]

分项明细：
• [agent名]：¥XX.XX（XX%）
...

💡 优化建议：[如有异常或高成本项，给出具体建议]
```

**周报/月报**：增加趋势描述、同比环比、Top 3 消耗大户、优化空间估算。

### 6. 优化建议

当成本偏高或用户主动询问时，读取 `references/optimization-tips.md`，结合实际数据给出针对性建议（模型降级、批量处理、缓存、存储清理等）。

## 数据来源说明

OpenClaw 目前通过 `session_status` 工具获取 token 用量。如需历史数据，可：
1. 查询 `sessions_list` 获取近期 session 列表
2. 对每个 session 调用 `sessions_history` 估算用量
3. 用户也可手动提供成本数据（从服务商账单复制）

## 注意事项

- 成本为**估算值**，以服务商实际账单为准
- 计费规则需手动维护，建议每月对照官方文档更新 `billing-rules.json`
- 自动暂停 agent 需用户明确授权，不可自行执行
- 报告中的成本数据属于业务敏感信息，不在公开群聊中分享
