## Description: <br>
Creates compact, privacy-aware audit records for important agent decisions, checks, changes, evidence, and residual risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mindbomber](https://clawhub.ai/user/mindbomber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to produce concise audit notes for guardrail decisions, sensitive actions, refusals, escalations, corrections, and changed plans. It helps record what was checked, what failed or remained unverified, what changed, and how private data was minimized. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Decision logs may expose sensitive data if raw records, secrets, payment details, private messages, or sensitive logs are copied into the audit note. <br>
Mitigation: Use redacted summaries, omit forbidden payload content, and record only the evidence basis needed for review. <br>
Risk: A log can overstate assurance by implying checks, tests, evidence review, or compliance validation that did not actually happen. <br>
Mitigation: List only checks actually performed, mark missing or unclear checks as unverified, and include residual risk for high-impact decisions. <br>
Risk: The skill provides instructions and schema guidance but does not enforce storage, retention, access control, or review workflows by itself. <br>
Mitigation: Treat decision logs as guidance-driven audit artifacts and apply host-side review, retention, and access controls before sharing or storing them. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/mindbomber/aana-decision-log) <br>
- [README](README.md) <br>
- [Skill instructions](SKILL.md) <br>
- [Decision log schema](schemas/decision-log.schema.json) <br>
- [Redacted decision log example](examples/redacted-decision-log.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown decision-log bullets or JSON matching the bundled decision-log schema] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; does not install dependencies, execute commands, call services, write files, or persist memory by itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
