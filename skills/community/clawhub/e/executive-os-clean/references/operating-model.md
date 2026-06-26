# Operating Model

Goal: turn inbound signals into a clean action queue.

Canonical flow:
1. ingest signals
2. classify by People and Programs
3. assign Priority and Action State
4. produce a digest
5. propose replies when useful
6. never contact third parties without explicit approval

Supported source families:
- email
- chat and messaging
- local notes and meeting docs

Priority:
- `P1` urgent now
- `P2` important
- `P3` useful but not urgent
- `P4` low signal or noise

Action state:
- `reply`
- `decide`
- `follow-up`
- `wait`
- `ignore`
- `watch`

Digest sections:
- urgent now
- needs reply
- decisions pending
- follow-ups slipping
- important but not urgent
- FYI / low signal
- source gaps
