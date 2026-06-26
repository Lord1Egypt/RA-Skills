-- Upgrade script: VectorClaw v4.x → v5.0.0
-- Adds auto-extraction, memory relations (knowledge graph), and MyVector self-sufficiency
-- Safe to run on production databases (uses IF NOT EXISTS / idempotent operations)

-- ============================================
-- 1. Add source tracking to memories table
-- ============================================
-- The jerith.memories table (used by self-improving system) needs source tracking
-- to distinguish manually-written memories from auto-extracted ones.

ALTER TABLE memories
  ADD COLUMN source ENUM('manual', 'auto', 'consolidation', 'import') NOT NULL DEFAULT 'manual',
  ADD COLUMN verified_by_human BOOLEAN DEFAULT FALSE,
  ADD COLUMN extraction_prompt TEXT NULL;

CREATE INDEX idx_mem_source ON memories(source);

-- ============================================
-- 2. Create memory_relations table (knowledge graph)
-- ============================================
-- Replaces Hancho's external reasoning with native MySQL graph edges.
-- Enables graph traversal during retrieval without external tools.

CREATE TABLE IF NOT EXISTS memory_relations (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    fact_id BIGINT NOT NULL,
    related_fact_id BIGINT NOT NULL,
    relation_type ENUM('mentions', 'implies', 'contradicts', 'same_entity', 'related_to') NOT NULL DEFAULT 'related_to',
    confidence FLOAT NOT NULL DEFAULT 0.5,
    source ENUM('auto', 'manual', 'consolidation') NOT NULL DEFAULT 'auto',
    discovered_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fact_id) REFERENCES memories(id) ON DELETE CASCADE,
    FOREIGN KEY (related_fact_id) REFERENCES memories(id) ON DELETE CASCADE,
    UNIQUE KEY unique_relation (fact_id, related_fact_id, relation_type),
    INDEX idx_rel_fact (fact_id),
    INDEX idx_rel_related (related_fact_id),
    INDEX idx_rel_type (relation_type),
    INDEX idx_rel_source (source),
    INDEX idx_rel_confidence (confidence)
) ENGINE=InnoDB;

-- ============================================
-- 3. Create consolidation tracking for auto-extraction
-- ============================================
-- Tracks extraction quality metrics for tuning

CREATE TABLE IF NOT EXISTS extraction_log (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    discord_id VARCHAR(32),
    input_text_length INT,
    facts_extracted INT,
    facts_merged INT,
    facts_inserted INT,
    relations_discovered INT,
    extraction_time_ms INT,
    model_used VARCHAR(128),
    fallback_used BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_ext_user (discord_id),
    INDEX idx_ext_time (created_at)
) ENGINE=InnoDB;

-- ============================================
-- 4. Extend user_context for v5.0.0 types
-- ============================================
-- Add auto-extraction and graph reasoning context types

ALTER TABLE user_context
  MODIFY COLUMN context_type ENUM(
    'episodic', 'semantic', 'procedural', 'emotional', 'preference', 'fact', 'custom',
    'hindisght', 'holohraphic', 'hancho', 'discovery', 'behavioral', 'metadata', 'reasoning', 'social_graph',
    -- v5.0.0 new types:
    'auto_extracted', 'graph_derived', 'extraction_quality'
  ) NOT NULL DEFAULT 'semantic';

-- ============================================
-- 5. Add graph traversal helper view
-- ============================================
-- Pre-computed view for fast 1-hop graph traversal during retrieval

CREATE OR REPLACE VIEW memory_graph_1hop AS
    SELECT
        r.fact_id AS source_id,
        r.related_fact_id AS target_id,
        r.relation_type,
        r.confidence AS relation_confidence,
        m.topic AS target_topic,
        m.content AS target_content,
        m.importance AS target_importance,
        m.discord_id AS target_user
    FROM memory_relations r
    JOIN memories m ON r.related_fact_id = m.id
    WHERE r.confidence >= 0.5;

-- ============================================
-- 6. Insert system context entry
-- ============================================
INSERT INTO user_context (user_id, context_key, context_value, context_type, importance, source, is_active, created_at)
VALUES (
  '0',
  'vectorclaw_version',
  '5.0.0 — MyVector self-sufficiency: auto-extraction hook (replaces Mem0), memory_relations knowledge graph (replaces Hancho), extraction logging, graph traversal view',
  'semantic',
  0.95,
  'system',
  TRUE,
  NOW()
)
ON DUPLICATE KEY UPDATE
  context_value = '5.0.0 — MyVector self-sufficiency: auto-extraction hook (replaces Mem0), memory_relations knowledge graph (replaces Hancho), extraction logging, graph traversal view',
  updated_at = NOW();

-- ============================================
-- 7. Verify upgrade
-- ============================================
SELECT 'VectorClaw v5.0.0 upgrade complete' as status;
SELECT COUNT(*) as total_memories FROM memories;
SELECT COUNT(*) as auto_memories FROM memories WHERE source = 'auto';
SELECT COUNT(*) as total_relations FROM memory_relations;
SELECT COUNT(*) as graph_edges FROM memory_relations WHERE confidence >= 0.5;
