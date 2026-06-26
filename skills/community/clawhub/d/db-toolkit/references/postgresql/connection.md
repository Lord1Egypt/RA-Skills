# PostgreSQL 连接参考

## 连接 URL 格式

```
postgresql://user:password@host:port/database
postgres://user:password@host:port/database
```

## 连接参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| host | 数据库主机 | localhost |
| port | 端口号 | 5432 |
| user | 用户名 | - |
| password | 密码 | - |
| database | 数据库名 | - |
| sslmode | SSL 模式 | prefer |

## 使用脚本连接

```bash
# 使用 URL
tsx $SKILL_DIR/scripts/test-connection.ts --url "postgresql://postgres:secret@localhost:5432/mydb"

# 使用分开的参数
tsx $SKILL_DIR/scripts/test-connection.ts \
  --db-type postgresql \
  --host localhost \
  --port 5432 \
  --user postgres \
  --password secret \
  --database mydb
```

## SSL 连接

```bash
# 要求 SSL
tsx $SKILL_DIR/scripts/test-connection.ts --url "postgresql://user:pass@host/db?sslmode=require"
```

## 常见问题

### 连接被拒绝
- 检查 PostgreSQL 服务是否启动
- 确认 pg_hba.conf 允许连接
- 检查 postgresql.conf 中的 listen_addresses

### 认证失败
- 确认用户名和密码正确
- 检查 pg_hba.conf 认证方法
- 确认数据库存在

### 角色不存在
- PostgreSQL 用户称为"角色"
- 使用 `CREATE ROLE` 或 `CREATE USER` 创建
