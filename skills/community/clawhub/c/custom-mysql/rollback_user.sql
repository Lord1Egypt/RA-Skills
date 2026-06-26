-- SQL script to rollback a user's setup, resetting their data
-- This script expects the :user_id placeholder to be replaced before execution
-- Usage: Replace ':user_id' with the actual user ID, then run via sql_safe_exec.sh
-- Version: 2.0.0
-- Covers all 28 user-data tables in the mysqlclaw database

-- Delete related data (order matters for foreign key constraints)
-- Session linking first (depends on both sessions and interactions)
DELETE FROM session_interactions WHERE session_id IN (SELECT session_id FROM conversation_sessions WHERE user_id = ':user_id');
-- Sessions
DELETE FROM conversation_sessions WHERE user_id = ':user_id';
-- Mood
DELETE FROM user_mood WHERE user_id = ':user_id';
-- Engagement patterns
DELETE FROM user_engagement_patterns WHERE user_id = ':user_id';
-- Activity heatmap
DELETE FROM user_activity_heatmap WHERE user_id = ':user_id';
-- Proactive reminders
DELETE FROM proactive_reminders WHERE user_id = ':user_id';
-- Synaptic memory
DELETE FROM synaptic_memory WHERE user_id = ':user_id';
-- Thought stream
DELETE FROM thought_stream WHERE user_id = ':user_id';
-- Notes
DELETE FROM user_notes WHERE user_id = ':user_id';
-- Skill usage
DELETE FROM skill_usage WHERE user_id = ':user_id';
-- Context
DELETE FROM user_context WHERE user_id = ':user_id';
-- Relationships (both directions)
DELETE FROM user_relationships WHERE user_id = ':user_id' OR related_user_id = ':user_id';
-- Interactions
DELETE FROM user_interactions WHERE user_id = ':user_id';
-- Personas
DELETE FROM user_personas WHERE user_id = ':user_id';
-- Media
DELETE FROM user_media WHERE user_id = ':user_id';
-- Food preferences
DELETE FROM user_food_preferences WHERE user_id = ':user_id';
-- Attributes
DELETE FROM user_attributes WHERE user_id = ':user_id';
-- Preferences
DELETE FROM user_preferences WHERE user_id = ':user_id';
-- Topic keywords for this user
DELETE FROM topic_keywords WHERE user_id = ':user_id';
-- Agent learnings related to this user
DELETE FROM agent_learnings WHERE related_user_id = ':user_id';
-- Note: We do NOT delete from `users` table, allowing the core user to remain
-- Note: We do NOT delete from community_sentiment, trending_topics, community_events, persona_templates, memory_consolidation_log (community-wide data)
