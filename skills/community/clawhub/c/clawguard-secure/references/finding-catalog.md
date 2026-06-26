# Look up rule definitions

Lookup table for rule IDs. Load when explaining specific findings.

---

## Gateway Security

| Rule | Severity | Title |
|------|----------|-------|
| OC-001 | CRITICAL | Non-loopback gateway binding with missing or disabled authentication |
| OC-002 | CRITICAL | Authentication disabled with HTTP endpoints exposed |
| OC-003 | CRITICAL | Tailscale Funnel mode exposes gateway to public internet |
| OC-004 | CRITICAL | Control UI missing allowedOrigins on non-loopback deployment |
| OC-005 | CRITICAL | Device authentication disabled for Control UI |
| OC-006 | HIGH | Host header origin fallback enabled, bypassing origin checks |
| OC-007 | HIGH | Real IP fallback enabled, allowing client IP spoofing |
| OC-101 | HIGH | Insecure authentication compatibility flag enabled for Control UI |
| OC-107 | MEDIUM | Gateway authentication configured without brute-force rate limiting |
| OC-108 | MEDIUM | Trusted proxy mode missing user identity header or allowlist |

## Channel Access Control

| Rule | Severity | Title |
|------|----------|-------|
| OC-008 | HIGH | DM channel policy set to open, allowing unrestricted direct messages |
| OC-009 | HIGH | Group channel policy set to open, allowing unrestricted group access |
| OC-010 | MEDIUM | Mention gating disabled on shared or external group channels |

## Tool Permissions

| Rule | Severity | Title |
|------|----------|-------|
| OC-011 | CRITICAL | Exec tool security mode missing or not set to deny/allowlist |
| OC-012 | CRITICAL | Elevated tools enabled with unrestricted or wildcard allowFrom |
| OC-013 | HIGH | Filesystem tools not restricted to workspace directory |
| OC-014 | HIGH | apply_patch not restricted to workspace directory |
| OC-105 | MEDIUM | Safe-bins interpreters lack execution profiling |

## Hooks & External Content

| Rule | Severity | Title |
|------|----------|-------|
| OC-015 | HIGH | Unsafe external content bypass enabled in hooks |

## Hooks & Automation

| Rule | Severity | Title |
|------|----------|-------|
| OC-048 | MEDIUM | Hooks enabled but defaultSessionKey is missing |
| OC-049 | MEDIUM | Hooks token has insufficient length or entropy |
| OC-050 | HIGH | Hooks allow callers to override session key, enabling session hijacking |
| OC-051 | HIGH | Session key override enabled without allowed prefix list |
| OC-102 | MEDIUM | Hooks token reuses gateway auth token (same-instance credential reuse) |
| OC-103 | MEDIUM | Hooks allowed agent IDs unrestricted (missing, empty, or wildcard) |

## Secret Management

| Rule | Severity | Title |
|------|----------|-------|
| OC-016 | HIGH | Plaintext secrets or API tokens found in configuration files |
| OC-017 | HIGH | Secrets audit reports plaintext residue or unresolved references |

## Logging & Audit

| Rule | Severity | Title |
|------|----------|-------|
| OC-018 | MEDIUM | Sensitive data redaction disabled in logging |
| OC-019 | HIGH | Command logger not enabled, no command audit trail |

## Local State Security

| Rule | Severity | Title |
|------|----------|-------|
| OC-020 | CRITICAL | OpenClaw state directory is group or world writable |
| OC-021 | CRITICAL | OpenClaw config file is group or world writable |
| OC-022 | CRITICAL | Credential and config files are group or world readable |
| OC-113 | MEDIUM | OpenClaw state directory is inside a cloud-synced folder |

## Plugin Intake

| Rule | Severity | Title |
|------|----------|-------|
| OC-023 | HIGH | Plugin allowlist missing or overly permissive |
| OC-024 | HIGH | Plugin/hook npm packages not version-pinned or missing integrity hashes |

## Browser Security

| Rule | Severity | Title |
|------|----------|-------|
| OC-025 | HIGH | SSRF protection disabled, allowing private network access from browser |
| OC-029 | HIGH | Browser sandbox on bridge network without CDP source restriction |
| OC-052 | HIGH | Remote browser routing exposed beyond private network |
| OC-053 | HIGH | Agent using host browser profile instead of dedicated profile |
| OC-054 | MEDIUM | Agent browser profile has sync or password manager enabled |
| OC-112 | CRITICAL | Browser control endpoint lacks authentication |

## Sandboxing & Isolation

| Rule | Severity | Title |
|------|----------|-------|
| OC-026 | MEDIUM | Sandbox mode disabled despite Docker/browser sandbox config present |
| OC-027 | HIGH | Exec routed to sandbox but sandbox mode is off, causing silent host execution |
| OC-028 | CRITICAL | Docker sandbox using host network or container namespace join |
| OC-030 | HIGH | Sandbox browser host control enabled, allowing sandbox escape |
| OC-031 | HIGH | Dangerous bind mount exposes reserved system paths |
| OC-032 | HIGH | Secret-containing bind mount is mounted read-write |
| OC-033 | HIGH | Agent workspace root is too broad |
| OC-111 | CRITICAL | Docker sandbox running without seccomp or AppArmor confinement |

## Exposure Combinations

| Rule | Severity | Title |
|------|----------|-------|
| OC-034 | CRITICAL | Open groups can reach runtime/filesystem tools without sandbox or workspaceOnly |
| OC-035 | CRITICAL | Open groups can reach elevated tools |

## Tool Policy Hygiene

| Rule | Severity | Title |
|------|----------|-------|
| OC-036 | MEDIUM | Global tools.profile is minimal but overridden by per-agent profile |
| OC-037 | MEDIUM | Extension plugin tools reachable by untrusted agents |
| OC-109 | MEDIUM | Automatic skill whitelisting enabled without manual review |
| OC-110 | MEDIUM | safeBins references binaries in mutable directories |

## Control Plane Tools

| Rule | Severity | Title |
|------|----------|-------|
| OC-038 | HIGH | Shared or untrusted agent can invoke control-plane tools |
| OC-039 | HIGH | sessions_spawn allowed with unrestricted subagents |

## Node & Device Security

| Rule | Severity | Title |
|------|----------|-------|
| OC-040 | HIGH | gateway.nodes.allowCommands includes dangerous device commands |
| OC-041 | MEDIUM | Node denyCommands uses invalid patterns or unrecognized command names |
| OC-042 | HIGH | Paired node exec approvals default to permissive mode |

## Network Discovery

| Rule | Severity | Title |
|------|----------|-------|
| OC-043 | MEDIUM | mDNS discovery mode set to full, exposing host metadata |

## Identity Matching

| Rule | Severity | Title |
|------|----------|-------|
| OC-044 | HIGH | Channel uses dangerouslyAllowNameMatching, enabling identity spoofing |

## Sessions & Multi-User

| Rule | Severity | Title |
|------|----------|-------|
| OC-045 | HIGH | Shared DM channel uses dmScope=main, merging all users into one session |
| OC-046 | HIGH | Multi-user heuristic triggered but no session isolation or sandbox |

## HTTP / URL Ingestion

| Rule | Severity | Title |
|------|----------|-------|
| OC-047 | HIGH | URL allowlist missing for OpenResponses file/image ingestion |

## Allowlists

| Rule | Severity | Title |
|------|----------|-------|
| OC-057 | HIGH | Channel allowFrom or group allowlist contains wildcard |
| OC-058 | MEDIUM | Allowlist uses mutable identifiers instead of stable IDs |

## Path & Package Safety

| Rule | Severity | Title |
|------|----------|-------|
| OC-059 | MEDIUM | Skill, plugin, or hook entry escapes root directory via symlink |

## Runtime Hygiene

| Rule | Severity | Title |
|------|----------|-------|
| OC-060 | MEDIUM | Sandbox browser container missing or has stale config hash label |

## Model Hygiene

| Rule | Severity | Title |
|------|----------|-------|
| OC-055 | HIGH | Weak or legacy model granted broad tool access without sandbox |
| OC-056 | HIGH | External-input agent has broad tool surface without minimized profile |
| OC-114 | LOW | Legacy or deprecated AI model configured in agent |

## Identity Governance

| Rule | Severity | Title |
|------|----------|-------|
| OC-061 | MEDIUM | Production integrations still use personal email or personal accounts |
| OC-062 | HIGH | Control-plane or upstream provider accounts lack enforced MFA |
| OC-063 | HIGH | Same gateway token or password reused across environments |
| OC-064 | HIGH | Multiple agents or channels share a single broad-privilege human credential |

## Credential Governance

| Rule | Severity | Title |
|------|----------|-------|
| OC-065 | HIGH | Gateway bearer token scope exceeds least privilege |
| OC-066 | MEDIUM | Token TTL or rotation period exceeds organizational policy |
| OC-067 | MEDIUM | Same secret reused across channels, agents, or trust boundaries |
| OC-068 | MEDIUM | Credential supporting SecretRef is still stored as plaintext |
| OC-106 | MEDIUM | Cross-config credential/token reuse detected across multiple locations |

## Host Governance

| Rule | Severity | Title |
|------|----------|-------|
| OC-069 | HIGH | Shared runtime lacks dedicated OS user, full-disk encryption, or dedicated host |

## Trust Boundary Governance

| Rule | Severity | Title |
|------|----------|-------|
| OC-070 | HIGH | Personal and corporate agents share the same gateway host or configuration |
| OC-071 | HIGH | Personal and corporate agents share the same workspace or browser profile |

## Supply Chain Governance

| Rule | Severity | Title |
|------|----------|-------|
| OC-072 | MEDIUM | No formal inventory or approval process for enabled plugins and hooks |
| OC-073 | MEDIUM | Internal plugin or hook release artifacts lack an SBOM |
| OC-074 | HIGH | Plugins or hooks have no dependency vulnerability scanning |
| OC-075 | HIGH | Internal plugin or hook packages lack code signing or provenance |
| OC-076 | MEDIUM | Locally distributed archive lacks hash or integrity verification |
| OC-115 | CRITICAL | Plugin source code contains potentially unsafe code patterns |
| OC-116 | CRITICAL | Installed skill source code contains potentially unsafe code patterns |

## CI / SDLC Security

| Rule | Severity | Title |
|------|----------|-------|
| OC-077 | MEDIUM | Repositories do not have secret scanning enabled |
| OC-078 | MEDIUM | Production configuration does not use security audit as a release gate |
| OC-079 | MEDIUM | No configuration drift detection or policy-as-code enforcement |

## Governance Exceptions

| Rule | Severity | Title |
|------|----------|-------|
| OC-080 | MEDIUM | Break-glass or dangerous override enabled without owner, ticket, or expiry |

## Gateway Credential Governance

| Rule | Severity | Title |
|------|----------|-------|
| OC-081 | HIGH | Third-party automation uses full operator bearer credential without scoping |
| OC-082 | HIGH | Tailscale tokenless auth enabled in untrusted environment |

## Reverse Proxy Governance

| Rule | Severity | Title |
|------|----------|-------|
| OC-083 | MEDIUM | TLS terminated at reverse proxy without HSTS or trusted proxy policy |

## Monitoring & Detection

| Rule | Severity | Title |
|------|----------|-------|
| OC-084 | MEDIUM | Agent events not centralized to SIEM |
| OC-085 | MEDIUM | Missing alerting for auth failures and dangerous flag toggles |
| OC-086 | HIGH | Missing alerting for elevated exec and browser automation |
| OC-087 | HIGH | Missing monitoring for private network browser access and anomalous egress |

## Incident Response

| Rule | Severity | Title |
|------|----------|-------|
| OC-088 | MEDIUM | No incident response runbook for prompt injection or tool misuse |
| OC-089 | MEDIUM | No secret rotation playbook for log or transcript leakage |
| OC-090 | MEDIUM | No evidence collection checklist for incident investigations |

## Data Governance

| Rule | Severity | Title |
|------|----------|-------|
| OC-091 | MEDIUM | Log and transcript retention period undefined or exceeds business need |
| OC-092 | MEDIUM | Cron session retention exceeds organizational policy |
| OC-093 | LOW | Raw logs shared for debugging instead of redacted diagnostic output |

## AI Governance

| Rule | Severity | Title |
|------|----------|-------|
| OC-094 | MEDIUM | No adversarial or prompt-injection testing before enabling new surface |
| OC-095 | MEDIUM | No model or tool risk review before enabling weak models or browser tools |

## Asset & Risk Governance

| Rule | Severity | Title |
|------|----------|-------|
| OC-096 | MEDIUM | Missing asset inventory for agents, channels, nodes, plugins, hooks |
| OC-097 | MEDIUM | Missing trust-boundary matrix mapping agents to data classes and tools |

## Change & Access Governance

| Rule | Severity | Title |
|------|----------|-------|
| OC-098 | MEDIUM | No approval or change record for enabling new plugins or tool groups |
| OC-099 | MEDIUM | Pairing allowlists and wildcard sender rules not periodically reviewed |

## Enterprise Baseline

| Rule | Severity | Title |
|------|----------|-------|
| OC-100 | HIGH | No enterprise OpenClaw hardening baseline defined or enforced |

## Config Hygiene

| Rule | Severity | Title |
|------|----------|-------|
| OC-104 | MEDIUM | Unrecognized dangerously* config flags enabled |

---

## Category Cross-Reference

| Category | Rules | Count | L1 Checks |
|----------|-------|-------|-----------|
| Gateway Security | OC-001..007, OC-101, OC-107, OC-108 | 10 | 8 of 10 |
| Channel Access Control | OC-008..010 | 3 | 2 of 3 |
| Tool Permissions | OC-011..014, OC-105 | 5 | 4 of 5 |
| Hooks & External Content | OC-015 | 1 | 1 of 1 |
| Hooks & Automation | OC-048..051, OC-102, OC-103 | 6 | 3 of 6 |
| Secret Management | OC-016..017 | 2 | 1 of 2 |
| Logging & Audit | OC-018..019 | 2 | 1 of 2 |
| Local State Security | OC-020..022, OC-113 | 4 | 0 of 4 |
| Plugin Intake | OC-023..024 | 2 | 1 of 2 |
| Browser Security | OC-025, OC-029, OC-052..054, OC-112 | 6 | 1 of 6 |
| Sandboxing & Isolation | OC-026..028, OC-030..033, OC-111 | 8 | 3 of 8 |
| Exposure Combinations | OC-034..035 | 2 | 1 of 2 |
| Tool Policy Hygiene | OC-036..037, OC-109, OC-110 | 4 | 0 of 4 |
| Control Plane Tools | OC-038..039 | 2 | 0 of 2 |
| Node & Device Security | OC-040..042 | 3 | 0 of 3 |
| Network Discovery | OC-043 | 1 | 0 of 1 |
| Identity Matching | OC-044 | 1 | 1 of 1 |
| Sessions & Multi-User | OC-045..046 | 2 | 0 of 2 |
| HTTP / URL Ingestion | OC-047 | 1 | 1 of 1 |
| Allowlists | OC-057..058 | 2 | 1 of 2 |
| Path & Package Safety | OC-059 | 1 | 0 of 1 |
| Runtime Hygiene | OC-060 | 1 | 0 of 1 |
| Model Hygiene | OC-055..056, OC-114 | 3 | 0 of 3 |
| Identity Governance | OC-061..064 | 4 | 0 of 4 |
| Credential Governance | OC-065..068, OC-106 | 5 | 1 of 5 |
| Host Governance | OC-069 | 1 | 0 of 1 |
| Trust Boundary Governance | OC-070..071 | 2 | 0 of 2 |
| Supply Chain Governance | OC-072..076, OC-115, OC-116 | 7 | 0 of 7 |
| CI / SDLC Security | OC-077..079 | 3 | 0 of 3 |
| Governance Exceptions | OC-080 | 1 | 0 of 1 |
| Gateway Credential Governance | OC-081..082 | 2 | 0 of 2 |
| Reverse Proxy Governance | OC-083 | 1 | 0 of 1 |
| Monitoring & Detection | OC-084..087 | 4 | 0 of 4 |
| Incident Response | OC-088..090 | 3 | 0 of 3 |
| Data Governance | OC-091..093 | 3 | 0 of 3 |
| AI Governance | OC-094..095 | 2 | 0 of 2 |
| Asset & Risk Governance | OC-096..097 | 2 | 0 of 2 |
| Change & Access Governance | OC-098..099 | 2 | 0 of 2 |
| Enterprise Baseline | OC-100 | 1 | 0 of 1 |
| Config Hygiene | OC-104 | 1 | 1 of 1 |
| **Total** | | **116** | **33 of 116** |

---

## Notes

- L1 checks (33 rules) run during browser-based local scans: OC-001 through OC-016, OC-018, OC-023, OC-025, OC-026, OC-027, OC-030, OC-034, OC-044, OC-047, OC-048, OC-050, OC-057, OC-101, OC-102, OC-103, OC-104, OC-106.
- Non-L1 rules appear only in L2 (full config audit) and L3 (governance review) reports.
- Catalog descriptions are sourced from rulepack v2 (`openclaw_rules_v2.json`).
- For rules not in this catalog, construct explanation from the finding's own message and description fields and mark with **[not in catalog]**.
