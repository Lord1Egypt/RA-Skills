# CLI reference

`apache-aiops init`, `doctor`, `version`, `build`, `config-check`, `runtime-config`, `config-includes`, `compiled-modules`, `static-directives`, `vhosts`, `modules`, `probe`, `server-status`, `error-log`, `access-status`, and `diagnose` are read commands. `graceful-reload` supports `--dry-run`; a real CLI call requires two confirmations and exits 2 when the final state remains unknown. Use `--target` to choose a configured target. `apache-aiops mcp` starts stdio MCP. CLI operations call governed MCP twins.
