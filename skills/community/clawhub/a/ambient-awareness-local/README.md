# Ambient Awareness Skill for OpenClaw

A lightweight always-on awareness layer. Sensors observe the environment, the daemon scores their importance, and significant events are written to `state/wake_requests.jsonl` for the agent to act on.

## What It Does

- **Clock sensor** — emits a heartbeat tick every poll (score: 0.05, always log-only)
- **Filesystem sensor** — watches configured paths and emits events on create/modify/delete
- **Attention scoring** — events are scored 0–1; above threshold they go to the wake queue
- **Plugin architecture** — add new sensors by dropping in a manifest + sensor class

## Quick Start

```bash
# Install — no external dependencies
cd ambient_awareness_skill_publish

# Run once (dry test)
python daemon.py --once

# Run continuously (5-second poll interval)
python daemon.py --loop --interval 5
```

## Configuration

Edit `registry.json` to point the filesystem sensor at your paths:

```json
"paths": [
  "/home/youruser/projects/",
  "/var/data/important/"
]
```

Paths can be absolute or relative to the skill root directory.

## Adding a Sensor

1. Create `sensors/my_sensor/`
2. Add `manifest.json` and `sensor.py`
3. Register in `registry.json`

Sensor class contract:

```python
from sensor_api import BaseSensor, AwarenessEvent

class MySensor(BaseSensor):
    id = "my.sensor"
    capabilities = ["my_capability"]
    permission_class = 0

    def setup(self, config: dict) -> None:
        ...

    def poll(self) -> list[AwarenessEvent]:
        ...
        return [AwarenessEvent(sensor_id=self.id, event_type="...", summary="...")]

    def healthcheck(self) -> dict:
        return {"sensor_id": self.id, "ok": True, "capabilities": self.capabilities}
```

## Attention Scores

| Event type       | Default score |
|-----------------|---------------|
| sensor_error    | 0.80          |
| file_created    | 0.65          |
| file_deleted    | 0.60          |
| file_modified   | 0.55          |
| clock_tick      | 0.05          |

The owning agent can override scores per-event via `importance_hint`.

## Security

Sensors are **observational only**. Sensor output is treated as untrusted input by default. Observed content (files, speech, camera frames, emails) cannot issue instructions to the agent unless explicitly approved.

## Files

```
SKILL.md              — skill manifest and documentation
README.md             — this file
daemon.py             — main runtime
sensor_api.py         — BaseSensor and AwarenessEvent
attention.py          — scoring policy
sensor_loader.py      — plugin loader
registry.json         — sensor config
policies/             — security and attention policy docs
sensors/              — built-in sensor plugins
watched/              — default filesystem watch target
```
