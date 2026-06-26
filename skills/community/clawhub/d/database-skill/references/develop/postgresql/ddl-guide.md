---
name: "ddl-guide-postgres"
description: "PostgreSQL DDL 结构变更指南：CREATE/ALTER/DROP 语句编写规范与最佳实践"
---

# PostgreSQL DDL 结构变更指南

本指南详细说明如何编写符合规范的 PostgreSQL 表结构变更（DDL）SQL 语句。

## 适用场景

- **CREATE TABLE**: 建表
- **ALTER TABLE**: 加减列、修改索引、修改表属性
- **DROP TABLE/INDEX**: 删表、删索引

## 核心规范

1.  **命名规范**: 使用小写字母和下划线（snake_case）。
2.  **主键强制**: 必须有主键 (`PRIMARY KEY`)。
3.  **注释**: 表和关键字段必须有 `COMMENT`。
4.  **类型推荐**:
    *   ID: `bigserial` (自增) 或 `uuid`.
    *   时间: `timestamptz` (带时区的时间戳).
    *   JSON: `jsonb` (二进制 JSON，支持索引).
    *   文本: `text` (PG 中 `text` 和 `varchar` 性能几乎无差，推荐 `text`).

## 编写规范

### 1. 建表规范 (CREATE TABLE)

```sql
CREATE TABLE user_orders (
    id bigserial PRIMARY KEY, -- 自增主键
    user_id bigint NOT NULL,
    order_no text NOT NULL DEFAULT '',
    amount numeric(12, 2) NOT NULL DEFAULT 0.00,
    status smallint NOT NULL DEFAULT 0,
    extra_info jsonb DEFAULT '{}', -- JSONB 类型
    created_at timestamptz NOT NULL DEFAULT NOW(), -- 带时区
    updated_at timestamptz NOT NULL DEFAULT NOW(),
    deleted_at timestamptz
);

-- 添加注释
COMMENT ON TABLE user_orders IS '用户订单表';
COMMENT ON COLUMN user_orders.id IS '主键ID';
COMMENT ON COLUMN user_orders.status IS '状态: 0-待支付, 1-已支付';

-- 创建索引
CREATE UNIQUE INDEX uk_order_no ON user_orders (order_no);
CREATE INDEX idx_user_status ON user_orders (user_id, status);
-- GIN 索引用于 JSONB
CREATE INDEX idx_extra_info ON user_orders USING GIN (extra_info);
```

### 2. 修改表结构 (ALTER TABLE)

PostgreSQL 的 DDL 大多支持事务，且很多操作（如添加带默认值的列）在 PG 11+ 是瞬间完成的。

```sql
-- 添加字段
ALTER TABLE user_orders 
ADD COLUMN pay_channel text DEFAULT '';

-- 添加索引 (建议使用 CONCURRENTLY 避免锁表)
-- 注意: CONCURRENTLY 不能在事务块中运行，但在工单系统中通常会单独处理
CREATE INDEX CONCURRENTLY idx_created_at ON user_orders (created_at);

-- 修改字段类型 (慎用，可能会重写表)
-- 这种操作建议在业务低峰期进行
ALTER TABLE user_orders 
ALTER COLUMN amount TYPE numeric(14, 2);
```

## 最佳实践

### 锁机制与风险

1.  **CREATE INDEX CONCURRENTLY**: 
    *   标准 `CREATE INDEX` 会锁定表（排他锁），阻止写入。
    *   **强烈推荐**使用 `CONCURRENTLY` 关键字创建索引，它允许在构建索引时继续进行读写操作。
    *   *注意*: `CONCURRENTLY` 操作耗时更长，且不能在事务块中执行（工单系统需特殊支持或单独执行）。
2.  **添加列**: 
    *   PG 11+ 添加带 `DEFAULT` 值的列不需要重写表，非常快。
3.  **锁队列**: DDL 操作需要获取排他锁，如果长事务占用了锁，DDL 会等待，导致后续的所有查询也被阻塞（锁队列效应）。务必确保没有长事务运行。

### 工单填写建议

1.  **索引创建**: 显式注明是否使用 `CONCURRENTLY`。
2.  **备注**:
    *   **表数据量**: 必须注明。
    *   **业务影响**: 是否需要停机。

## 调用示例

```python
# 创建 DDL 工单
create_ddl_sql_change_ticket(client,
    sql_text="CREATE INDEX CONCURRENTLY idx_created_at ON user_orders (created_at);",
    title="订单表添加时间索引",
    memo="PG 库，使用 CONCURRENTLY 避免锁表，表数据量约 100万",
)
```
