# ChatBI Agent CLI — 命令参考

## OpenClaw 集成：流式调用

在 OpenClaw 中使用本 CLI 时，**必须**使用 `yieldMs=200` 参数触发流式返回：

```
exec(command="python3 scripts/chatbi_cli.py -q '查询销售' --output summary", yieldMs=200)
```

不要使用 `--no-stream`，CLI 内部会在每个 Tool 完成后立即 flush 结果，OpenClaw 以 ~200ms 间隔分批推送，实现渐进式展示。

## 基本用法

```bash
python3 scripts/chatbi_cli.py -q "你的问题" [选项]
```

## 参数说明

| 参数 | 简写 | 必需 | 说明 |
|------|------|------|------|
| `--query` | `-q` | ✅ | 自然语言查询问题 |
| `--output` | `-o` | ❌ | 输出模式: `summary` / `detail` / `sql-only` / `raw`，默认 `summary` |
| `--no-stream` | | ❌ | 使用非流式调用（调试用） |
| `--save-raw` | | ❌ | 将所有原始流式事件保存到指定 JSON 文件 |
| `--api-url` | | ❌ | 覆盖 API 端点 URL |

## 输出模式

### summary（默认）

输出四项关键信息：
- 🧠 意图理解（`intent_tool` → `understanding_thinking`）
- 📋 选表结果（`table_select_tool` → `table_name` + `table_selected_reason`）
- 🔍 SQL（`sql_executed`）
- ✅ 最终回答（`is_final_answer=true` 且 `type=answer`）

### detail

在 summary 基础上增加：
- 📊 执行计划（`execution_plan`）
- 📦 数据预览（`data_preview_info`）

### sql-only

仅输出生成的 SQL 语句，适合管道使用：

```bash
python3 scripts/chatbi_cli.py -q "查询销量Top10" --output sql-only | pbcopy
```

### raw

输出所有被过滤命中的事件 JSON，用于调试。

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `CHATBI_API_URL` | API 端点 URL | 内置默认值 |
| `CHATBI_UIN` | 用户 UIN | 内置默认值 |
| `CHATBI_OWNER_UIN` | 主账号 UIN | 内置默认值 |
| `CHATBI_APP_ID` | 应用 ID | 内置默认值 |
| `CHATBI_WORKSPACE_ID` | 工作空间 ID | 内置默认值 |
| `CHATBI_ROOM_KEY` | 房间 KEY | 内置默认值 |
| `CHATBI_NAMESPACE` | 命名空间 | Production |

## 示例

```bash
# 基本查询
python3 scripts/chatbi_cli.py -q "查询乳制品的销售情况"

# 查看完整过程
python3 scripts/chatbi_cli.py -q "各品类月度销售趋势" --output detail

# 仅获取 SQL
python3 scripts/chatbi_cli.py -q "查询销量Top10的商品" --output sql-only

# 调试：保存原始事件
python3 scripts/chatbi_cli.py -q "查询销售情况" --save-raw debug_events.json

# 使用自定义 API 地址
python3 scripts/chatbi_cli.py -q "查询销售情况" --api-url "http://your-server/api/v1/chatflows/xxx/prediction"
```

## 提取逻辑说明

从 Agent 流式输出中，仅提取以下事件：

| 事件条件 | 提取字段 | 含义 |
|----------|----------|------|
| `type=tool`, `tool_name=intent_tool` | `data.payload.understanding_thinking` | Agent 对用户问题的理解 |
| `type=tool`, `tool_name=table_select_tool` | `data.payload.selected_tables[].table_name`, `data.payload.table_selected_reason` | 选择了哪些表及原因 |
| `type=tool`, `tool_name=sql_execution_tool` | `data.payload.sql_executed`, `data.payload.execution_plan`, `data.payload.data_preview_info`, `data.payload.result_raw` | SQL 生成与执行结果（stage=1: SQL+计划, stage=2: 结果数据） |
| `type=answer`, `extra.is_final_answer="true"` | 逐 token 流式碎片拼接 | 最终自然语言回答 |

其他所有 Agent 输出均被忽略。
