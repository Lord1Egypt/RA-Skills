# Nonce MCP Tools Reference

Nonce MCP Server: `https://mcp.nonce.app/mcp`
Antalpha wraps these tools via: `easy-mining-*` prefix

## Tool Mapping

| Antalpha Tool | Nonce Tool | Type |
|---------------|------------|------|
| easy-mining-get-workspace | get_workspace | Read |
| easy-mining-list-farms | list_farms | Read |
| easy-mining-list-agents | list_agents | Read |
| easy-mining-list-miners | list_miners | Read |
| easy-mining-list-metrics-history | list_metrics_history | Read |
| easy-mining-list-pool-diffs | list_pool_diffs | Read |
| easy-mining-list-history | list_history | Read |
| easy-mining-list-miner-tasks | list_miner_tasks | Read |
| easy-mining-list-task-batches | list_task_batches | Read |
| easy-mining-create-task-batch | create_task_batch | **Write** |
| easy-mining-get-task-batch | get_task_batch | Read |

## Official Task Names (use exactly as shown)

- `miner.system.reboot` — 重启
- `miner.power_mode.update` — 功耗模式（params: `{mode: "low_power"|"high_performance"|"normal"|"sleep"}`)
- `miner.firmware.update` — 固件升级
- `miner.network.scan` — 网络扫描
- `miner.pool.config` — 矿池配置
- `miner.light.flash` — 指示灯

> ⚠️ PRD 附录中的 `reboot`/`power_mode`/`firmware_upgrade` 是缩写，不能直接使用。
