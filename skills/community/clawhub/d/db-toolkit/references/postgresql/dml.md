# PostgreSQL DML 参考

## INSERT 插入

```sql
-- 插入单条
INSERT INTO users (username, email, password_hash)
VALUES ('john', 'john@example.com', 'hash123');

-- 插入并返回
INSERT INTO users (username, email, password_hash)
VALUES ('john', 'john@example.com', 'hash123')
RETURNING id, username;

-- 插入多条
INSERT INTO users (username, email, password_hash) VALUES
('alice', 'alice@example.com', 'hash456'),
('bob', 'bob@example.com', 'hash789');

-- 插入或冲突处理（UPSERT）
INSERT INTO users (username, email, password_hash)
VALUES ('john', 'john@example.com', 'newhash')
ON CONFLICT (username) DO UPDATE SET password_hash = EXCLUDED.password_hash;

-- 忽略冲突
INSERT INTO users (username, email, password_hash)
VALUES ('john', 'john@example.com', 'hash123')
ON CONFLICT (username) DO NOTHING;

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
SELECT * FROM users WHERE email ILIKE '%GMAIL%';  -- 不区分大小写

-- 排序和分页
SELECT * FROM users ORDER BY created_at DESC;
SELECT * FROM users LIMIT 10 OFFSET 20;  -- 分页
SELECT * FROM users ORDER BY id FETCH FIRST 10 ROWS ONLY;  -- SQL 标准写法

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

-- JSON 查询
SELECT metadata->>'name' as name FROM users;
SELECT * FROM users WHERE metadata @> '{"role": "admin"}';
```

## UPDATE 更新

```sql
-- 基础更新
UPDATE users SET status = 0 WHERE id = 1;

-- 多字段更新
UPDATE users 
SET status = 0, updated_at = NOW() 
WHERE id = 1;

-- 返回更新的行
UPDATE users SET status = 0 WHERE id = 1
RETURNING id, username, status;

-- 使用 FROM 子查询更新
UPDATE users u
SET status = 0
FROM orders o
WHERE u.id = o.user_id AND o.amount > 1000;

-- 条件更新
UPDATE users 
SET status = 0 
WHERE last_login_at < '2023-01-01';
```

## DELETE 删除

```sql
-- 条件删除
DELETE FROM users WHERE id = 1;

-- 返回删除的行
DELETE FROM users WHERE id = 1 RETURNING id, username;

-- 删除多条
DELETE FROM users WHERE status = 0;

-- 使用子查询删除
DELETE FROM users 
WHERE id IN (SELECT user_id FROM orders WHERE amount = 0);
```

## 事务

```sql
-- 开始事务
BEGIN;

-- 或
START TRANSACTION;

-- 提交
COMMIT;

-- 回滚
ROLLBACK;

-- 设置保存点
SAVEPOINT sp1;
ROLLBACK TO SAVEPOINT sp1;

-- 事务隔离级别
BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED;
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- 事务示例
BEGIN;
INSERT INTO orders (user_id, amount) VALUES (1, 100);
UPDATE users SET balance = balance - 100 WHERE id = 1;
COMMIT;
```

## 性能优化

```sql
-- 使用 EXPLAIN 分析查询
EXPLAIN SELECT * FROM users WHERE username = 'john';
EXPLAIN ANALYZE SELECT * FROM users WHERE username = 'john';

-- 使用 VACUUM 清理
VACUUM users;
VACUUM ANALYZE users;

-- 使用 ANALYZE 更新统计信息
ANALYZE users;

-- 批量插入优化
-- 使用 COPY 或批量 INSERT
COPY users (username, email) FROM '/path/to/data.csv' CSV;
```
