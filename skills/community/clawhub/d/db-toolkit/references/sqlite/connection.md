# SQLite 连接参考

## 连接方式

SQLite 是嵌入式数据库，直接使用文件路径连接。

## 连接参数

| 参数 | 说明 | 示例 |
|------|------|------|
| database | 数据库文件路径 | /path/to/database.db |
| :memory: | 内存数据库 | :memory: |

## 使用脚本连接

```bash
# 使用文件数据库
tsx $SKILL_DIR/scripts/test-connection.ts --url "sqlite:///path/to/database.db"

# 使用分开的参数
tsx $SKILL_DIR/scripts/test-connection.ts \
  --db-type sqlite \
  --database /path/to/database.db

# 内存数据库（测试用）
tsx $SKILL_DIR/scripts/test-connection.ts --url "sqlite://:memory:"
```

## 注意事项

### 文件权限
- 确保对数据库文件有读写权限
- 确保对数据库所在目录有写权限（用于创建临时文件）

### 并发限制
- SQLite 使用文件锁，写操作会锁定整个数据库
- 适合读多写少的场景
- 高并发写入场景建议使用 MySQL 或 PostgreSQL

### 内存数据库
- `:memory:` 数据库仅在内存中，进程结束后数据丢失
- 适合测试和临时数据处理

## 常见问题

### 数据库被锁定
- 等待其他写操作完成
- 检查是否有长时间运行的事务
- 考虑增加超时时间

### 磁盘空间不足
- 检查磁盘空间
- SQLite 会自动扩展文件大小
- 使用 VACUUM 命令可以压缩数据库

### 文件损坏
- 使用 `.recover` 命令尝试恢复
- 定期备份数据库文件
