-- Upgrade script: VectorClaw v5.0.0 → v5.0.1
-- Security audit response: addresses ClawHub audit findings (2026-05-27)
--
-- Changes:
-- 1. thought_stream.user_id made optional (NULL allowed) to decouple
--    agent reasoning logs from user-identifiable data
-- 2. Add extraction_config table for per-user opt-in tracking
-- 3. Add data_retention_policy table for configurable retention limits
-- 4. Add audit_log table for tracking data access and modifications
-- 5. System context entry for v5.0.1
--
-- ⚠️ BACK UP YOUR DATABASE BEFORE RUNNING THIS MIGRATION
-- docker exec myvector-db mysqldump -u root -p<pass> mysqlclaw > backup_pre_v5.0.1.sql

-- ============================================
-- 1. Make thought_stream.user_id optional (if table exists)
-- ============================================
-- Agent reasoning logs (chain-of-thought) should not be automatically
-- linked to identifiable users. The user_id column is now optional.
-- Note: thought_stream may be in a different database (e.g., jerith).
-- Run this manually against the correct database if needed:
--   ALTER TABLE thought_stream MODIFY COLUMN user_id VARCHAR(255) NULL;
-- Skip if table doesn't exist in this database.

-- ============================================
-- 2. Create extraction_config table (per-user opt-in)
-- ============================================
-- Tracks per-user consent for auto-extraction. Auto-extraction must be
-- explicitly enabled per-user before any data is extracted or stored.
CREATE TABLE IF NOT EXISTS extraction_config (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    auto_extract_enabled BOOLEAN DEFAULT FALSE,
    consolidation_enabled BOOLEAN DEFAULT FALSE,
    mood_tracking_enabled BOOLEAN DEFAULT TRUE,
    engagement_tracking_enabled BOOLEAN DEFAULT TRUE,
    max_retention_days INT DEFAULT 90,
    consent_given_at TIMESTAMP NULL,
    consent_method VARCHAR(64) DEFAULT 'explicit',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_extraction_user (user_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- 3. Create data_retention_policy table
-- ============================================
-- Configurable retention limits per table/data type.
-- Agent should periodically purge data older than the configured limit.
CREATE TABLE IF NOT EXISTS data_retention_policy (
    id INT AUTO_INCREMENT PRIMARY KEY,
    table_name VARCHAR(128) NOT NULL,
    data_type VARCHAR(64) NOT NULL,
    retention_days INT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    last_purged TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_retention (table_name, data_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Insert default retention policies
INSERT INTO data_retention_policy (table_name, data_type, retention_days) VALUES
    ('user_interactions', 'interaction', 30),
    ('user_mood', 'mood', 90),
    ('user_context', 'holohraphic_metadata', 30),
    ('user_context', 'consolidation_derived', 90),
    ('thought_stream', 'reasoning_log', 7),
    ('synaptic_memory', 'synaptic', 365),
    ('community_sentiment', 'sentiment', 90),
    ('trending_topics', 'trend', 90),
    ('memory_consolidation_log', 'maintenance', 365),
    ('extraction_log', 'quality_metric', 30),
    ('memories', 'auto_extracted', 30),
    ('memories', 'manual', 365)
ON DUPLICATE KEY UPDATE retention_days = VALUES(retention_days);

-- ============================================
-- 4. Create audit_log table
-- ============================================
-- Tracks all data access and modification for accountability.
-- Especially important for sensitive operations (bulk delete, extraction).
CREATE TABLE IF NOT EXISTS audit_log (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    action VARCHAR(64) NOT NULL,
    table_name VARCHAR(128),
    user_id VARCHAR(255),
    details TEXT,
    rows_affected INT DEFAULT 0,
    performer VARCHAR(64) DEFAULT 'agent',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_audit_time (created_at DESC),
    INDEX idx_audit_action (action),
    INDEX idx_audit_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- 5. Insert system context entry
-- ============================================
INSERT IGNORE INTO user_context (user_id, context_key, context_value, context_type, importance, source, is_active, created_at)
VALUES (
    '0',
    'vectorclaw_version',
    '5.0.1 — Security audit response: env-var credentials (no hardcoding), auto-extraction opt-in only, thought_stream user_id made optional, extraction_config for per-user consent, data_retention_policy table, audit_log for accountability',
    'semantic',
    0.95,
    'system',
    TRUE,
    NOW()
);

-- ============================================
-- 6. Verify upgrade
-- ============================================
SELECT 'VectorClaw v5.0.1 security upgrade complete' as status;
SELECT COUNT(*) as total_users FROM users;
SELECT COUNT(*) as extraction_configs FROM extraction_config;
SELECT COUNT(*) as retention_policies FROM data_retention_policy;
