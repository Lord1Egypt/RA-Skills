---
name: aliyun_log_query
description: 当需要查询阿里云日志（SLS）时使用此技能，支持 CLI 查询日志、分析数据。
---

## 安装

使用 uv 安装 CLI：

```bash
uv pip install -U aliyun-log-cli
```

确认安装：

```bash
aliyunlog --version
```

## 配置认证

CLI 支持三种方式（优先级：命令行参数 > 环境变量 > 配置文件）。

**如果用户没有提供 access_id 和 access_key，需要引导用户提供后再执行查询。**

### 方式一：configure 命令（推荐）

```bash
aliyunlog configure <access_id> <access_key> <endpoint>
```

示例：

```bash
aliyunlog configure LTAIxxxxxxxx xxxxxxxxx cn-hangzhou.log.aliyuncs.com
```

使用 HTTPS：

```bash
aliyunlog configure LTAIxxxxxxxx xxxxxxxxx https://cn-hangzhou.log.aliyuncs.com
```

配置文件位置：`~/.aliyunlogcli`，默认账号块名是 `main`。

### 方式二：命令行直接传参数

```bash
aliyunlog log get_log_all \
  --access-id=<value> \
  --access-key=<value> \
  --region-endpoint=<value> \
  --project=<value> \
  --logstore=<value> \
  ...
```

## SDK 方法到 CLI 命令的映射规则

规则：`aliyunlog log <子命令>` 映射到 SDK `LogClient` 的方法名，参数一一对应。

示例：
- `client.create_logstore(project_name, logstore_name, ttl=2, shard_count=30)`
- → `aliyunlog log create_logstore --project_name=... --logstore_name=... --ttl=... --shard_count=...`

## 日志查询（SQL 方式）

使用 `--power_sql=true` 启用增强 SQL 模式，通过 SQL 的 `LIMIT` 控制返回条数，避免数据量过大导致上下文爆满。

**如果用户没有指定 project 和 logstore，先查阅 `references/project_mapping.md` 查找对应的值。**

### Command Template

```bash
aliyunlog log get_log_all \
  --project="{{project}}" \
  --logstore="{{logstore}}" \
  --from_time="{{from_time}}" \
  --to_time="{{to_time}}" \
  --query="* | SELECT * FROM log WHERE {{query}} LIMIT {{limit}}" \
  --power_sql=true
```

### Inputs

| 参数名     | 必填 | 说明                                      |
|------------|------|------------------------------------------|
| project    | ✅   | SLS 项目名                                 |
| logstore   | ✅   | 日志库名                                   |
| from_time  | ✅   | 开始时间（字符串如 "2026-03-18 10:00:00" 或时间戳） |
| to_time    | ✅   | 结束时间                                   |
| query      | ❌   | SQL WHERE 条件（默认 "1=1" 表示无过滤）      |
| limit      | ❌   | 最大返回条数（默认 10）                      |

### Behavior

1. query 转化为 SQL WHERE 条件
2. 自动拼接 `SELECT * FROM log WHERE <query> LIMIT <limit>`
3. 启用 `--power_sql=true`
4. 默认 limit=10，避免输出过大

**重要：不要一次查全部日志，始终使用 LIMIT 限制返回条数。**

### Examples

**1. 查询全部日志（限制 10 条）**
```bash
aliyunlog log get_log_all \
  --project="my-project" \
  --logstore="app-log" \
  --from_time="2026-03-18 10:00:00" \
  --to_time="2026-03-18 11:00:00" \
  --query="1=1" \
  --limit=10 \
  --power_sql=true
```

**2. 查询错误日志**
```bash
aliyunlog log get_log_all \
  --project="my-project" \
  --logstore="app-log" \
  --from_time="2026-03-18 10:00:00" \
  --to_time="2026-03-18 11:00:00" \
  --query="log like '%ERROR%'" \
  --limit=10 \
  --power_sql=true
```

**3. 字段过滤**
```bash
aliyunlog log get_log_all \
  --project="my-project" \
  --logstore="app-log" \
  --from_time="2026-03-18 10:00:00" \
  --to_time="2026-03-18 11:00:00" \
  --query="status = 500" \
  --limit=10 \
  --power_sql=true
```

**4. URL 统计**
```bash
aliyunlog log get_log_all \
  --project="my-project" \
  --logstore="app-log" \
  --from_time="2026-03-18 10:00:00" \
  --to_time="2026-03-18 11:00:00" \
  --query="* | SELECT url, COUNT(*) AS cnt GROUP BY url ORDER BY cnt DESC LIMIT 10" \
  --power_sql=true
```

## 输出格式

### 格式化 JSON 输出

```bash
aliyunlog log list_project --format-output=json,no_escape
```

### 设置默认格式

```bash
aliyunlog log configure --format-output=json,no_escape
```

### 默认输出

```json
{
  "logs": [...],
  "count": 100,
  "total": 1000
}
```

## Error Handling

- CLI 执行失败 → 输出 stderr
- 无结果 → `{"logs": [], "count": 0}`

## Notes

SQL WHERE 条件语法：
- 全文搜索：`log like '%ERROR%'`
- 字段过滤：`status = 500`、`method = 'GET'`
- 组合条件：`log like '%ERROR%' AND status = 500`

统计类查询（无 WHERE）直接写完整 SQL：
- `* | SELECT url, COUNT(*) AS cnt GROUP BY url LIMIT 10`

建议：
- 限制时间范围避免慢查询
- 默认 limit=10，避免输出过大
