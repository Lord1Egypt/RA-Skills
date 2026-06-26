# MySQL 连接参考

## 连接 URL 格式

```
mysql://user:password@host:port/database
mysql2://user:password@host:port/database
```

## 连接参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| host | 数据库主机 | localhost |
| port | 端口号 | 3306 |
| user | 用户名 | - |
| password | 密码 | - |
| database | 数据库名 | - |

## 使用脚本连接

```bash
# 使用 URL
tsx $SKILL_DIR/scripts/test-connection.ts --url "mysql://root:secret@localhost:3306/mydb"

# 使用分开的参数
tsx $SKILL_DIR/scripts/test-connection.ts \
  --db-type mysql \
  --host localhost \
  --port 3306 \
  --user root \
  --password secret \
  --database mydb
```

## 常见问题

### 连接被拒绝
- 检查 MySQL 服务是否启动
- 确认 host 和 port 正确
- 检查防火墙设置

### 认证失败
- 确认用户名和密码正确
- 检查用户是否有远程连接权限
- MySQL 8.0+ 可能需要调整认证插件

### 数据库不存在
- 确认数据库名称正确
- 检查用户是否有访问该数据库的权限
