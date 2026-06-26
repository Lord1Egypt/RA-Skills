-- ============================================
-- MySQLClaw Database Upgrade: v1.x → v2.0.0
-- Safe to run on existing database — preserves all data
-- Uses individual ALTER/CREATE statements compatible with MySQL 8.0
-- ============================================

USE mysqlclaw;

-- ============================================
-- PART 1: Create new tables (12 missing)
-- ============================================

CREATE TABLE IF NOT EXISTS user_mood (
    mood_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    mood_state ENUM('happy','excited','calm','neutral','tired','stressed','frustrated','sad','angry','anxious') NOT NULL,
    intensity FLOAT DEFAULT 0.5,
    trigger_topic VARCHAR(255),
    trigger_context TEXT,
    source_channel VARCHAR(32),
    source_message_id VARCHAR(32),
    confidence FLOAT DEFAULT 0.7,
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_mood_user_time (user_id, created_at DESC),
    INDEX idx_mood_state (mood_state)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS user_engagement_patterns (
    pattern_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    pattern_type ENUM('time_of_day','day_of_week','topic_trigger','channel_preference','response_style','session_length','activity_burst') NOT NULL,
    pattern_key VARCHAR(255) NOT NULL,
    pattern_value TEXT,
    frequency INT DEFAULT 1,
    confidence FLOAT DEFAULT 0.5,
    first_observed TIMESTAMP NULL,
    last_observed TIMESTAMP NULL,
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_pattern_user_type (user_id, pattern_type),
    INDEX idx_pattern_confidence (confidence)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS conversation_sessions (
    session_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    channel_id VARCHAR(32),
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP NULL,
    topic VARCHAR(255),
    summary TEXT,
    message_count INT DEFAULT 0,
    avg_sentiment FLOAT DEFAULT 0.0,
    mood_start VARCHAR(32),
    mood_end VARCHAR(32),
    key_points JSON,
    metadata JSON,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_session_user_time (user_id, started_at DESC),
    INDEX idx_session_channel (channel_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS session_interactions (
    session_id INT NOT NULL,
    interaction_id INT NOT NULL,
    PRIMARY KEY (session_id, interaction_id),
    FOREIGN KEY (session_id) REFERENCES conversation_sessions(session_id) ON DELETE CASCADE,
    FOREIGN KEY (interaction_id) REFERENCES user_interactions(interaction_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS proactive_reminders (
    reminder_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    trigger_type ENUM('time_based','event_based','pattern_based','followup') NOT NULL,
    trigger_condition TEXT NOT NULL,
    reminder_text TEXT NOT NULL,
    priority ENUM('low','medium','high') DEFAULT 'medium',
    is_active BOOLEAN DEFAULT TRUE,
    triggered_at TIMESTAMP NULL,
    trigger_count INT DEFAULT 0,
    max_triggers INT DEFAULT 1,
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_reminder_user_active (user_id, is_active),
    INDEX idx_reminder_trigger_type (trigger_type),
    INDEX idx_reminder_priority (priority)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS synaptic_memory (
    memory_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    memory_key VARCHAR(255) NOT NULL,
    memory_value TEXT,
    priority TINYINT DEFAULT 5,
    decay_rate FLOAT DEFAULT 0.01,
    access_count INT DEFAULT 0,
    last_accessed TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_synaptic_key (user_id, memory_key),
    INDEX idx_synaptic_user (user_id),
    INDEX idx_synaptic_priority (priority DESC),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS thought_stream (
    thought_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255),
    channel_id VARCHAR(32),
    thought TEXT NOT NULL,
    thought_type ENUM('reasoning','observation','decision','reflection','planning') DEFAULT 'reasoning',
    related_interaction_id INT,
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_thought_user_time (user_id, created_at DESC),
    INDEX idx_thought_type (thought_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS user_activity_heatmap (
    heatmap_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    day_of_week TINYINT NOT NULL,
    hour_of_day TINYINT NOT NULL,
    activity_count INT DEFAULT 0,
    message_count INT DEFAULT 0,
    interaction_count INT DEFAULT 0,
    avg_sentiment FLOAT DEFAULT 0.0,
    period_start DATE,
    period_end DATE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    UNIQUE KEY uk_heatmap (user_id, day_of_week, hour_of_day, period_start),
    INDEX idx_heatmap_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS memory_consolidation_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    consolidation_type ENUM('summarize','merge','prune','archive','reindex') NOT NULL,
    source_count INT DEFAULT 0,
    result_count INT DEFAULT 0,
    affected_users JSON,
    details TEXT,
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_consolidation_type (consolidation_type),
    INDEX idx_consolidation_time (created_at DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS community_sentiment (
    sentiment_id INT AUTO_INCREMENT PRIMARY KEY,
    channel_id VARCHAR(32),
    sentiment ENUM('positive','neutral','negative','mixed') NOT NULL,
    score FLOAT DEFAULT 0.0,
    topic VARCHAR(255),
    sample_size INT DEFAULT 1,
    period_start TIMESTAMP NULL,
    period_end TIMESTAMP NULL,
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_sentiment_period (period_start, period_end),
    INDEX idx_sentiment_channel (channel_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS trending_topics (
    trend_id INT AUTO_INCREMENT PRIMARY KEY,
    topic VARCHAR(255) NOT NULL,
    mention_count INT DEFAULT 1,
    unique_users INT DEFAULT 1,
    avg_sentiment FLOAT DEFAULT 0.0,
    related_keywords JSON,
    first_mentioned TIMESTAMP NULL,
    last_mentioned TIMESTAMP NULL,
    period_start DATE,
    period_end DATE,
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_trend_count (mention_count DESC),
    INDEX idx_trend_period (period_start, period_end)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS community_events (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    event_type ENUM('milestone','achievement','incident','trend','custom') NOT NULL,
    title VARCHAR(512) NOT NULL,
    description TEXT,
    involved_users JSON,
    channel_id VARCHAR(32),
    message_id VARCHAR(32),
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_event_type (event_type),
    INDEX idx_event_time (created_at DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS agent_learnings (
    learning_id INT AUTO_INCREMENT PRIMARY KEY,
    learning_type ENUM('correction','preference','pattern','error','success','insight','rule') NOT NULL,
    title VARCHAR(512) NOT NULL,
    description TEXT,
    related_user_id VARCHAR(255),
    related_skill VARCHAR(128),
    priority ENUM('low','medium','high','critical') DEFAULT 'medium',
    is_active BOOLEAN DEFAULT TRUE,
    applied_count INT DEFAULT 0,
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_learning_type (learning_type),
    INDEX idx_learning_priority (priority),
    INDEX idx_learning_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- PART 2: Upgrade existing tables
-- ============================================

-- users: expand status enum, add new columns
ALTER TABLE users
    MODIFY COLUMN status ENUM('active','inactive','banned','new','away','dnd') DEFAULT 'active',
    ADD COLUMN timezone VARCHAR(64) AFTER status,
    ADD COLUMN roles JSON AFTER timezone,
    ADD COLUMN total_messages INT DEFAULT 0 AFTER roles,
    ADD COLUMN total_reactions INT DEFAULT 0 AFTER total_messages,
    ADD COLUMN total_sessions INT DEFAULT 0 AFTER total_reactions,
    ADD COLUMN last_seen TIMESTAMP NULL AFTER total_sessions,
    ADD INDEX idx_users_last_seen (last_seen);

-- user_interactions: add new columns
ALTER TABLE user_interactions
    ADD COLUMN sentiment_score FLOAT DEFAULT 0.0 AFTER sentiment,
    ADD COLUMN mood_impact FLOAT DEFAULT 0.0 AFTER sentiment_score,
    ADD COLUMN channel_id VARCHAR(32) AFTER mood_impact,
    ADD COLUMN message_id VARCHAR(32) AFTER channel_id,
    ADD COLUMN is_important BOOLEAN DEFAULT FALSE AFTER message_id,
    ADD COLUMN requires_followup BOOLEAN DEFAULT FALSE AFTER is_important,
    ADD COLUMN followup_topic VARCHAR(255) AFTER requires_followup,
    ADD COLUMN followup_due TIMESTAMP NULL AFTER followup_topic,
    ADD COLUMN metadata JSON AFTER followup_due,
    ADD INDEX idx_int_sentiment (sentiment),
    ADD INDEX idx_int_followup (requires_followup, followup_due),
    ADD INDEX idx_int_important (user_id, is_important);

-- user_context: add new columns
ALTER TABLE user_context
    ADD COLUMN context_type ENUM('episodic','semantic','procedural','emotional','preference','fact','custom') DEFAULT 'episodic' AFTER context_value,
    ADD COLUMN importance FLOAT DEFAULT 0.5 AFTER context_type,
    ADD COLUMN source ENUM('conversation','observation','explicit','inferred','system') DEFAULT 'conversation' AFTER importance,
    ADD COLUMN channel_id VARCHAR(32) AFTER source,
    ADD COLUMN message_id VARCHAR(32) AFTER channel_id,
    ADD COLUMN is_active BOOLEAN DEFAULT TRUE AFTER expires_at,
    ADD COLUMN metadata JSON AFTER is_active,
    ADD INDEX idx_ctx_type (context_type),
    ADD INDEX idx_ctx_active (is_active),
    ADD INDEX idx_ctx_importance (importance DESC);

-- user_attributes: expand enum, add new columns
ALTER TABLE user_attributes
    MODIFY COLUMN attribute_type ENUM('like','dislike','hobby','interest','skill','trait','goal','custom') NOT NULL,
    ADD COLUMN confidence FLOAT DEFAULT 1.0 AFTER category,
    ADD COLUMN source ENUM('stated','inferred','observed') DEFAULT 'stated' AFTER confidence,
    ADD COLUMN metadata JSON AFTER source,
    ADD INDEX idx_attr_user_type (user_id, attribute_type);

-- user_media: expand enum, add new columns
ALTER TABLE user_media
    MODIFY COLUMN media_type ENUM('tv_show','movie','book','game','music','podcast','anime','comic','youtube','other') NOT NULL,
    ADD COLUMN status ENUM('completed','in_progress','planned','dropped','on_hold') DEFAULT 'completed' AFTER rating,
    ADD COLUMN progress VARCHAR(64) AFTER status,
    ADD COLUMN review TEXT AFTER progress,
    ADD COLUMN source ENUM('stated','observed','inferred') DEFAULT 'stated' AFTER review,
    ADD COLUMN metadata JSON AFTER source,
    ADD INDEX idx_media_status (status),
    ADD INDEX idx_media_rating (rating);

-- user_food_preferences: expand enum, add new columns
ALTER TABLE user_food_preferences
    MODIFY COLUMN preference ENUM('loves','likes','neutral','dislikes','allergic','hates') NOT NULL,
    ADD COLUMN context VARCHAR(255) AFTER preference,
    ADD COLUMN source ENUM('stated','observed','inferred') DEFAULT 'stated' AFTER context,
    ADD COLUMN metadata JSON AFTER source,
    ADD INDEX idx_food_pref (preference);

-- user_relationships: expand enum, add new columns
ALTER TABLE user_relationships
    MODIFY COLUMN relationship_type ENUM('friend','close_friend','family','colleague','acquaintance','blocked','mentor','mentee','rival','other') NOT NULL DEFAULT 'acquaintance',
    ADD COLUMN trust_level TINYINT DEFAULT 5 AFTER strength,
    ADD COLUMN interaction_frequency ENUM('daily','weekly','monthly','rarely','never') DEFAULT 'weekly' AFTER trust_level,
    ADD COLUMN shared_interests JSON AFTER interaction_frequency,
    ADD INDEX idx_rel_type (relationship_type);

-- skill_usage: add error_type
ALTER TABLE skill_usage
    ADD COLUMN error_type VARCHAR(128) AFTER error_message,
    ADD INDEX idx_skill_error_type (error_type);

-- user_notes: add tags, is_private, source_message_id
ALTER TABLE user_notes
    ADD COLUMN tags JSON AFTER category,
    ADD COLUMN is_private BOOLEAN DEFAULT FALSE AFTER is_pinned,
    ADD COLUMN source_message_id VARCHAR(32) AFTER is_private,
    ADD INDEX idx_notes_private (is_private);

-- topic_keywords: add new columns (keep existing ones)
ALTER TABLE topic_keywords
    ADD COLUMN user_id VARCHAR(255) AFTER keyword,
    ADD COLUMN weight FLOAT DEFAULT 1.0 AFTER user_id,
    ADD COLUMN category VARCHAR(128) AFTER weight,
    ADD COLUMN first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP AFTER category,
    ADD COLUMN last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP AFTER first_seen,
    ADD COLUMN count INT DEFAULT 1 AFTER last_seen,
    ADD COLUMN metadata JSON AFTER count,
    ADD INDEX idx_kw_user (user_id),
    ADD INDEX idx_kw_category (category),
    ADD INDEX idx_kw_weight (weight DESC);

-- ============================================
-- PART 3: Migrate existing data
-- ============================================

-- Migrate user_media: convert old PascalCase enum values to new snake_case
UPDATE user_media SET media_type = 'tv_show' WHERE media_type = 'TV Show';
UPDATE user_media SET media_type = 'movie' WHERE media_type = 'Movie';
UPDATE user_media SET media_type = 'book' WHERE media_type = 'Book';

-- Set default count for existing topic_keywords
UPDATE topic_keywords SET count = 1 WHERE count IS NULL;
