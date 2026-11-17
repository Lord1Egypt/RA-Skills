# Offline helper contract

Python 3.11+ standard library, no network, writes, credentials or external actions. Resolve paths from the installed skill directory.

```sh
python3 scripts/guard.py assets/example.json
```

Run the command from this skill directory, or resolve both paths absolutely. For real use point to a private input JSON file. Reads only the explicitly supplied file and prints derived JSON; errors go to stderr with exit code 2. No output file is created and the source is unchanged. The included [example](../assets/example.json) is fictional.

Schema 1: now, due, cutoff are explicit-offset ISO timestamps; due < cutoff. event_status is active/cancelled/closed. event_revision and job_revision are positive integers; task_complete and already_sent are explicit booleans. Caller obtains current time/state from the live source immediately before use, not from the example or a stale cached record.

Window is [due, cutoff): exactly due is eligible, exactly cutoff is expired. Inactive event, superseded revision, completed task, recorded sent, expired window and not-yet-due each suppress sending. Exactly one reason is returned, in that precedence. No IANA timezone interpretation or quiet-hours calculation; use the scheduler's verified settings and resolve DST ambiguity before producing these timestamps.

Expected example: superseded, not eligible. Even with matching revision, the delayed job is expired. Eligibility establishes no authority and provides no concurrency/duplicate-send lock: scheduler admission plus an external idempotency/receipt registry is still needed. Two processes can both read already_sent=false; serialize send ownership or reconcile before any retry. Do not claim exactly-once delivery from this helper.
