## Description:

Universal React dashboard audit — detect hardcoded values, tier bypasses, stale components, and onboarding inconsistencies before users see them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tooled-app](https://clawhub.ai/user/tooled-app)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill before dashboard releases, auth or tier changes, onboarding changes, and production readiness reviews to find inconsistent React UI behavior and risky hardcoded values.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit guidance may lead an agent to propose changes around auth, tiering, or pricing behavior.

Mitigation: Review proposed fixes before applying them and verify the resulting dashboard behavior with the skill's release-readiness checks.

Risk: The skill asks the agent to run local source-code searches and normal project verification steps.

Mitigation: Run the checks in the intended project workspace and inspect any commands before execution.

## Reference(s):

- [Pre-flight Skill Page](https://clawhub.ai/tooled-app/skills/dashboard-pre-flight)
- [IKKF](https://ikkf.info)
- [Demystify](https://demystified.website)
- [Tooled](https://tooled.pro)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown checklist with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces audit findings, verification steps, and concise fix records for React dashboard release readiness.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
