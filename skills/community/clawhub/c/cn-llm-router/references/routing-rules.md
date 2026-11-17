# 路由规则说明（国产大模型统一路由）

本文件解释路由引擎如何把「一次对话请求」映射到「具体厂商 / 模型」。目标：**任务感知、成本最优、失败可降级**。

## 一、四种路由模式

| 模式 | 触发 | 行为 |
|------|------|------|
| `auto` | 默认 | 任务分类器 + 成本权重自动选最优 |
| `cheap` | `--model cheap` | 强制最便宜模型（批量抽取 / 分类 / 翻译场景） |
| `quality` | `--model quality` | 强制最强模型（复杂推理 / 重要产出） |
| `manual` | `--model 厂商:模型` | 显式指定，如 `deepseek:deepseek-reasoner` |

## 二、任务分类维度（auto 模式）

分类器为**纯规则 + 启发式**（零密钥、零模型、毫秒级），输出：

- `task_type`：classify / extract / summarize / translate / reason / code / long / general
- `needs_reasoning`：是否需推理（命中「为什么 / 分析 / 推导 / 根因 …」）
- `length_bucket`：short(<4k) / mid(4k–32k) / long(>32k) 以字符粗略估算
- `budget_sensitive`：分类 / 抽取 / 总结 / 翻译 → 对价格更敏感

设 `confidence` 阈值：关键词命中或含推理词 → 0.8；纯 general 且无推理词 → 0.4。
低于阈值时由路由回退到 `quality` 或 `manual`（用户可随时覆盖）。

## 三、auto 模式映射表（仅从「已配置密钥」的厂商中选择）

| 分类信号 | 偏好 |
|----------|------|
| 需推理 | DeepSeek-R1（reasoner） |
| 长文 (>32k) | Kimi-128k / 混元-long / 通义-long（上下文 ≥128k） |
| 代码 | DeepSeek-Chat / 通义 |
| 价格敏感 | GLM-4-Flash / 豆包-lite（最便宜档） |
| 常规 | DeepSeek-Chat（均衡默认） |

> 若偏好厂商未配置密钥，自动降级到「已配置厂商里最便宜 / 最强」的可用模型，并给出原因说明。

## 四、失败降级（budget guard）

- 主模型返回 429 / 5xx / 超时 → 适配器自动指数退避重试（最多 2 次）。
- 仍失败 → 路由层 budget guard 阻止「贵模型 runaway」，并记录失败调用（成本统计中的 success=0）。
- 预算阈值（config.json 的 `budget_monthly`）超支 → 主动告警（CLI 提示 + 可选企微机器人）。

## 五、成本统计（第 7 类：AI 成本 / 用量可观测）

每次调用无论成败都落本地 SQLite（`~/.cn_llm_router/calls.db`）：
厂商 / 模型 / 任务 / 入 token / 出 token / 花费 / 耗时 / 成功与否。

花费 = 入 token ÷ 1e6 × price_in + 出 token ÷ 1e6 × price_out（价格取自 models.yaml）。
`report` 命令据此出日 / 周 / 月报、各家花费柱状、成功率、P95 延迟。

## 六、与成熟网关（LiteLLM / One API）的关系

它们是独立部署的网关服务；本技能是 **WorkBuddy 内的轻量封装**：
- 复用各家 OpenAI 兼容端点（自研 urllib 适配器，零依赖）；
- 在其之上叠加**任务感知路由**（网关不内置）；
- 中文成本月报 + 可选企微 / 网盘告警（轻量本地版）。

即：站在巨人肩膀上做「国产任务感知路由 + 成本可观测」这一层差异化。
