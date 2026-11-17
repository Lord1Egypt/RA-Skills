# 七块预算与口径（2026-11-09）

## 1 当前实测（安装 agent-slim 后）

| # | 块 | 字节 | 来源 | 说明 |
|---:|---|---:|---|---|
| 1 | 记忆摘要 | 8,081 | measured | `${CODEX_HOME}/memories/memory_summary.md` |
| 2 | 基础系统提示 | 21,779 | static | App 二进制最大 `instructions_template`，App 升级需重抽 |
| 3 | 技能目录 | 7,914 | measured | 安装本 skill 前 7,744，新增条目 **+170 B** |
| 4 | 权限块 | 5,665 | measured | 含 Codex 固定权限模板 |
| 5 | 全局 AGENTS | 5,443 | measured | 含 41 B 前缀 + 15 B 后缀；源文件 5,387 B |
| 6 | MCP schema | 3,900 | **占位，不是实测** | 仅为七块对账占位；见 `mcp-measure.md` |
| 7 | 环境上下文 | 350 | measured | 按 `/tmp` cwd 渲染，cwd 不同略有差异 |

- 文本七块（不含 MCP）：**49,232 B**（安装前 49,062 B；+170 B 为本 skill 条目）。
- 七块含 MCP 占位：**53,132 B**（安装前 52,962 B）。
- 文本块闸门：57,344 B → **PASS**，余量 **8,112 B**。
- 整体口径：**UNMEASURED**；已知上界 49,232 + 2,400（node_repl）+ 12,400（codex_app）= **64,032 B** → 超闸门 **6,688 B**。

## 2 三种 MCP 口径（不可混写）

| 口径 | 字节 | 含义 | 能否当每请求成本 |
|---|---:|---|---|
| 七块占位 | 3,900 | 历史假设，仅用于对账 | 否 |
| 原始 schema 已知 | 130,481 | github 126,805 + node_repl 2,400 + lis-skill-bus 1,276 | **否**；服务端 `tools/list` 总量 |
| App 实际注入 | UNMEASURED | codex_app ≤12,400 + node_repl 2,400 为已知上界 | 只有 shim 抓包后才能定论 |

- github / lis-skill-bus 在当前 App 会话未下发（工具清单只有 `mcp__codex_app__*` 与 `mcp__node_repl__*`），是 deferred 延迟下发的直接旁证（观测，不是字节实测）。
- 因此：**文本块 PASS，整体很可能 FAIL，但不能写“整体 PASS”**。
- 给整体 PASS 的可行路径（只列方案，不自动改配置）：
  1. 停用或延迟 `node_repl`；
  2. 缩减 `codex_app` 工具暴露面（31 个工具）；
  3. 或明确把闸门口径改为“文本块闸门（不含 tools schema）”。

## 3 分块预算

| 块 | 预算 | 当前 | 余量 | 依据 |
|---|---:|---:|---:|---|
| 记忆摘要 | 12,000 | 8,081 | 3,919 | 一期 s3 目标 |
| 技能目录 | 10,240 | 7,914 | 2,326 | 技能索引约 10 KB |
| 全局 AGENTS | 5,500（源文件） | 5,387 | 113 | 一期 s6 目标；注入块另含 56 B 包装 |
| 文本七块合计 | 57,344 | 49,232 | 8,112 | 56 KiB 闸门 |
| MCP | 未设独立预算 | UNMEASURED | — | 缺 App 实测，不伪造余量 |

## 4 token 实验协议（观测，不是账单）

- 数据源：`${CODEX_HOME}/scripts/token-usage.sh --days N --top 200 --json`。
- 指标：每会话 **first_request_input**（首请求 input），组内中位数、均值、样本数；不使用 cache_read 二次相加。
- 过滤：开工日期 `--start`、模型（透传 token-usage 的 `--model`）、项目（`--project` 匹配 cwd）。
- 窗口：`--baseline-start` / `--baseline-end` 对瘦身前；`--after-start` 对瘦身后。
- 最小样本：默认 5/组；不足时只写“样本不足”，不计算节省比例。
- 正式跑日期：**2026-11-12 之后**（干净窗口；避开 11-09 当天混模型、混项目、缓存干扰）。
- 输出固定字段：`billing_claim=false`、`claim_type=observational_first_request_input`；不得把观测写成账单节省。

## 5 对账与退出码

- `measure_prompt.py`：`0` = 文本块未超闸门且对账 PASS；`1` = 文本块超闸门；`2` = 基线内部不一致；`3` = 测量失败。
- 对账：七行字节相加必须等于 `total`；基线 JSON 的 `blocks` 相加必须等于基线 `total`。
- `injection_state.py`：`0` = VERIFIED/OK；`1` = DRIFT/MISSING/UNVERIFIED；`2` = 状态文件或参数错误；`3` = 未预期异常。
- `budget_dashboard.py`：`0` = 七行相加等于合计；`1` = 求和失败。与 s1 的差异只作信息展示，不冒充失败。
