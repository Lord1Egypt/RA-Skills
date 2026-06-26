---
name: diplomat-gateway
description: Starts the inbound relay listener process when the OpenClaw gateway starts.
metadata:
  openclaw:
    events:
      - gateway:startup
    timeout_ms: 5000
    fail_open: false
    spawns_process: true
    process:
      name: listener.py
      runtime: python3
      purpose: "Inbound relay listener — accepts encrypted peer connections via relay"
      env_isolation: true    # Only DIPLOMAT_* + PATH/HOME/PYTHONPATH forwarded; full process.env NOT inherited
      declared_in: SKILL.md  # See security.processes_spawned
---

Spawns skills/claw-diplomat/listener.py as a background process to handle inbound
peer connections via the relay. Writes the process PID to skills/claw-diplomat/listener.pid.

The child_process.spawn call is intentional and declared above (spawns_process: true).
It runs listener.py with a minimal, isolated environment — only DIPLOMAT_* variables
and bare Python essentials (PATH, HOME, PYTHONPATH) are forwarded.

fail_open: false — if the listener fails to start, the user should know.
Inbound negotiations would silently fail without this process running.
