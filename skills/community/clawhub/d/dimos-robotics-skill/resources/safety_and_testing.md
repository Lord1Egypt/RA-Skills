# Safety and Testing Notes for DimOS Skills

Robotics code can affect the physical world. Use this conservative sequence when creating or changing DimOS skills.

## Safety gate

Before a skill moves hardware, confirm:

- The user has selected replay or simulation for the first run.
- The skill has limits for distance, speed, turn angle, and duration where relevant.
- The skill returns a refusal string when inputs exceed those limits.
- The robot can be stopped with `dimos stop` or a local emergency stop.
- The code does not disable obstacle avoidance, collision checks, or emergency stops.
- The area around real hardware is clear and supervised.

## Smoke test

```bash
# 1. Start from a clean environment.
dimos stop || true

# 2. List blueprints and pick a replay/sim agentic one.
dimos list

# 3. Run in replay or simulation.
dimos --replay run unitree-go2-agentic --daemon
# or:
dimos --simulation run unitree-go2-agentic --daemon

# 4. Inspect status.
dimos status
dimos log -n 100

# 5. Verify MCP is serving tools.
dimos mcp status
dimos mcp list-tools

# 6. Call the new skill with harmless arguments.
dimos mcp call safe_relative_move --json-args '{"forward": 0.1, "left": 0.0, "degrees": 0.0}'

# 7. Watch logs for errors.
dimos log -f

# 8. Stop when finished.
dimos stop
```

## Input validation pattern

Prefer explicit validation over silent clamping for robot movement. Returning a refusal gives the agent clear feedback and prevents accidental motion.

```python
if abs(forward) > self.max_forward_m:
    return f"Refused: forward={forward} exceeds limit {self.max_forward_m}."
```

## Logging pattern

Keep result strings short and factual. Use logs for details, not long tool returns. Do not include secrets in logs.
