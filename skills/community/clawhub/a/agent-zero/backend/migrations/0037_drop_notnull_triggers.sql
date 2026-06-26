-- Drop NOT NULL triggers on search_profile_id.
-- These were added in 0032_rename_search_profile.sql but conflict with the
-- agent-suggest workflow introduced in 0035_agent_fields.sql, which intentionally
-- inserts listings with NULL search_profile_id (status=AgentPending) and lets
-- the Claude agent assign the profile asynchronously.
-- Migration 0035 dropped these triggers from backend/listings.db but the
-- database/listings.db copy still has them active.
DROP TRIGGER IF EXISTS listings_search_profile_id_notnull_insert;
DROP TRIGGER IF EXISTS listings_search_profile_id_notnull_update;
