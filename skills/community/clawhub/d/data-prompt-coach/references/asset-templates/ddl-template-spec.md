# DDL 模板规格

> 适用场景：3 SQL 生成
> 配套方法论：M3（80/20 协作）+ M10（SQL 4 必看）+ M2（防幻觉三招）

## 触发场景

仅场景 3（SQL 生成）使用。当用户已有 DDL 或需要从访谈快照生成 DDL 草稿时，按此规格输出。

## 模板结构（SQL）

```sql
-- ============================================================
-- {场景名} DDL 草稿 — {日期}
-- 配套 Prompt：见 SKILL.md Step A4 输出
-- 业务口径待确认项：见文件末尾 [待确认业务口径]
-- ============================================================

-- ====== 表 1: {表名} ======
CREATE TABLE {table_name} (
    {column_name} {data_type} {constraints},
    -- ... 更多字段
    PRIMARY KEY ({pk_column}),
    INDEX idx_{column} ({column}),
    CONSTRAINT fk_{name} FOREIGN KEY ({fk_column})
        REFERENCES {ref_table}({ref_column})
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='{表说明}';

-- ====== 表 2: ... ======

-- ============================================================
-- [待确认业务口径]
-- 1. {字段/指标}: {模糊点描述} — 需用户明确
-- 2. {字段/指标}: ...
-- ============================================================
```

## 生成规则

### Step 1: 从访谈快照提取表结构

读取 SKILL.md Step A2 的 5 要素完备快照：
- 表清单（来自 ddl-analyzer 自动识别或访谈）
- 字段详情（名称、类型、约束）
- 表关系（外键）
- 索引建议
- 业务口径模糊点

### Step 2: 标注业务口径待确认项

涉及以下场景必须列入"待确认业务口径"：
- 比率类指标（分子分母未明确）→ **强制提示**
- 时间范围（动态 vs 固定）
- 去重策略（DISTINCT 是否需要）
- JOIN 类型（LEFT JOIN vs INNER JOIN）
- NULL 处理（COUNT(*) vs COUNT(field)）

### Step 3: 注入 M10 SQL 4 必看检查点

在 DDL 草稿中标注以下 4 个检查点（对应 M10）：

```sql
-- [M10 检查点 1: JOIN 类型] 此处使用 LEFT JOIN，是否需要保留未匹配行？
-- [M10 检查点 2: 时间范围] 此处使用动态时间，是否符合业务预期？
-- [M10 检查点 3: 去重] 此 COUNT 是否需要 DISTINCT？
-- [M10 检查点 4: 口径] {指标} 的分子分母是否已明确？
```

### Step 4: 与 JSON Schema 联动

DDL 草稿生成后，同时生成对应的 JSON Schema（见 [json-schema-spec.md](json-schema-spec.md)），用于：
- API 接口的请求/响应校验
- 数据导出格式规范

## 示例输出（场景 3 活跃学员统计）

```sql
-- ============================================================
-- 活跃学员统计 DDL 草稿 — 2026-07-22
-- 配套 Prompt：见 SKILL.md Step A4 输出
-- 业务口径待确认项：见文件末尾
-- ============================================================

-- ====== 表 1: students（学员主表） ======
CREATE TABLE students (
    student_id BIGINT NOT NULL COMMENT '学员ID',
    name VARCHAR(64) NOT NULL COMMENT '姓名',
    city VARCHAR(32) COMMENT '所在城市',
    register_time DATETIME NOT NULL COMMENT '注册时间',
    status TINYINT NOT NULL DEFAULT 1 COMMENT '状态: 1=活跃, 0=停用',
    PRIMARY KEY (student_id),
    INDEX idx_city (city),
    INDEX idx_register_time (register_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='学员主表';

-- ====== 表 2: orders（订单表，用于活跃度判断） ======
CREATE TABLE orders (
    order_id BIGINT NOT NULL COMMENT '订单ID',
    student_id BIGINT NOT NULL COMMENT '学员ID',
    order_time DATETIME NOT NULL COMMENT '订单时间',
    amount DECIMAL(10,2) NOT NULL COMMENT '订单金额',
    PRIMARY KEY (order_id),
    INDEX idx_student_time (student_id, order_time),
    CONSTRAINT fk_orders_student FOREIGN KEY (student_id)
        REFERENCES students(student_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单表';

-- ============================================================
-- [待确认业务口径]
-- 1. "活跃"定义：是否有订单即算活跃？还是需满足订单金额阈值？
-- 2. 时间范围：统计近 30 天 / 近 90 天 / 自然月？
-- 3. 城市归属：按注册时城市 vs 最近一次订单城市？
-- ============================================================

-- [M10 检查点 1: JOIN 类型] 建议用 LEFT JOIN students 保留无订单学员
-- [M10 检查点 2: 时间范围] 使用动态 DATE_SUB(NOW(), INTERVAL 30 DAY)
-- [M10 检查点 3: 去重] COUNT(DISTINCT student_id) 去重学员
-- [M10 检查点 4: 口径] "活跃"定义待用户确认
```

## 与其他模块的接口

| 接口 | 调用方 | 依赖 |
|------|--------|------|
| 上游 | ddl-analyzer.md | 自动识别表结构回填 |
| 上游 | SKILL.md Step A4 | 5 要素完备快照 + 方法论组合 |
| 下游 | json-schema-spec.md | 同步生成 JSON Schema |
| 下游 | verify-template-spec.md | 验真脚本检查 SQL 输出 |
| 关联方法论 | M3 80/20 协作 | AI 出草稿 + 人审业务口径 |
| 关联方法论 | M10 SQL 4 必看 | 4 个检查点 |
| 关联方法论 | M2 防幻觉三招 | 待确认业务口径段落 |
