# Template Groups

- `MyBatisPlus`
  - Source: `EasyCodeConfig-mybatispuls.json`
  - Typical outputs: `entity`, `dao`, `service`, `serviceImpl`, `controller`
- `Custom-V2`
  - Source: `EasyCodeConfig-V2.json`
  - Use when user explicitly requests V2 template style
- `Custom-V3`
  - Source: `EasyCodeConfig-V3.json`
  - Default group for generic custom generation

## Selection Rule

1. If user explicitly names a group, use it.
2. Else if state has prior `template_group`, reuse it.
3. Else use `Custom-V3`.

## Rendering Notes

- Runtime rendering uses Velocity via `scripts/java/VelocityRenderBridge.java`.
- Global macros come from `src/main/resources/globalConfig/Default/*.vm`.
- Metadata priority:
  - Use `generation_config.table_columns` if provided.
  - Else auto-fetch columns via JDBC (`scripts/java/JdbcMetadataBridge.java`).
  - If JDBC driver is missing, pass `db_connection.driver_jar` and optional `db_connection.driver_class`.
