---
name: "ddl-guide-mysql"
description: "MySQL DDL 结构变更指南：CREATE/ALTER/DROP 语句编写规范与最佳实践"
---

# MySQL DDL 结构变更指南

本指南基于公司内部《MySQL开发最佳实践》编写，详细说明如何编写符合规范的表结构变更（DDL）SQL 语句。

## 适用场景

- **CREATE TABLE**: 建表
- **ALTER TABLE**: 加减列、修改索引、修改表属性
- **DROP TABLE/INDEX**: 删表、删索引

## 核心规范

1.  **存储引擎**: 必须使用 `InnoDB` (或 `MyRocks`)。
2.  **字符集**: 统一使用 `utf8mb4` (Collation: `utf8mb4_0900_ai_ci` 或 `utf8mb4_bin`)。
3.  **主键强制**: 必须有主键。推荐使用 **`bigint unsigned`** 类型，值由公司 ID Generator 生成（**禁止使用数据库自增 ID**）。
4.  **禁止项**: 严禁使用 `Foreign Keys` (外键), `Triggers` (触发器), `Stored Procedures` (存储过程), `Views` (视图), `ENUM` 类型。
5.  **字段约束**: 
    *   所有字段（除唯一索引/deleted_at）必须为 `NOT NULL`。
    *   必须提供默认值（字符串 `''`, 数值 `0`）。
    *   必须有清晰的 `COMMENT`。

## 编写规范

### 1. 建表规范 (CREATE TABLE)

```sql
CREATE TABLE `user_orders` (
  `id` bigint(20) unsigned NOT NULL COMMENT '主键ID', -- 不使用 AUTO_INCREMENT
  `user_id` bigint(20) unsigned NOT NULL DEFAULT '0' COMMENT '用户ID',
  `order_no` varchar(64) NOT NULL DEFAULT '' COMMENT '订单号',
  `amount` decimal(12,2) NOT NULL DEFAULT '0.00' COMMENT '订单金额', -- 禁止使用 float/double
  `status` tinyint(4) NOT NULL DEFAULT '0' COMMENT '状态: 0-待支付, 1-已支付',
  `description` varchar(2048) NOT NULL DEFAULT '' COMMENT '描述', -- 超过2048建议拆表
  `is_deleted` tinyint(4) NOT NULL DEFAULT '0' COMMENT '软删除标识',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间', -- 禁止使用 TIMESTAMP
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `deleted_at` datetime DEFAULT NULL COMMENT '删除时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_order_no` (`order_no`),
  KEY `idx_user_status` (`user_id`, `status`) -- 联合索引遵循最左前缀
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='用户订单表';
```

### 2. 修改表结构 (ALTER TABLE)

优先使用 `Online DDL` 特性，建议显式指定 `ALGORITHM` 和 `LOCK`。

```sql
-- 添加字段 (INSTANT 算法，MySQL 8.0+)
ALTER TABLE `user_orders` 
ADD COLUMN `pay_channel` varchar(32) NOT NULL DEFAULT '' COMMENT '支付渠道',
ALGORITHM=INSTANT;

-- 添加索引 (INPLACE 算法，不阻塞 DML)
ALTER TABLE `user_orders` 
ADD INDEX `idx_create_time` (`create_time`),
ALGORITHM=INPLACE, LOCK=NONE;
```

## 最佳实践

### 字段设计

1.  **类型选择**:
    *   **整数**: `tinyint` (状态), `bigint unsigned` (ID). 禁止 `int` 做主键。
    *   **小数**: 必须 `decimal`。
    *   **字符串**: `char` (定长), `varchar` (变长, <2048). 避免 `BLOB/TEXT` (会导致临时表性能下降)。
    *   **时间**: `datetime`。
2.  **冗余字段**: 允许适当冗余以减少 Join，但需保证一致性。

### 索引设计

1.  **命名**: `pk_` (主键), `uk_` (唯一), `idx_` (普通)。
2.  **数量**: 单表索引建议 < 5 个。
3.  **最左前缀**: 联合索引要把最常查询的列放在最左边。
4.  **覆盖索引**: 尽量让索引包含查询所需字段，减少回表。
5.  **低基数列**: 区分度低（如性别）的列不适合单独建索引。

### 变更风险控制

1.  **大表变更**:
    *   **LOCK=NONE**: 确保使用非锁表方式。
    *   **业务低峰**: 在流量低谷期执行。
    *   **超时**: 单条 DDL 执行预计超过 1分钟 需在工单备注说明。
2.  **兼容性**:
    *   **禁止 DROP 列**: 除非确认代码已完全移除引用。
    *   **禁止修改列类型**: 尤其是缩短长度或改变类型，风险极高。

### 工单填写建议

1.  **SQL 内容**: 包含完整的 `ALGORITHM` 和 `LOCK` 提示（如果需要）。
2.  **备注**:
    *   **表数据量**: 必须注明（如 "约 500万行"）。
    *   **锁表风险**: 评估是否会锁表。
    *   **业务影响**: 是否需要停机或有短暂报错。

## 调用示例

```python
# 创建 DDL 工单
create_ddl_sql_change_ticket(client,
    sql_text="ALTER TABLE user_orders ADD INDEX idx_create_time (create_time), ALGORITHM=INPLACE, LOCK=NONE;",
    title="订单表添加时间索引",
    memo="优化后台查询性能，表数据量约 50万，使用 Online DDL 不锁表",
)
```
