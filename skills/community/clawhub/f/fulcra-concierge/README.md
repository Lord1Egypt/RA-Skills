# concierge-wrapper

The **orchestrator**. Ties the other eight skills together: a status check (what's installed and authenticated), the morning sequence (check-in → briefing), the evening sequence (debrief → weekly cadence), and a day-of routing table so your agent knows which skill to reach for.

- **Reads/writes:** nothing of its own — it routes to the other skills
- **Prerequisites:** Fulcra account; whatever the skills it routes to require (e.g. `ATTIO_API_KEY` for the CRM/event/restaurant skills)
- **Install the other skills too** for the full experience.

## Use

Ask your agent ("start my day", "status check"). Or run the status script directly:

```
uv run --python 3.12 scripts/status.py --help
```

Needs the shared `/lib` (auto-resolved by `concierge_bootstrap.py`). See `SKILL.md` for the routing logic and sequences.
