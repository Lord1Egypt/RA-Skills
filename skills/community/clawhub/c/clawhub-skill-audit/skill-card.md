## Description:

Audits locally installed skills against ClawHub to detect version drift, identify publish candidates, review security flags, and triage ownership conflicts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to run ClawHub lifecycle checks for local and published skills, including drift detection, publish readiness, security review, and ownership-conflict triage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publish and update commands can change public ClawHub registry state or local installed skills.

Mitigation: Treat publish and update steps as manual approval points and review the target skill, version, and changelog before execution.

Risk: The playbook includes hardcoded local paths, owner names, and an AEST lifecycle schedule that may not match another environment.

Mitigation: Adapt paths, publisher handles, and schedule details before using the workflow outside the evidenced environment.

Risk: The skill fetches registry metadata through the ClawHub CLI.

Mitigation: Run it only in environments approved for outbound ClawHub registry access.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nissan/skills/clawhub-skill-audit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks and checklist-style guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the clawhub CLI and python3; uses outbound network access to fetch ClawHub registry metadata.]

## Skill Version(s):

1.0.2 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
