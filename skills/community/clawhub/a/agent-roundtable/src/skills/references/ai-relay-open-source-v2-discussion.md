# AI Relay Open-Source Readiness Discussion (v2)

## Metadata
- **Discussion ID**: rt_xxxxxxxx
- **Date**: 2026-05-23
- **Rounds**: 3
- **Participants**: bingge (Product Director), pixiel (Designer), mafei (Dev Engineer)
- **Pattern**: Hybrid workflow (delegate_task for reasoning + Direct Core API for recording)

## Key Pattern: roundtable_init Tool Import Failure

The `roundtable_init` tool call failed with `ModuleNotFoundError: No module named 'hermes_tools'`. This is because the tool layer's import chain (`roundtable_tools.py` → `hermes_tools`) breaks when invoked via direct Python. The Direct Core API path (`_get_core()`) works fine because it only imports from the installed `roundtable` package.

**Lesson**: Don't waste time debugging `roundtable_init` import errors. Go straight to Direct Core API via `core = _get_core(); core.create_discussion(...)`.

## Workflow Used

1. `core.create_discussion()` — created discussion + WebViewer
2. `open "{web_url}"` — manually opened browser (Direct Core API doesn't auto-open)
3. `core.speak(participant="coordinator")` — Round 0 opening
4. For each participant × each round:
   - `delegate_task(goal=..., toolsets=["roundtable"])` — generate speech content
   - Extract speech from sub-agent summary (tool_trace always empty)
   - `core.speak(participant="{name}", content="{speech}")` — record reliably
5. `send_message()` — Round 1 summary to company group
6. `write_file()` — Conclusion document saved to project docs
7. `core.end_discussion()` — Conclude with brief text

## Discussion Outcome

### P0 — Must complete before open-source release (5/28)
| Task | Owner | Time |
|------|-------|------|
| Security scan + secret cleanup | mafei | 0.5d |
| License compliance check | mafei | 0.5d |
| CI/CD pipeline | mafei | 1d |
| Local build script verification | mafei | 0.5d |
| README + Quick Start optimization | bingge | 0.5d |
| Visual baseline (Logo + layout) | pixiel | 0.5d |
| Issue/PR templates | bingge | 0.5d |

### P1 — Within 1 week after release
- CONTRIBUTING.md, screenshots/GIF, social share image, CODE_OF_CONDUCT.md, SECURITY.md

### Release Timeline
- 5/26: Confirm assignments, start security scan
- 5/28: Code Freeze, P0 complete
- **5/29: Official release v0.1.0**

## Kanban Task Distribution

4 tasks created and dispatched via kanban three-step pattern:
- `t_xxxxxxxx` — mafei: Security + License (P0)
- `t_xxxxxxxx` — mafei: CI/CD + build scripts (P0)
- `t_xxxxxxxx` — bingge: README + templates (P0)
- `t_xxxxxxxx` — pixiel: Logo + visual baseline (P0)

All subscribed to company group notifications. All picked up by Gateway Dispatcher within seconds.
