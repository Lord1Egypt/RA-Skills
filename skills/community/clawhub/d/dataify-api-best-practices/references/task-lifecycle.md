# Task lifecycle

The default contract is submit once → persist ID → wait with a deadline → download after success → validate final records. Poll status reads with bounded backoff. On a local timeout, return the same task ID and an exact resume command; do not cancel or resubmit. On terminal failure, include category, remote message, and safe next action.
