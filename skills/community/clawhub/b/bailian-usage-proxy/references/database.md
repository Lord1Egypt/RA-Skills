# 数据库设计

## 表结构

### users - 用户表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT | 主键，自增 |
| user_key | VARCHAR(64) | 内部API Key，唯一 |
| user_name | VARCHAR(64) | 用户姓名 |
| department | VARCHAR(64) | 所属部门 |
| daily_limit | INT | 日Token限额，默认100万 |
| status | TINYINT | 1启用，0禁用 |
| created_at | TIMESTAMP | 创建时间 |

**索引：**
- PRIMARY KEY (id)
- UNIQUE KEY (user_key)
- INDEX (status)

### usage_stats - 用量统计表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BIGINT | 主键，自增 |
| user_key | VARCHAR(64) | 用户标识 |
| model | VARCHAR(64) | 模型名称 |
| hour_bucket | DATETIME | 小时时间段 |
| request_count | INT | 请求次数 |
| prompt_tokens | INT | Prompt Token数 |
| completion_tokens | INT | Completion Token数 |
| total_tokens | INT | 总Token数 |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

**索引：**
- PRIMARY KEY (id)
- UNIQUE KEY (user_key, model, hour_bucket)
- INDEX (hour_bucket)
- INDEX (user_key)

**说明：**
- 按小时聚合，减少数据量
- 支持按用户、模型、时间维度查询

### request_logs - 调用日志表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BIGINT | 主键，自增 |
| user_key | VARCHAR(64) | 用户标识 |
| request_id | VARCHAR(64) | 百炼返回的请求ID |
| model | VARCHAR(64) | 模型名称 |
| prompt_tokens | INT | Prompt Token数 |
| completion_tokens | INT | Completion Token数 |
| total_tokens | INT | 总Token数 |
| latency_ms | INT | 响应耗时（毫秒）|
| status_code | INT | HTTP状态码 |
| error_msg | TEXT | 错误信息 |
| created_at | TIMESTAMP | 创建时间 |

**索引：**
- PRIMARY KEY (id)
- INDEX (created_at)
- INDEX (user_key)

**说明：**
- 保留7天，用于问题排查和审计
- 使用分区表按时间分区

## ER 图

```
┌─────────────┐       ┌─────────────────┐       ┌─────────────────┐
│    users    │       │  usage_stats    │       │  request_logs   │
├─────────────┤       ├─────────────────┤       ├─────────────────┤
│ id (PK)     │◄──────┤ user_key (FK)   │       │ user_key (FK)   │
│ user_key    │       │ model           │       │ model           │
│ user_name   │       │ hour_bucket     │       │ request_id      │
│ department  │       │ request_count   │       │ ...             │
│ daily_limit │       │ total_tokens    │       │ created_at      │
│ status      │       │ ...             │       │                 │
└─────────────┘       └─────────────────┘       └─────────────────┘
```

## 常用查询

### 今日用量
```sql
SELECT 
    u.user_name,
    SUM(s.total_tokens) as today_tokens
FROM users u
LEFT JOIN usage_stats s ON u.user_key = s.user_key
    AND DATE(s.hour_bucket) = CURDATE()
WHERE u.status = 1
GROUP BY u.user_key;
```

### 用户日限额检查
```sql
SELECT 
    u.user_key,
    u.daily_limit,
    COALESCE(SUM(s.total_tokens), 0) as used_today,
    u.daily_limit - COALESCE(SUM(s.total_tokens), 0) as remaining
FROM users u
LEFT JOIN usage_stats s ON u.user_key = s.user_key
    AND DATE(s.hour_bucket) = CURDATE()
WHERE u.user_key = 'xxx'
GROUP BY u.user_key;
```

### 清理过期日志
```sql
-- 删除7天前的日志
DELETE FROM request_logs 
WHERE created_at < DATE_SUB(NOW(), INTERVAL 7 DAY);
```
