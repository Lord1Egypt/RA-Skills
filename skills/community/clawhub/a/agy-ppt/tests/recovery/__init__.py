"""Phase 9 deterministic fault-injection and recovery scenarios.

Every module in this package drives the frozen production control plane
(``scripts/project_state.py``) through a scripted failure using fake workers.
No real Codex, Kiro or ``image_gen`` call is made and no subscription quota is
consumed. Live (quota-consuming) recovery checks live in
``tests/integration/test_recovery_live.py`` and are opt-in only.
"""
