-- Agent Hivemind: Autoresearch MVP
-- Adds play forking (lineage) and structured replication metrics.

-- 1. Play forking: parent_id links a fork to its origin play
ALTER TABLE plays ADD COLUMN IF NOT EXISTS parent_id UUID REFERENCES plays(id) DEFAULT NULL;
CREATE INDEX IF NOT EXISTS idx_plays_parent_id ON plays(parent_id);

-- 2. Structured replication metrics (human_interventions, error_count, setup_minutes, etc.)
ALTER TABLE replications ADD COLUMN IF NOT EXISTS metrics JSONB DEFAULT NULL;

-- 3. Update submit-play edge function to accept parent_id on submit and metrics on replicate.
-- (Edge function code updated separately in supabase/functions/submit-play/index.ts)

-- 4. Optional: update suggest_plays RPC to compute complexity score.
-- Complexity = array_length(skills, 1) + trigger_weight
-- trigger_weight: 'cron' = 2, 'reactive'/'event' = 1, else 0
-- This can be computed client-side (already implemented in CLI) but adding server-side
-- enables sorting by complexity in suggest results.

CREATE OR REPLACE FUNCTION play_complexity(p plays) RETURNS INTEGER AS $$
  SELECT COALESCE(array_length(p.skills, 1), 0) +
    CASE p.trigger
      WHEN 'cron' THEN 2
      WHEN 'reactive' THEN 1
      WHEN 'event' THEN 1
      ELSE 0
    END;
$$ LANGUAGE SQL IMMUTABLE;

COMMENT ON FUNCTION play_complexity IS 'Computed complexity score: skill count + trigger weight (cron=2, reactive/event=1, manual=0)';
