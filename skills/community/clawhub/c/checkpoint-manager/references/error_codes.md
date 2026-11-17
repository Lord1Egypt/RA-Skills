# 错误码定义 - checkpoint-manager

> 来源: SKILL.md v1.0.0 (ARCH-5) 异常处理表

## 错误码列表

| 错误码 | 描述 | 处理方案 |
|:-------|:-----|:---------|
| INVALID_ARG | workflow_id/step_id为空或state_data非dict | 返回错误,提示必填字段及类型要求 |
| DB_NOT_CONFIGURED | DATABASE_URL未配置 | 提示配置PG连接串 |
| PG_WRITE_ERROR | PG写入失败 | 记录日志,返回错误,SQLite未写入 |
| PG_READ_ERROR | PG读取失败 | 记录日志,返回错误 |
| PG_LIST_ERROR | PG列表查询失败 | 记录日志,返回错误 |
| VERIFY_FAILED | 一致性验证失败 | 记录日志,返回错误详情 |
| REBUILD_FAILED | 缓存重建失败 | 记录日志,返回错误 |

> 注: SQLite缓存写入/读取失败为非关键错误,仅记录debug日志,业务不受影响;缓存读取失败时自动降级到PG读取
