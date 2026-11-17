-- ============================================================
-- {场景名} DDL 草稿模板 — {日期}
-- 配套 Prompt：见 SKILL.md Step A4 输出
-- 业务口径待确认项：见文件末尾
-- ============================================================

-- ====== 表 1: {表名} ======
CREATE TABLE {table_name} (
    {column_name} {data_type} {constraints} COMMENT '{字段说明}',
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
-- ============================================================

-- [M10 检查点 1: JOIN 类型] 此处使用 LEFT JOIN，是否需要保留未匹配行？
-- [M10 检查点 2: 时间范围] 此处使用动态时间，是否符合业务预期？
-- [M10 检查点 3: 去重] 此 COUNT 是否需要 DISTINCT？
-- [M10 检查点 4: 口径] {指标} 的分子分母是否已明确？
