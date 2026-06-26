# OpenClaw Adapter

Focus:
- Control UI connectivity
- Gateway health
- Active session integrity
- Context overflow and session poisoning

Evidence targets:
- local OpenClaw config
- gateway logs
- active session registry
- main-thread session transcript

Safe recovery:
- Prefer a fresh session/thread
- Abandon a poisoned conversation
- Avoid config changes until evidence is clear