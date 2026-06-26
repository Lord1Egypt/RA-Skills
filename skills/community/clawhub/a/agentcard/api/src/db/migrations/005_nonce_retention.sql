-- Migration 005: Nonce retention TTL cleanup
-- Prevents agent_nonces from growing indefinitely.
-- Deletes nonces older than retention window (default 24h) in safe batches.

-- Function: cleanup_expired_nonces(retention_hours, batch_size)
CREATE OR REPLACE FUNCTION cleanup_expired_nonces(
    retention_hours INT DEFAULT 24,
    batch_limit INT DEFAULT 10000
)
RETURNS TABLE(deleted_count BIGINT) AS $$
BEGIN
    RETURN QUERY
    WITH expired AS (
        SELECT nonce
        FROM agent_nonces
        WHERE created_at < now() - (retention_hours || ' hours')::INTERVAL
        ORDER BY created_at ASC
        LIMIT batch_limit
        FOR UPDATE SKIP LOCKED
    ),
    deleted AS (
        DELETE FROM agent_nonces
        WHERE nonce IN (SELECT nonce FROM expired)
        RETURNING 1
    )
    SELECT COUNT(*)::BIGINT AS deleted_count FROM deleted;
END;
$$ LANGUAGE plpgsql;

-- Optional: pg_cron schedule (requires pg_cron extension, run manually if unavailable)
-- SELECT cron.schedule('nonce-cleanup', '0 * * * *', $$SELECT cleanup_expired_nonces(24, 10000)$$);

COMMENT ON FUNCTION cleanup_expired_nonces IS
    'Batch-deletes expired agent nonces. Safe for concurrent use (SKIP LOCKED). '
    'Call via /ops/nonce-cleanup or pg_cron.';
