## Description: <br>
DashClaw platform expert for integration, troubleshooting, and governance. Snapshot-based - prefer live queries via `python -m livingcode query`, or `GET {baseUrl}/api/doctor` when Python/livingcode/the repo are unavailable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dashclaw](https://clawhub.ai/user/dashclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to understand DashClaw platform structure, API routes, environment requirements, troubleshooting paths, and integration health. It helps agents prefer live platform queries when available and fall back to bundled snapshot documentation when live access is unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents to query a DashClaw instance with sensitive credentials. <br>
Mitigation: Use a least-privilege or test API key and avoid sharing production credentials in prompts, logs, or diagnostics. <br>
Risk: Full validation, bootstrap validation, live bootstrap, `/api/doctor/fix`, and setup-proof capture can create records or change configuration. <br>
Mitigation: Review commands before execution and avoid running write-capable flows against production unless the resulting records, uploads, or configuration changes are acceptable. <br>
Risk: Bundled platform facts may become stale when live queries or the DashClaw repository are unavailable. <br>
Mitigation: Prefer `python -m livingcode query` or `GET {baseUrl}/api/doctor`; use the static snapshot only as the documented fallback. <br>


## Reference(s): <br>
- [DashClaw API Surface](references/api-surface.md) <br>
- [DashClaw Platform Knowledge](references/platform-knowledge.md) <br>
- [DashClaw Troubleshooting Guide](references/troubleshooting.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/dashclaw/dashclaw-platform-intelligence) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON diagnostic output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend live queries, authenticated API calls, diagnostic scripts, or opt-in write checks.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
