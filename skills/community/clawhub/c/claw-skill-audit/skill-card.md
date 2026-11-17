## Description:

Automatically audits newly installed skills for structure, basic security indicators, and health before activation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yoborlon-alpha](https://clawhub.ai/user/yoborlon-alpha)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect newly installed OpenClaw or ClawHub skills before enabling them. It helps identify missing structure, obvious secret patterns, unsafe permissions, and basic health issues during install and maintenance workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A PASS result may overstate the safety of another skill because the audit checks can fail silently.

Mitigation: Treat the audit output as triage only; review the target skill source and scanner evidence before enabling or distributing it.

Risk: The skill focuses on basic structure, secret patterns, permissions, and health checks, so it may miss behavior outside those checks.

Mitigation: Use it alongside manual review and independent security scanning for install or release decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yoborlon-alpha/skills/claw-skill-audit)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text audit report with PASS, WARN, FAIL, and INFO status lines]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a severity-oriented exit code for pass, warning, or failure outcomes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
