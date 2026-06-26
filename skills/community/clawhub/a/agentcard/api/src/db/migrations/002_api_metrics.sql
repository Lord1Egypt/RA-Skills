-- ASG Card — Migration 002: API Metrics (observability)
-- Non-blocking, append-only event log for rollout monitoring
-- Created: 2026-02-27

CREATE TABLE IF NOT EXISTS api_metrics (
  id          BIGSERIAL PRIMARY KEY,
  event_type  TEXT NOT NULL,
  latency_ms  INTEGER,
  source      TEXT,             -- e.g. '4payments' for webhook source identification
  metadata    JSONB DEFAULT '{}',
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Fast aggregation queries for /ops/metrics
CREATE INDEX idx_metrics_type_time ON api_metrics (event_type, created_at DESC);
CREATE INDEX idx_metrics_created   ON api_metrics (created_at DESC);
