# MySQL DML 参考

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
INSERT INTO users (username, email, password_hash)
VALUES ('charlie', 'charlie@example.com', 'hash000');

-- 获取最后插入的 ID
SELECT LAST_INSERT_ID();

-- 插入或更新（ON DUPLICATE KEY UPDATE）
INSERT INTO users (username, email, password_hash)
VALUES ('john', 'john@example.com', 'newhash')
ON DUPLICATE KEY UPDATE password_hash = 'newhash';
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

-- 排序和分页
SELECT * FROM users ORDER BY created_at DESC;
SELECT * FROM users LIMIT 10 OFFSET 20;  -- 分页：每页10条，第3页

-- 聚合查询
SELECT COUNT(*) FROM users;
SELECT status, COUNT(*) as count FROM users GROUP BY status;
SELECT status, COUNT(*) as count FROM users GROUP BY status HAVING count > 10;

-- 连接查询
SELECT u.username, o.order_no
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;

-- 子查询
SELECT * FROM users WHERE id IN (SELECT user_id FROM orders);
```

## UPDATE 更新

```sql
-- 基础更新
UPDATE users SET status = 0 WHERE id = 1;

-- 多字段更新
UPDATE users 
SET status = 0, updated_at = NOW() 
WHERE id = 1;

-- 条件更新
UPDATE users 
SET status = 0 
WHERE last_login_at < '2023-01-01';

-- 使用 LIMIT 限制更新行数
UPDATE users SET status = 0 WHERE status = 1 LIMIT 100;
```

## DELETE 删除

```sql
-- 条件删除
DELETE FROM users WHERE id = 1;

-- 删除多条
DELETE FROM users WHERE status = 0;

-- 使用 LIMIT
DELETE FROM users WHERE status = 0 LIMIT 100;

-- 删除所有数据（保留表结构）
TRUNCATE TABLE users;  -- 比 DELETE FROM 更快，但会重置自增 ID
```

## 事务

```sql
-- 开始事务
START TRANSACTION;

-- 或
BEGIN;

-- 提交
COMMIT;

-- 回滚
ROLLBACK;

-- 设置保存点
SAVEPOINT sp1;
ROLLBACK TO SAVEPOINT sp1;

-- 事务示例
START TRANSACTION;
INSERT INTO orders (user_id, amount) VALUES (1, 100);
UPDATE users SET balance = balance - 100 WHERE id = 1;
COMMIT;
```

## 性能优化

```sql
-- 使用 EXPLAIN 分析查询
EXPLAIN SELECT * FROM users WHERE username = 'john';

-- 使用 FORCE INDEX 强制使用索引
SELECT * FROM users FORCE INDEX (idx_username) WHERE username = 'john';

-- 批量插入优化
-- 一次性插入多条比多次插入单条快很多
INSERT INTO users (username, email) VALUES 
('a', 'a@b.com'), ('b', 'b@c.com'), ('c', 'c@d.com');
```
