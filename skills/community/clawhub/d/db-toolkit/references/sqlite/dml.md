# SQLite DML 参考

## INSERT 插入

```sql
-- 插入单条
INSERT INTO users (username, email, password_hash)
VALUES ('john', 'john@example.com', 'hash123');

-- 插入多条
INSERT INTO users (username, email, password_hash) VALUES
('alice', 'alice@example.com', 'hash456'),
('bob', 'bob@example.com', 'hash789');

-- 插入并返回 ID
-- SQLite 使用 last_insert_rowid()
INSERT INTO users (username, email, password_hash)
VALUES ('charlie', 'charlie@example.com', 'hash000');
SELECT last_insert_rowid();

-- 插入或忽略（忽略唯一约束冲突）
INSERT OR IGNORE INTO users (username, email, password_hash)
VALUES ('john', 'john@example.com', 'hash123');

-- 插入或替换（替换冲突行）
INSERT OR REPLACE INTO users (id, username, email, password_hash)
VALUES (1, 'john', 'john@example.com', 'newhash');

-- 从查询插入
INSERT INTO user_backup (username, email)
SELECT username, email FROM users WHERE status = 0;
```

## SELECT 查询

```sql
-- 基础查询
SELECT * FROM users;
SELECT id, username, email FROM users;

-- 条件查询
SELECT * FROM users WHERE status = 1;
SELECT * FROM users WHERE created_at > '2024-01-01';
SELECT * FROM users WHERE username LIKE 'j%';
SELECT * FROM users WHERE email LIKE '%gmail%';  -- 不区分大小写（LIKE）

-- 排序和分页
SELECT * FROM users ORDER BY created_at DESC;
SELECT * FROM users LIMIT 10 OFFSET 20;  -- 分页
SELECT * FROM users LIMIT 10;  -- 只限制数量

-- 聚合查询
SELECT COUNT(*) FROM users;
SELECT status, COUNT(*) as count FROM users GROUP BY status;
SELECT status, COUNT(*) FROM users GROUP BY status HAVING COUNT(*) > 10;

-- 连接查询
SELECT u.username, o.order_no
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;

-- 子查询
SELECT * FROM users WHERE id IN (SELECT user_id FROM orders);

-- CTE（公共表表达式）
WITH active_users AS (
    SELECT * FROM users WHERE status = 1
)
SELECT * FROM active_users WHERE created_at > '2024-01-01';

-- JSON 查询（SQLite 3.38.0+）
SELECT json_extract(metadata, '$.name') as name FROM users;
SELECT * FROM users WHERE json_extract(metadata, '$.role') = 'admin';
```

## UPDATE 更新

```sql
-- 基础更新
UPDATE users SET status = 0 WHERE id = 1;

-- 多字段更新
UPDATE users 
SET status = 0, updated_at = datetime('now') 
WHERE id = 1;

-- 条件更新
UPDATE users 
SET status = 0 
WHERE last_login_at < '2023-01-01';

-- 使用子查询更新
UPDATE users
SET status = 0
WHERE id IN (SELECT user_id FROM orders WHERE amount = 0);
```

## DELETE 删除

```sql
-- 条件删除
DELETE FROM users WHERE id = 1;

-- 删除多条
DELETE FROM users WHERE status = 0;

-- 删除所有数据
DELETE FROM users;
-- 重置自增 ID
DELETE FROM sqlite_sequence WHERE name = 'users';
```

## 事务

```sql
-- 开始事务
BEGIN TRANSACTION;

-- 或
BEGIN;

-- 提交
COMMIT;

-- 回滚
ROLLBACK;

-- 事务示例
BEGIN;
INSERT INTO orders (user_id, amount) VALUES (1, 100);
UPDATE users SET balance = balance - 100 WHERE id = 1;
COMMIT;

-- 嵌套事务（使用 SAVEPOINT）
BEGIN;
INSERT INTO users (username) VALUES ('test');
SAVEPOINT sp1;
INSERT INTO orders (user_id) VALUES (last_insert_rowid());
ROLLBACK TO SAVEPOINT sp1;  -- 回滚到保存点
COMMIT;  -- 只提交第一个 INSERT
```

## 性能优化

```sql
-- 使用 EXPLAIN 分析查询
EXPLAIN QUERY PLAN SELECT * FROM users WHERE username = 'john';

-- 使用 ANALYZE 更新统计信息
ANALYZE;

-- 使用 VACUUM 压缩数据库
VACUUM;

-- 批量操作优化
-- 1. 在事务中执行批量操作
BEGIN;
INSERT INTO users (username) VALUES ('a');
INSERT INTO users (username) VALUES ('b');
INSERT INTO users (username) VALUES ('c');
COMMIT;

-- 2. 临时禁用索引（大批量导入时）
-- SQLite 不支持禁用索引，需要删除后重建
DROP INDEX idx_users_username;
-- 批量导入...
CREATE INDEX idx_users_username ON users(username);
```

## 日期时间函数

```sql
-- 当前日期时间
SELECT datetime('now');  -- UTC
SELECT datetime('now', 'localtime');  -- 本地时间

-- 日期计算
SELECT datetime('now', '+1 day');
SELECT datetime('now', '-7 days');
SELECT date('now', 'start of month');

-- 日期格式化
SELECT strftime('%Y-%m-%d %H:%M:%S', 'now');
SELECT strftime('%Y年%m月%d日', 'now');
```
