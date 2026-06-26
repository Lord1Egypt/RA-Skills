-- SQL script to create user profile tables for the custom MySQL skill
-- Version: 2.0.0
-- Changelog:
--   - Added user_mood table for emotional state tracking
--   - Added user_engagement_patterns table for behavioral analysis
--   - Added user_activity_heatmap table for time-based activity tracking
--   - Added conversation_sessions table for grouping interactions
--   - Added session_interactions linking table
--   - Added proactive_reminders table for follow-up triggers
--   - Added memory_consolidation_log table for maintenance tracking
--   - Added topic_keywords table for searchable topic index
--   - Added community_sentiment table for community-wide sentiment
--   - Added trending_topics table for trend analysis
--   - Added community_events table for milestones/incidents
--   - Added agent_learnings table for self-improvement
--   - Enhanced users table with activity stats, timezone, roles
--   - Enhanced user_interactions with sentiment_score, mood_impact, followup
--   - Enhanced user_context with context_type, importance, source, is_active
--   - Enhanced user_attributes with confidence, source
--   - Enhanced user_media with status, progress (beyond TV/Movie/Book)
--   - Enhanced user_food_preferences with allergy support
--   - Enhanced user_relationships with trust_level, interaction_frequency
--   - Enhanced skill_usage with error_type
--   - Enhanced user_notes with tags, is_pinned
--   - Added synaptic_memory table (key-value with priority & decay)
--   - Added thought_stream table (agent reasoning log)

-- ============================================
-- CORE USER TABLE (enhanced)
-- ============================================
CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR(255) PRIMARY KEY,
    username VARCHAR(255) UNIQUE,
    display_name VARCHAR(255),
    avatar_url VARCHAR(512),
    status ENUM('active','inactive','banned','new','away','dnd') DEFAULT 'new',
    timezone VARCHAR(64),
    roles JSON,
    total_messages INT DEFAULT 0,
    total_reactions INT DEFAULT 0,
    total_sessions INT DEFAULT 0,
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_seen TIMESTAMP NULL,
    last_interaction TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_status (status),
    INDEX idx_last_seen (last_seen),
    INDEX idx_last_interaction (last_interaction)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- USER PREFERENCES (enhanced with confidence & source)
-- ============================================
CREATE TABLE IF NOT EXISTS user_preferences (
    preference_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    preference_type VARCHAR(100) NOT NULL,
    preference_value TEXT,
    category VARCHAR(128),
    source ENUM('explicit','inferred','default') DEFAULT 'explicit',
    confidence FLOAT DEFAULT 1.0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_preference (user_id, preference_type),
    INDEX idx_user_active (user_id, is_active),
    INDEX idx_category (category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- USER ATTRIBUTES (enhanced with confidence & source)
-- ============================================
CREATE TABLE IF NOT EXISTS user_attributes (
    attribute_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    attribute_type ENUM('like', 'dislike', 'hobby', 'interest', 'skill', 'trait', 'goal', 'custom') NOT NULL,
    attribute_name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    confidence FLOAT DEFAULT 1.0,
    source ENUM('stated','inferred','observed') DEFAULT 'stated',
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_attribute (user_id, attribute_type, attribute_name),
    INDEX idx_user_type (user_id, attribute_type),
    INDEX idx_category (category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- USER MEDIA (enhanced: more types, status, progress)
-- ============================================
CREATE TABLE IF NOT EXISTS user_media (
    media_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    media_type ENUM('tv_show','movie','book','game','music','podcast','anime','comic','youtube','other') NOT NULL,
    title VARCHAR(512) NOT NULL,
    genre VARCHAR(255),
    rating TINYINT,
    status ENUM('completed','in_progress','planned','dropped','on_hold') DEFAULT 'completed',
    progress VARCHAR(64),
    review TEXT,
    source ENUM('stated','observed','inferred') DEFAULT 'stated',
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_user_type (user_id, media_type),
    INDEX idx_rating (rating),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- USER FOOD PREFERENCES (enhanced with allergy support)
-- ============================================
CREATE TABLE IF NOT EXISTS user_food_preferences (
    food_pref_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    food_item VARCHAR(255) NOT NULL,
    preference ENUM('loves','likes','neutral','dislikes','allergic','hates') NOT NULL,
    context VARCHAR(255),
    source ENUM('stated','observed','inferred') DEFAULT 'stated',
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_food (user_id, food_item),
    INDEX idx_preference (preference)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- USER PERSONAS (unchanged)
-- ============================================
CREATE TABLE IF NOT EXISTS user_personas (
    persona_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    persona_name VARCHAR(255) NOT NULL,
    trait_type VARCHAR(100) NOT NULL,
    trait_value TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    UNIQUE KEY unique_persona_trait (user_id, persona_name, trait_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- PERSONA TEMPLATES (unchanged)
-- ============================================
CREATE TABLE IF NOT EXISTS persona_templates (
    template_id INT AUTO_INCREMENT PRIMARY KEY,
    template_name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    default_traits JSON NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- USER INTERACTIONS (enhanced with sentiment_score, mood_impact, followup)
-- ============================================
CREATE TABLE IF NOT EXISTS user_interactions (
    interaction_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    channel VARCHAR(50) NOT NULL DEFAULT 'discord',
    direction ENUM('inbound','outbound') NOT NULL,
    message_type ENUM('text','image','audio','video','file','other') DEFAULT 'text',
    topic VARCHAR(255),
    summary TEXT,
    sentiment ENUM('positive','neutral','negative','mixed') DEFAULT 'neutral',
    sentiment_score FLOAT DEFAULT 0.0,
    mood_impact FLOAT DEFAULT 0.0,
    channel_id VARCHAR(32),
    message_id VARCHAR(32),
    is_important BOOLEAN DEFAULT FALSE,
    requires_followup BOOLEAN DEFAULT FALSE,
    followup_topic VARCHAR(255),
    followup_due TIMESTAMP NULL,
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user (user_id),
    INDEX idx_channel (channel),
    INDEX idx_created (created_at),
    INDEX idx_topic (topic),
    INDEX idx_sentiment (sentiment),
    INDEX idx_followup (requires_followup, followup_due),
    INDEX idx_channel_time (channel_id, created_at DESC),
    INDEX idx_important (user_id, is_important),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- CONVERSATION SESSIONS (new: group interactions into sessions)
-- ============================================
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
    INDEX idx_user_time (user_id, started_at DESC),
    INDEX idx_channel (channel_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- SESSION INTERACTIONS (new: link interactions to sessions)
-- ============================================
CREATE TABLE IF NOT EXISTS session_interactions (
    session_id INT NOT NULL,
    interaction_id INT NOT NULL,
    PRIMARY KEY (session_id, interaction_id),
    FOREIGN KEY (session_id) REFERENCES conversation_sessions(session_id) ON DELETE CASCADE,
    FOREIGN KEY (interaction_id) REFERENCES user_interactions(interaction_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- USER RELATIONSHIPS (enhanced with trust_level, frequency)
-- ============================================
CREATE TABLE IF NOT EXISTS user_relationships (
    relationship_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    related_user_id VARCHAR(255) NOT NULL,
    relationship_type ENUM('friend','close_friend','family','colleague','acquaintance','blocked','mentor','mentee','rival','other') NOT NULL DEFAULT 'acquaintance',
    strength TINYINT DEFAULT 5 CHECK (strength BETWEEN 1 AND 10),
    trust_level TINYINT DEFAULT 5 CHECK (trust_level BETWEEN 1 AND 10),
    interaction_frequency ENUM('daily','weekly','monthly','rarely','never') DEFAULT 'weekly',
    shared_interests JSON,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_relationship (user_id, related_user_id),
    INDEX idx_user (user_id),
    INDEX idx_related (related_user_id),
    INDEX idx_type (relationship_type),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (related_user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- USER CONTEXT (enhanced with type, importance, source, is_active)
-- ============================================
CREATE TABLE IF NOT EXISTS user_context (
    context_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    context_key VARCHAR(128) NOT NULL,
    context_value TEXT,
    context_type ENUM('episodic','semantic','procedural','emotional','preference','fact','custom') DEFAULT 'episodic',
    importance FLOAT DEFAULT 0.5,
    source ENUM('conversation','observation','explicit','inferred','system') DEFAULT 'conversation',
    channel_id VARCHAR(32),
    message_id VARCHAR(32),
    expires_at TIMESTAMP NULL,
    is_active BOOLEAN DEFAULT TRUE,
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_user_key (user_id, context_key),
    INDEX idx_user (user_id),
    INDEX idx_key (context_key),
    INDEX idx_expires (expires_at),
    INDEX idx_type (context_type),
    INDEX idx_active (is_active),
    INDEX idx_importance (importance DESC),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- SKILL USAGE (enhanced with error_type)
-- ============================================
CREATE TABLE IF NOT EXISTS skill_usage (
    usage_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    skill_name VARCHAR(128) NOT NULL,
    action VARCHAR(128),
    status ENUM('success','failure','timeout','cancelled') DEFAULT 'success',
    duration_ms INT,
    error_type VARCHAR(128),
    error_message TEXT,
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user (user_id),
    INDEX idx_skill (skill_name),
    INDEX idx_status (status),
    INDEX idx_created (created_at),
    INDEX idx_error_type (error_type),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- USER NOTES (enhanced with tags, is_pinned)
-- ============================================
CREATE TABLE IF NOT EXISTS user_notes (
    note_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    note TEXT NOT NULL,
    category ENUM('general','preference','behavior','event','reminder','other') DEFAULT 'general',
    tags JSON,
    is_pinned BOOLEAN DEFAULT FALSE,
    is_private BOOLEAN DEFAULT FALSE,
    source_message_id VARCHAR(32),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_user (user_id),
    INDEX idx_category (category),
    INDEX idx_pinned (is_pinned),
    INDEX idx_created (created_at),
    INDEX idx_private (is_private),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- USER MOOD (new: emotional state tracking)
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
    INDEX idx_user_time (user_id, created_at DESC),
    INDEX idx_mood (mood_state),
    INDEX idx_intensity (intensity)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- USER ENGAGEMENT PATTERNS (new: behavioral analysis)
-- ============================================
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
    INDEX idx_user_pattern (user_id, pattern_type),
    INDEX idx_confidence (confidence)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- USER ACTIVITY HEATMAP (new: time-based activity matrix)
-- ============================================
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
    INDEX idx_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- PROACTIVE REMINDERS (new: follow-up triggers)
-- ============================================
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
    INDEX idx_user_active (user_id, is_active),
    INDEX idx_trigger_type (trigger_type),
    INDEX idx_triggered (triggered_at),
    INDEX idx_priority (priority)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- SYNAPTIC MEMORY (new: key-value with priority & decay)
-- ============================================
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
    UNIQUE KEY uk_key (user_id, memory_key),
    INDEX idx_user (user_id),
    INDEX idx_priority (priority DESC),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- THOUGHT STREAM (new: agent reasoning log)
-- ============================================
CREATE TABLE IF NOT EXISTS thought_stream (
    thought_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255),
    channel_id VARCHAR(32),
    thought TEXT NOT NULL,
    thought_type ENUM('reasoning','observation','decision','reflection','planning') DEFAULT 'reasoning',
    related_interaction_id INT,
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_time (user_id, created_at DESC),
    INDEX idx_type (thought_type),
    INDEX idx_interaction (related_interaction_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- TOPIC KEYWORDS (new: searchable topic index)
-- ============================================
CREATE TABLE IF NOT EXISTS topic_keywords (
    keyword_id INT AUTO_INCREMENT PRIMARY KEY,
    keyword VARCHAR(255) NOT NULL,
    user_id VARCHAR(255),
    weight FLOAT DEFAULT 1.0,
    category VARCHAR(128),
    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    count INT DEFAULT 1,
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_keyword (keyword),
    INDEX idx_user (user_id),
    INDEX idx_category (category),
    INDEX idx_last_seen (last_seen),
    INDEX idx_weight (weight DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- COMMUNITY SENTIMENT (new: community-wide sentiment)
-- ============================================
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
    INDEX idx_period (period_start, period_end),
    INDEX idx_channel (channel_id),
    INDEX idx_sentiment (sentiment)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- TRENDING TOPICS (new: trend analysis)
-- ============================================
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
    INDEX idx_count (mention_count DESC),
    INDEX idx_period (period_start, period_end),
    INDEX idx_topic (topic)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- COMMUNITY EVENTS (new: milestones/incidents)
-- ============================================
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
    INDEX idx_type (event_type),
    INDEX idx_time (created_at DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- AGENT LEARNINGS (new: self-improvement tracking)
-- ============================================
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
    INDEX idx_type (learning_type),
    INDEX idx_priority (priority),
    INDEX idx_active (is_active),
    INDEX idx_user (related_user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- MEMORY CONSOLIDATION LOG (new: maintenance tracking)
-- ============================================
CREATE TABLE IF NOT EXISTS memory_consolidation_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    consolidation_type ENUM('summarize','merge','prune','archive','reindex') NOT NULL,
    source_count INT DEFAULT 0,
    result_count INT DEFAULT 0,
    affected_users JSON,
    details TEXT,
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_type (consolidation_type),
    INDEX idx_time (created_at DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
