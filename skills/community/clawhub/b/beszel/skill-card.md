## Description:

Deploy, secure, and troubleshoot Beszel monitoring with Docker agents, alert tuning, and upgrade-safe operations for self-hosted servers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to plan and maintain Beszel monitoring for self-hosted infrastructure, including Docker-based deployment, agent onboarding, alert calibration, diagnostics, and upgrade rollback planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local operational notes could accidentally capture credentials or sensitive monitoring details.

Mitigation: Review each proposed save, avoid storing credentials in ~/beszel/, and keep only reusable operational context.

Risk: Over-broad proactive activation could surface monitoring advice in contexts where it is not wanted.

Mitigation: Approve proactive activation only for the Beszel and monitoring contexts the user explicitly wants.

Risk: Alert thresholds or deployment changes applied too quickly can create noisy incidents or monitoring blind spots.

Mitigation: Baseline first, change one variable at a time, define alert ownership, and keep rollback notes for upgrades.

## Reference(s):

- [Beszel ClawHub skill page](https://clawhub.ai/ivangdavila/skills/beszel)
- [Beszel skill homepage](https://clawic.com/skills/beszel)
- [Setup behavior](setup.md)
- [Memory template](memory-template.md)
- [Deployment patterns](deployment-patterns.md)
- [Alert tuning workflow](alert-tuning.md)
- [Diagnostics playbook](diagnostics-playbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with checklists and inline command or configuration suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local operational notes under ~/beszel/ after user confirmation.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
