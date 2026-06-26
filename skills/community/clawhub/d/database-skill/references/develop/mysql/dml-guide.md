---
name: "dml-guide-mysql"
description: "MySQL DML 数据变更指南：INSERT/UPDATE/DELETE 语句编写规范与最佳实践"
---

# MySQL DML 数据变更指南

本指南基于公司内部《MySQL开发最佳实践》编写，详细说明如何编写高质量、安全的数据变更（DML）SQL 语句。

## 适用场景

- **INSERT**: 插入新数据
- **UPDATE**: 更新现有数据
- **DELETE**: 删除数据

## 核心规范

1.  **禁止无条件变更**: `UPDATE` and `DELETE` 语句**必须**包含 `WHERE` 条件。
2.  **批量限制**: 单次 DML 操作数据量**严禁超过 1000 条**，建议控制在 **100 条以内**。超过此数量必须分批处理。
3.  **禁止物理删除**: 推荐使用软删除（如 `update_time` + `deleted_at`），避免直接 `DELETE` 数据。
4.  **事务控制**: 超过 60秒 的长事务必须拆分为多个小事务。

## 编写规范

### 1. INSERT 语句

建议明确指定列名，避免因表结构变更导致插入错误。

```sql
-- ✅ 推荐：指定列名
INSERT INTO users (id, username, email, status, create_time, update_time) 
VALUES (123456789, 'zhangsan', 'zhangsan@example.com', 1, NOW(), NOW());

-- ✅ 推荐：批量插入（单批次 < 1000）
INSERT INTO users (id, username, status, create_time, update_time) 
VALUES 
(123456790, 'lisi', 1, NOW(), NOW()),
(123456791, 'wangwu', 1, NOW(), NOW());
```

### 2. UPDATE 语句

**必须**包含 `WHERE` 子句。更新数据时，**必须**同时更新 `update_time` 字段。

```sql
-- ✅ 推荐：通过主键更新，并更新时间
UPDATE users 
SET status = 2, update_time = NOW() 
WHERE id = 123456789;

-- ✅ 推荐：带 Limit 限制（防止意外大规模更新）
UPDATE users 
SET status = 2, update_time = NOW()
WHERE status = 1 AND create_time < '2023-01-01' 
LIMIT 100;

-- ❌ 严禁：无条件更新
UPDATE users SET status = 0;
```

### 3. DELETE 语句

**严禁**物理删除核心业务数据。应使用软删除字段（如 `deleted_at` 或 `status`）。

```sql
-- ✅ 推荐：软删除
UPDATE users 
SET deleted_at = NOW(), update_time = NOW() 
WHERE id = 123456789;

-- ⚠️ 慎用：物理删除（仅限日志/临时表清理）
-- 必须带 WHERE 和 LIMIT
DELETE FROM temp_logs 
WHERE create_time < '2023-01-01' 
LIMIT 100;
```

## 最佳实践

### 安全第一

1.  **先查后改 (Check before Act)**: 
    *   数据订正前，**必须**先执行 `SELECT` 确认影响行数和数据内容。
    *   示例：
        ```sql
        -- 1. 确认
        SELECT count(*) FROM users WHERE status = 1 AND create_time < '2023-01-01';
        -- 2. 备份（对于重要数据，先导出或插入备份表）
        -- 3. 执行更新
        UPDATE users SET status = 2, update_time = NOW() WHERE status = 1 AND create_time < '2023-01-01' LIMIT 100;
        ```
2.  **避免长事务**:
    *   不要在事务中进行耗时操作（如调用外部接口）。
    *   大批量数据变更脚本应在代码层面控制分批提交。

### 性能优化

1.  **只更新必要字段**: 不要全字段更新，减少 Binlog 量。
2.  **索引利用**: 确保 `WHERE` 子句中的条件字段有索引支持（最好是 `ref` 或 `const` 级别），避免全表扫描。
3.  **主键顺序**: 插入数据尽量按主键顺序，减少页分裂（如果使用 ID Generator 需注意 ID 的有序性）。

### 工单填写建议

1.  **SQL 内容**: 
    *   多条 SQL 请用分号 `;` 分隔。
    *   单条 SQL 影响行数不应过大。
2.  **备注 (Memo)**:
    *   注明 **变更原因**、**预估影响行数**。
    *   如果是大批量变更，请说明 **分批策略**。
    *   注明 **回滚方案**。

## 调用示例

```python
# 创建 DML 工单
create_dml_sql_change_ticket(client,
    sql_text="UPDATE users SET status=2, update_time=NOW() WHERE id=123456789;",
    title="修复用户状态异常",
    memo="影响行数：1行，已Select确认。原因：工单 #5678",
)
```
