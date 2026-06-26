-- Backfill any NULL status values to 'Interested'.
-- The application now enforces status is always set; this handles legacy rows.
UPDATE listings SET status = 'Interested' WHERE status IS NULL;
