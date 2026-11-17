# content-orchestrator 错误码参考

> 来源: pipeline_state.py + content_orchestrator.py

## 错误码清单

| 错误码 | 描述 | 触发条件 | 处理方式 |
|:-------|:-----|:---------|:---------|
| PIPELINE_NOT_FOUND | 管线不存在 | pipeline_id在PG和JSON中均未找到 | 检查ID拼写,确认未过期清理 |
| STEP_NOT_FOUND | 步骤不存在 | step_name不在11步STEPS列表中 | 检查步骤名,参考valid_steps |
| INVALID_STEP_STATUS | 步骤状态不允许操作 | redo_step目标步骤非failed状态 | 只允许重试failed步骤 |
| STORE_ERROR | 管线存储失败 | PG写入失败且JSON写入也失败 | 检查PG连接+磁盘空间 |
| CREATE_ERROR | 管线创建失败 | _store()返回False | 检查PG连接+JSON目录权限 |
| REDO_ERROR | redo_step异常 | 未预期异常 | 查看日志traceback |
| NO_API_KEY | API Key未配置 | SILICONFLOW_API_KEY环境变量为空 | 配置.env中的API Key |
| MISSING_TENANT | tenant_id必填 | tenant_id为空 | 传入租户ID(RLS隔离) |

## 降级行为

- PG不可用时: 自动降级到JSON文件存储(data/content_pipelines/)
- LLM不可用时: 返回NO_API_KEY错误,不降级到本地生成
- MCP不可用时: 步骤标记为failed,等待redo_step重试
