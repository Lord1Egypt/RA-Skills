-- Rename the old "Pending" status to "HumanPending".
-- The Rust FromStr impl keeps a legacy "Pending" arm during the transition,
-- but new rows are always written as "HumanPending".
UPDATE listings SET status = 'HumanPending' WHERE status = 'Pending';
