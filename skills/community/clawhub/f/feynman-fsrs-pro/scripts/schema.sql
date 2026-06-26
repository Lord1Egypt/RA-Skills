-- ============================================================
-- 费曼记忆系统 - 数据库初始化脚本
-- ============================================================
--
-- 运行方式：
-- psql -U openclaw_feiman -d openclaw_feiman -f schema.sql
--
-- ============================================================

-- 创建 feynman_memory 表
DROP TABLE IF EXISTS feynman_memory CASCADE;

CREATE TABLE feynman_memory (
    id SERIAL PRIMARY KEY,
    concept_name VARCHAR(255) NOT NULL UNIQUE,
    obsidian_path TEXT,
    stability REAL DEFAULT 0.0,
    difficulty REAL DEFAULT 5.0,
    last_review TIMESTAMP WITH TIME ZONE,
    next_review TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    weak_points JSONB DEFAULT '[]'::jsonb,
    review_history JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 索引
CREATE INDEX idx_concept_name ON feynman_memory(concept_name);
CREATE INDEX idx_next_review ON feynman_memory(next_review);
CREATE INDEX idx_stability ON feynman_memory(stability);
CREATE INDEX idx_due_tasks ON feynman_memory(next_review, stability);

-- 自动更新 updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_feynman_memory_updated_at
    BEFORE UPDATE ON feynman_memory
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- 注释
COMMENT ON TABLE feynman_memory IS '费曼记忆系统核心表';
COMMENT ON COLUMN feynman_memory.stability IS '稳定度（天数），数值越高记忆越牢固';
COMMENT ON COLUMN feynman_memory.difficulty IS '难度系数（1-10），数值越高越难掌握';

\echo '========================================'
\echo 'feynman_memory 表初始化完成！'
\echo '========================================'
