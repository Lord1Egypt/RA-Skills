# Compliance Mapping

How Guardian Audit satisfies regulatory requirements.

## EU AI Act (2026)

| Requirement | Guardian Audit Feature |
|-------------|------------------------|
| Art. 52(1) — High-risk systems log operation | Every tool call logged |
| Art. 52(2) — Automatic logging | Passive, no agent discretion |
| Art. 52(3) — Logs retained | Append-only, human-rotated |
| Art. 52(4) — Access by competent authorities | NDJSON readable without tooling |

## SOC 2 Type II

| Requirement | Guardian Audit Feature |
|-------------|------------------------|
| CC6.1 — Logical access controls | Every access logged with approver |
| CC7.2 — System operations monitored | Real-time event stream |
| CC7.3 — System changes logged | Guardian_HALT/EXECUTED capture changes |
| A1.2 — Availability monitoring | Outcome field tracks failures |

## HIPAA §164.312(b)

| Requirement | Guardian Audit Feature |
|-------------|------------------------|
| Audit controls | All agent activity logged |
| Mechanisms to examine | `scripts/export-report.py` generates readable reports |
| Activity recording | Who (agent_id), what (operation), when (timestamp), result (outcome) |

## GDPR Article 5(1)(d) — Accuracy

Guardian Audit captures the agent's stated reasoning at decision time, enabling post-hoc verification of whether the agent's justification matched reality.

## NIST AI RMF (2024)

| Function | Mapping |
|----------|---------|
| GOVERN 1.1 | Policy enforcement via Guardian + Audit |
| MAP 1.1 | Context documented in guardian_notes |
| MEASURE 2.1 | Metrics from audit trail: halt rate, approval rate, pattern frequency |
| MANAGE 2.1 | Escalation resolution tracked |
