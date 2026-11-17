## Description:

Generate safer OpenClaw configuration baselines and audit existing config files for exposure, missing controls, and secret hygiene issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mike007jd](https://clawhub.ai/user/mike007jd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use Baseline Kit to generate reviewable OpenClaw configuration JSON and audit existing OpenClaw configs before rollout or after configuration changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated configuration may not match a team's exact runtime policy or threat model.

Mitigation: Review generated JSON before use and treat the output as a starting baseline rather than a complete configuration management system.

Risk: Auditing a configuration can reveal paths to secret-like fields in command output.

Mitigation: Run audits in a trusted local environment and avoid sharing audit output until sensitive paths and values have been reviewed.

## Reference(s):

- [Baseline Kit on ClawHub](https://clawhub.ai/mike007jd/skills/baseline-kit)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [configuration, text, markdown, shell commands, guidance]

**Output Format:** [JSON files and Markdown or plain-text CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated profiles include development, team, enterprise, and airgapped variants; audit findings include severity, evidence path, recommendation, and compliance tags.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
