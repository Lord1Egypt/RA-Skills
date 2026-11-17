## Description:

Austrian-style Bilanz (annual accounts) generator

This skill is ready for commercial/non-commercial use.

## Publisher:

[kleberbaum](https://clawhub.ai/user/kleberbaum)

### License/Terms of Use:

MIT

## Use Case:

Developers and accounting-focused agents use this skill to produce Austrian-style annual accounts section templates for Aktiva and Passiva and to display release metadata. The current release is a static status and template helper, not a complete UGB compliance validator or financial calculation engine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill outputs static Austrian accounting section templates and should not be treated as validated financial statements or a complete UGB compliance determination.

Mitigation: Have qualified accounting or legal reviewers validate figures, structure, and regulatory suitability before business, audit, or filing use.

Risk: The skill requires executing a shell helper script.

Mitigation: Review the included shell script before deployment and run only the documented flags in a controlled environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kleberbaum/skills/bilanz)
- [Netsnek website](https://netsnek.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and plain-text report output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Executes a small shell helper with documented flags: --status, --aktiva, and --passiva.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter, claw.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
