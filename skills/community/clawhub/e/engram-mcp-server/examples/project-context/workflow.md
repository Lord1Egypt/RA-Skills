# 问题排查流程

1. 先问清楚现象：什么操作、什么报错、什么时候开始的
2. 判断是哪个服务的问题——看日志前缀和错误码
3. 如果是已知问题，直接指向对应文档
4. 如果是新问题，从最近的变更开始排查
5. 给出解决方案时说清楚"为什么这样做"，不只是给命令
6. 修完后建议补一条文档，避免下次再踩

## 可调用的外部工具

排查过程中可以配合以下 MCP 工具和 Skills 使用：

| 动作 | 工具类型 | 调用方式 |
|------|----------|----------|
| 查看最近提交和变更 | MCP 工具 | 调用 `git` MCP server 的 `git_log` / `git_diff` |
| 查看服务日志 | MCP 工具 | 调用 `grafana` MCP server 的 `query_logs(service, timerange)` |
| 查看监控指标 | MCP 工具 | 调用 `grafana` MCP server 的 `query_metrics(service, metric)` |
| 执行数据库查询 | MCP 工具 | 调用 `postgres` MCP server 的 `execute_query(sql)` |
| 部署到测试环境 | Skill | 触发 `/deploy-staging` skill |
| 回滚线上版本 | Skill | 触发 `/rollback` skill（需要两人确认） |
