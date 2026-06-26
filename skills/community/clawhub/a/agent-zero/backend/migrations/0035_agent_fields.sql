-- Add agent_comment column for storing the agent's triage reasoning.
ALTER TABLE listings ADD COLUMN agent_comment TEXT;

-- Make search_profile_id nullable: listings start with NULL while in
-- PendingAgentReview state; the agent assigns the profile on review.
-- The NOT NULL constraint was enforced via triggers (see 0031_rename_search_id.sql).
DROP TRIGGER IF EXISTS listings_search_criteria_id_notnull_insert;
DROP TRIGGER IF EXISTS listings_search_criteria_id_notnull_update;
