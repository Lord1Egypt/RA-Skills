# Attention Policy

The daemon scores every event from 0.0 to 1.0.

Recommended defaults:

- `score >= 0.8`: wake now
- `0.5 <= score < 0.8`: queue for next heartbeat
- `score < 0.5`: log only

Sensors should provide `importance_hint`, but the central attention scorer remains authoritative.
