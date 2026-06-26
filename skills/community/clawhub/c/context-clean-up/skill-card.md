## Description: <br>
Context Clean Up audits prompt-context bloat, ranks likely offenders, and returns a reversible cleanup plan without applying changes automatically. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phenomenoner](https://clawhub.ai/user/phenomenoner) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to diagnose slow, noisy, or costly OpenClaw sessions and prioritize low-risk context reductions. It helps produce ranked offenders, expected impact, rollback notes, and verification steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inspects local OpenClaw session history and may generate reports containing sensitive transcript details. <br>
Mitigation: Treat generated JSON reports as private, review them before sharing, and redact sensitive details. <br>
Risk: Out-of-band notification guidance can expose details if sent through an uncontrolled channel. <br>
Mitigation: Use only notification channels you control, keep messages short, and send links or paths to reviewed artifacts when details are needed. <br>
Risk: Cleanup recommendations could remove useful context or change runtime behavior if applied without review. <br>
Mitigation: Apply changes manually, lowest risk first, with explicit rollback notes and fresh-session verification. <br>


## Reference(s): <br>
- [Out-of-band delivery](references/out-of-band-delivery.md) <br>
- [Cron noise checklist](references/cron-noise-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with optional shell commands and JSON audit report paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Audit-only by default; no automatic deletions or unattended configuration edits are applied.] <br>

## Skill Version(s): <br>
1.0.7 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
