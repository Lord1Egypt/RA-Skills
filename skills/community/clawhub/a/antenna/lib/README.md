# Companion libraries

The installable allowlist retains local list metadata, signature/key helpers,
Registry contracts, session-policy validation and native backup dependencies.
The native backup adapter reuses identity/reference validation from
`antenna_state.py` and `session_policy.py`; these shared readers do not register
or restore a relay. The native backup rejects legacy transport snapshots.
Legacy setup, roster writers, configuration shell writers, policy restoration,
relay dispatch and model-admin helpers remain source-only, not installed.

The shared session-policy helper is read-only: legacy `mutate`, `initialize`,
`stage-queue` and session-administration entry points refuse without executing jq
or writing state. Native recovery and Registry readers retain their validators.
