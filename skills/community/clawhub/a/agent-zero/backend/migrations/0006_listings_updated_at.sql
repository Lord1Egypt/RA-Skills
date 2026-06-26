ALTER TABLE listings ADD COLUMN updated_at TEXT;
UPDATE listings SET updated_at = created_at WHERE updated_at IS NULL;
