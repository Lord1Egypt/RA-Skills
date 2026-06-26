#!/usr/bin/env node
const { resolveModule } = require('../module_resolver.cjs');
/**
 * Cognitive Brain - 数据库初始化脚本
 * 初始化 PostgreSQL + Redis 存储层
 */

const fs = require('fs');
const path = require('path');

// 配置
const configPath = path.join(__dirname, '..', '..', 'config.json');
let config;
try {
  config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
} catch (e) {
  console.error('❌ 无法加载配置文件:', e.message);
  process.exit(1);
}

// SQL Schema
const SCHEMA = `
-- ============================================
-- Cognitive Brain Database Schema
-- PostgreSQL + pgvector
-- ============================================

-- 启用扩展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "vector";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- ============================================
-- 概念节点表 (语义记忆)
-- ============================================
CREATE TABLE IF NOT EXISTS concepts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  type TEXT NOT NULL DEFAULT 'concept',
  attributes JSONB DEFAULT '{}',
  embedding vector(384),
  importance REAL DEFAULT 0.5 CHECK (importance >= 0 AND importance <= 1),
  activation REAL DEFAULT 0.0,
  access_count INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  last_accessed TIMESTAMPTZ,
  last_updated TIMESTAMPTZ DEFAULT NOW(),
  
  CONSTRAINT unique_concept_name UNIQUE (name)
);

CREATE INDEX IF NOT EXISTS idx_concepts_name ON concepts (name);
CREATE INDEX IF NOT EXISTS idx_concepts_name_trgm ON concepts USING GIN (name gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_concepts_type ON concepts (type);
CREATE INDEX IF NOT EXISTS idx_concepts_importance ON concepts (importance DESC);
CREATE INDEX IF NOT EXISTS idx_concepts_embedding ON concepts USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- ============================================
-- 联想关系表
-- ============================================
CREATE TABLE IF NOT EXISTS associations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  from_id UUID NOT NULL REFERENCES concepts(id) ON DELETE CASCADE,
  to_id UUID NOT NULL REFERENCES concepts(id) ON DELETE CASCADE,
  weight REAL NOT NULL DEFAULT 0.5 CHECK (weight >= 0 AND weight <= 1),
  type TEXT NOT NULL DEFAULT 'related',
  evidence_count INTEGER DEFAULT 1,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  last_reinforced TIMESTAMPTZ,
  
  CONSTRAINT unique_association UNIQUE (from_id, to_id, type)
);

CREATE INDEX IF NOT EXISTS idx_assoc_from ON associations (from_id);
CREATE INDEX IF NOT EXISTS idx_assoc_to ON associations (to_id);
CREATE INDEX IF NOT EXISTS idx_assoc_weight ON associations (weight DESC);

-- ============================================
-- 情景记忆表
-- ============================================
CREATE TABLE IF NOT EXISTS episodes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  timestamp TIMESTAMPTZ DEFAULT NOW(),
  type TEXT NOT NULL DEFAULT 'observation',
  summary TEXT NOT NULL,
  content TEXT,
  entities JSONB DEFAULT '[]',
  emotion JSONB DEFAULT '{}',
  intent TEXT,
  role TEXT DEFAULT 'user',
  layers JSONB DEFAULT '[]',
  tags JSONB DEFAULT '[]',
  importance REAL DEFAULT 0.5 CHECK (importance >= 0 AND importance <= 1),
  embedding vector(384),
  source_session TEXT,
  source_channel TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  last_accessed TIMESTAMPTZ,
  access_count INTEGER DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_episodes_timestamp ON episodes (timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_episodes_type ON episodes (type);
CREATE INDEX IF NOT EXISTS idx_episodes_importance ON episodes (importance DESC);
CREATE INDEX IF NOT EXISTS idx_episodes_summary_trgm ON episodes USING GIN (summary gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_episodes_tags ON episodes USING GIN (tags);
CREATE INDEX IF NOT EXISTS idx_episodes_embedding ON episodes USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- ============================================
-- 反思日志表
-- ============================================
CREATE TABLE IF NOT EXISTS reflections (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  timestamp TIMESTAMPTZ DEFAULT NOW(),
  trigger_type TEXT NOT NULL,
  trigger_event TEXT NOT NULL,
  context JSONB DEFAULT '{}',
  analysis JSONB DEFAULT '{}',
  insights JSONB DEFAULT '[]',
  actions JSONB DEFAULT '[]',
  importance REAL DEFAULT 0.5,
  applied BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_reflections_timestamp ON reflections (timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_reflections_type ON reflections (trigger_type);

-- ============================================
-- 用户档案表
-- ============================================
CREATE TABLE IF NOT EXISTS user_profiles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id TEXT NOT NULL UNIQUE,
  preferences JSONB DEFAULT '{}',
  patterns JSONB DEFAULT '{}',
  known_facts JSONB DEFAULT '[]',
  interaction_stats JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  last_updated TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_user_profiles_user_id ON user_profiles (user_id);

-- ============================================
-- 自我意识状态表
-- ============================================
CREATE TABLE IF NOT EXISTS self_awareness (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  timestamp TIMESTAMPTZ DEFAULT NOW(),
  identity JSONB DEFAULT '{}',
  resources JSONB DEFAULT '{}',
  state JSONB DEFAULT '{}',
  metacognition JSONB DEFAULT '{}',
  boundaries JSONB DEFAULT '{}',
  goals JSONB DEFAULT '{}',
  overall_confidence REAL DEFAULT 0.5
);

CREATE INDEX IF NOT EXISTS idx_selfawareness_timestamp ON self_awareness (timestamp DESC);

-- ============================================
-- 子代理调用日志表
-- ============================================
CREATE TABLE IF NOT EXISTS subagent_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  timestamp TIMESTAMPTZ DEFAULT NOW(),
  task_description TEXT NOT NULL,
  subagent_type TEXT NOT NULL,
  reason TEXT,
  self_assessment JSONB DEFAULT '{}',
  fit_analysis JSONB DEFAULT '{}',
  status TEXT DEFAULT 'pending',
  result JSONB,
  reflection TEXT,
  lessons_learned JSONB DEFAULT '[]'
);

CREATE INDEX IF NOT EXISTS idx_subagent_logs_timestamp ON subagent_logs (timestamp DESC);

-- ============================================
-- 存储函数
-- ============================================

-- 联想激活传播
CREATE OR REPLACE FUNCTION spread_activation(
  start_concept TEXT,
  decay_factor REAL DEFAULT 0.9,
  threshold REAL DEFAULT 0.3,
  max_depth INTEGER DEFAULT 3
)
RETURNS TABLE (id UUID, name TEXT, level REAL, depth INTEGER) AS $$
BEGIN
  RETURN QUERY
  WITH RECURSIVE activation AS (
    SELECT 
      c.id, c.name, 1.0::REAL as level, 0 as depth, ARRAY[c.id] as path
    FROM concepts c
    WHERE c.name = start_concept
    
    UNION ALL
    
    SELECT 
      c.id, c.name, 
      act.level * a.weight * decay_factor,
      act.depth + 1,
      act.path || c.id
    FROM associations a
    JOIN concepts c ON c.id = a.to_id
    JOIN activation act ON a.from_id = act.id
    WHERE act.level * a.weight * decay_factor > threshold
      AND act.depth < max_depth
      AND NOT c.id = ANY(act.path)
  )
  SELECT DISTINCT ON (activation.id) 
    activation.id, activation.name, activation.level, activation.depth
  FROM activation
  WHERE activation.level > threshold
  ORDER BY activation.id, activation.level DESC;
END;
$$ LANGUAGE plpgsql;

-- 记忆衰减函数
CREATE OR REPLACE FUNCTION memory_retention(
  importance REAL,
  age_seconds BIGINT,
  strength_days INTEGER DEFAULT 30
)
RETURNS REAL AS $$
DECLARE
  strength_seconds BIGINT := strength_days * 86400;
BEGIN
  RETURN importance * exp(-age_seconds::FLOAT / strength_seconds::FLOAT);
END;
$$ LANGUAGE plpgsql;

-- 向量相似度搜索
CREATE OR REPLACE FUNCTION find_similar_episodes(
  query_vector vector(384),
  match_count INTEGER DEFAULT 10,
  min_similarity REAL DEFAULT 0.5
)
RETURNS TABLE (
  id UUID,
  summary TEXT,
  content TEXT,
  importance REAL,
  similarity REAL
) AS $$
BEGIN
  RETURN QUERY
  SELECT 
    e.id, e.summary, e.content, e.importance,
    1 - (e.embedding <=> query_vector) as similarity
  FROM episodes e
  WHERE e.embedding IS NOT NULL
    AND 1 - (e.embedding <=> query_vector) >= min_similarity
  ORDER BY e.embedding <=> query_vector
  LIMIT match_count;
END;
$$ LANGUAGE plpgsql;
`;

// 主函数
async function initDatabase() {
  console.log('🧠 Cognitive Brain - 数据库初始化');
  console.log('====================================\n');
  
  try {
    // 检查是否有 pg
    let pg;
    try {
      pg = resolveModule('pg');
    } catch (e) {
      console.log('⚠️  pg 模块未安装，跳过 PostgreSQL 初始化');
      console.log('   运行: npm install pg\n');
    }
    
    if (pg) {
      const { Pool } = pg;
      const pool = new Pool(config.storage.primary);
      
      console.log('📦 连接 PostgreSQL...');
      await pool.query('SELECT NOW()');
      console.log('✅ PostgreSQL 连接成功\n');
      
      console.log('📋 执行 Schema...');
      await pool.query(SCHEMA);
      console.log('✅ Schema 创建成功\n');
      
      // 统计
      const stats = await pool.query(`
        SELECT 
          (SELECT count(*) FROM concepts) as concepts,
          (SELECT count(*) FROM episodes) as episodes,
          (SELECT count(*) FROM associations) as associations,
          (SELECT count(*) FROM reflections) as reflections
      `);
      
      console.log('📊 数据库状态:');
      console.log(`   概念: ${stats.rows[0].concepts}`);
      console.log(`   情景: ${stats.rows[0].episodes}`);
      console.log(`   联想: ${stats.rows[0].associations}`);
      console.log(`   反思: ${stats.rows[0].reflections}\n`);
      
      await pool.end();
    }
    
    // 检查 Redis
    try {
      const { createClient } = require('redis');
      const redisClient = createClient({
        socket: {
          host: config.storage.cache.host,
          port: config.storage.cache.port
        }
      });
      
      console.log('📦 连接 Redis...');
      await redisClient.connect();
      await redisClient.ping();
      console.log('✅ Redis 连接成功\n');
      
      await redisClient.quit();
    } catch (e) {
      console.log('⚠️  redis 模块未安装或 Redis 未启动');
      console.log('   运行: npm install redis');
      console.log('   或启动 Redis 服务\n');
    }
    
    console.log('🎉 Cognitive Brain 初始化完成！');
    
  } catch (error) {
    console.error('❌ 初始化失败:', error.message);
    process.exit(1);
  }
}

// 执行
initDatabase();

// ============================================

