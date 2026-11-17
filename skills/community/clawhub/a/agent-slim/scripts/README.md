# 脚本区

## 入口

```sh
python3 scripts/agent_slim.py host --home <codex-home> --output host.json
python3 scripts/agent_slim.py audit --json
python3 scripts/agent_slim.py plan --audit audit.json --output plan.json
python3 scripts/agent_slim.py apply --plan plan.json
python3 scripts/agent_slim.py apply --plan plan.json --apply
python3 scripts/agent_slim.py verify --plan plan.json --test-prompts prompts.json
python3 scripts/agent_slim.py restore --manifest <transaction>/manifest.json --apply
```

- `agent_slim.py`：CLI、只读 audit 和安全工作流调度。
- `agent_slim_adapter.py`：只读探测 Codex Home 能力，输出 `supported / unknown / unsupported` 三态；不执行插件管理或正文读取。
- `agent_slim_workflow.py`：plan/apply/verify/restore、事务 manifest、SHA-256、恢复脚本和冲突保护。

## 约束

- 纯标准库优先，兼容 Python 3.9+。
- 默认 dry-run；apply/restore 需要显式 `--apply`。
- 只允许三种移动动作；不提供删除、VACUUM、密钥/provider/认证或系统配置改动。
- 实际改动前写 manifest、manifest SHA-256、`restore.py` 和 `restore.sh`。
- 目标或隔离目标已存在时停止，不覆盖。
- 会话正文不进入报告或审计日志；只用于本地 SHA-256 和移动。
- 缺少 test-prompts 时，路由回归只能 PARTIAL，不伪造 PASS。

完整契约见 `docs/execution-contract.md`。

## 注入测量与闸门

- `measure_prompt.py`：七块固定注入测量与 57,344 B 文本块闸门。
- `injection_state.py`：源文件指纹与注入块状态机，区分 `OK / DRIFT / BODY_CHANGED / MISSING`。
- `mcp_probe.py`：只测 MCP `tools/list` schema 字节，不记录 token、请求头、请求体或提示词。
- `scan_layers.py`：记忆、AGENTS、rules、lessons 四层去重与冲突候选，只报告。
- `budget_dashboard.py`：七块预算看板，区分文本块、MCP 占位与 App 整体 `UNMEASURED`。
- `token_experiment.py`：首请求 input 观测，不是账单；固定 `billing_claim=false`。
- `self_test.py`：七块对账、gate 正反例、状态机 DRIFT、看板求和和 token 过滤的自测。

```sh
python3 scripts/measure_prompt.py --gate 57344
python3 scripts/injection_state.py --check
python3 scripts/self_test.py
```

这些脚本只读源文件与 `tools/list` schema；`injection_state.py --record` 只写状态文件并在写前备份。完整说明见 `docs/injection-measurement.md`。
