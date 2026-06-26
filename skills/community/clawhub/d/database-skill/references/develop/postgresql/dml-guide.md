---
name: "dml-guide-postgres"
description: "PostgreSQL DML 数据变更指南：INSERT/UPDATE/DELETE 语句编写规范与最佳实践"
---

# PostgreSQL DML 数据变更指南

本指南详细说明如何编写高质量、安全的 PostgreSQL 数据变更（DML）SQL 语句。

## 适用场景

- **INSERT**: 插入新数据
- **UPDATE**: 更新现有数据
- **DELETE**: 删除数据

## 核心规范

1.  **禁止无条件变更**: `UPDATE` and `DELETE` 语句**必须**包含 `WHERE` 条件。
2.  **批量限制**: 建议单次操作数据量控制在合理范围，大批量更新建议分批进行以减少 `WAL` 日志压力和锁竞争。
3.  **禁止物理删除**: 推荐使用软删除（如 `deleted_at`），避免直接 `DELETE` 数据。
4.  **事务控制**: 长时间运行的事务会阻碍 `VACUUM` 清理旧版本数据，应避免长事务。

## 编写规范

### 1. INSERT 语句

建议明确指定列名，推荐使用 `RETURNING` 子句获取插入后的数据（如自增ID）。

```sql
-- ✅ 推荐：指定列名
INSERT INTO users (username, email, status, created_at, updated_at) 
VALUES ('zhangsan', 'zhangsan@example.com', 1, NOW(), NOW());

-- ✅ 推荐：批量插入
INSERT INTO users (username, status) 
VALUES 
('lisi', 1),
('wangwu', 1);

-- ✅ 推荐：插入并返回 ID
INSERT INTO users (username, email) 
VALUES ('zhaoliu', 'zhaoliu@example.com')
RETURNING id;

-- ✅ 推荐：Upsert (插入或更新)
INSERT INTO users (id, username, email) 
VALUES (1, 'zhangsan', 'new_email@example.com')
ON CONFLICT (id) 
DO UPDATE SET email = EXCLUDED.email, updated_at = NOW();
```

### 2. UPDATE 语句

**必须**包含 `WHERE` 子句。

```sql
-- ✅ 推荐：通过主键更新
UPDATE users 
SET status = 2, updated_at = NOW() 
WHERE id = 1001;

-- ✅ 推荐：使用 RETURNING 获取更新后的值
UPDATE users 
SET status = 2 
WHERE id = 1001
RETURNING id, status, updated_at;
```

### 3. DELETE 语句

推荐使用软删除。

```sql
-- ✅ 推荐：软删除
UPDATE users 
SET deleted_at = NOW(), updated_at = NOW() 
WHERE id = 1001;

-- ⚠️ 慎用：物理删除
DELETE FROM temp_logs 
WHERE created_at < '2023-01-01';
```

## 最佳实践

### 安全与性能

1.  **VACUUM 友好**: 频繁的 `UPDATE` 和 `DELETE` 会产生死元组（Dead Tuples）。确保表上有合理的 `autovacuum` 设置。
2.  **索引利用**: 确保 `WHERE` 条件命中索引。
3.  **JSONB 更新**: 更新 `JSONB` 字段时，尽量只更新需要的键值，或者使用 `jsonb_set`。

### 工单填写建议

1.  **SQL 内容**: 使用标准 SQL 语法。
2.  **备注**:
    *   注明 **变更原因**。
    *   如果是大批量变更，请说明 **分批策略**。

## 调用示例

```python
# 创建 DML 工单
create_dml_sql_change_ticket(client,
    sql_text="UPDATE users SET status=2, updated_at=NOW() WHERE id=1001;",
    title="修复用户状态",
    memo="PG 库数据修复",
)
```
