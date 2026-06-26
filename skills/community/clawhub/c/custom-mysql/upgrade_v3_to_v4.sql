-- Upgrade script: VectorClaw v3.x → v4.0.0
-- Adds HindSight, HoloGraphic, and Hancho memory consolidation support
-- Safe to run on production databases (uses IF NOT EXISTS)

-- ============================================
-- 1. Extend user_context context_type enum
-- ============================================
-- Add new consolidation-related context types
ALTER TABLE user_context
  MODIFY COLUMN context_type ENUM(
    'episodic', 'semantic', 'procedural', 'emotional', 'preference', 'fact', 'custom',
    -- v4.0.0 new types:
    'hindisght', 'holohraphic', 'hancho', 'discovery', 'behavioral', 'metadata', 'reasoning', 'social_graph'
  ) NOT NULL DEFAULT 'semantic';

-- ============================================
-- 2. Add indexes for consolidation queries
-- ============================================

-- Fast lookup of consolidation-type memories by user
CREATE INDEX IF NOT EXISTS idx_context_type_importance
  ON user_context (user_id, context_type, importance);

-- Fast HindSight sentiment trend analysis
CREATE INDEX IF NOT EXISTS idx_interactions_sentiment_time
  ON user_interactions (user_id, created_at, sentiment);

-- Fast mood trend queries
CREATE INDEX IF NOT EXISTS idx_mood_user_time
  ON user_mood (user_id, created_at);

-- Fast engagement pattern lookups
CREATE INDEX IF NOT EXISTS idx_engagement_user_type
  ON user_engagement_patterns (user_id, pattern_type);

-- ============================================
-- 3. Extend memory_consolidation_log
-- ============================================
-- Ensure the table has columns for the new consolidation types
ALTER TABLE memory_consolidation_log
  ADD COLUMN IF NOT EXISTS details JSON NULL AFTER result_count;

-- ============================================
-- 4. Insert system context entries
-- ============================================
-- Mark the v4.0.0 upgrade in the system context
INSERT INTO user_context (user_id, context_key, context_value, context_type, importance, source, is_active, created_at)
VALUES (
  '0',
  'vectorclaw_version',
  '4.0.0 — Added HindSight, HoloGraphic, Hancho memory consolidation systems',
  'semantic',
  0.9,
  'system',
  TRUE,
  NOW()
)
ON DUPLICATE KEY UPDATE
  context_value = '4.0.0 — Added HindSight, HoloGraphic, Hancho memory consolidation systems',
  updated_at = NOW();

-- ============================================
-- 5. Verify upgrade
-- ============================================
SELECT 'VectorClaw v4.0.0 upgrade complete' as status;
SELECT COUNT(*) as total_context_entries FROM user_context;
SELECT COUNT(*) as consolidation_entries FROM user_context WHERE context_type IN ('hindisght', 'holohraphic', 'hancho', 'discovery', 'behavioral', 'metadata', 'reasoning', 'social_graph');
