## Description:

Analyze SKILL.md files for security risks, quality issues, and best-practice violations to support safer OpenClaw skill installation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gpunter](https://clawhub.ai/user/gpunter)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to audit OpenClaw SKILL.md files before installation, compare skill versions, and generate shareable security reports. It helps reviewers identify risky patterns, quality gaps, and best-practice violations while keeping final trust decisions human-reviewed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trust scores and findings are heuristic and may miss runtime-only attacks or risks that are not visible in the skill definition.

Mitigation: Use the audit output as review guidance, not as a guarantee, and combine it with manual inspection before installing or updating a skill.

Risk: The skill reads user-supplied skill files and may fetch a URL provided for audit.

Mitigation: Point it only at intended SKILL.md files or URLs, and avoid supplying private files unrelated to the audit task.

## Reference(s):

- [CLAW-1 Skill Auditor on ClawHub](https://clawhub.ai/gpunter/skills/claw1-skill-auditor)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown audit reports with trust scores, severity counts, warnings, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Heuristic security and quality findings for the SKILL.md file or URL supplied by the user.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
