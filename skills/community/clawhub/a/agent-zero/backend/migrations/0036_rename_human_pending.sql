-- Rename "HumanPending" status to "HumanReview".
UPDATE listings SET status = 'HumanReview' WHERE status = 'HumanPending';
