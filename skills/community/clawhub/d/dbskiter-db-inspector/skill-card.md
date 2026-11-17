## Description:

Guides an agent through dbskiter database instance inspections, report generation, baseline creation, anomaly detection, root-cause analysis, risk prediction, and optimization recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[magicczc](https://clawhub.ai/user/magicczc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database operators use this skill to run dbskiter inspections against named database instances, interpret health and risk findings, generate reports, and request follow-up analysis such as anomaly detection, root-cause analysis, and risk prediction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger database inspection commands from broad natural-language requests.

Mitigation: Require explicit database target confirmation before running dbskiter commands.

Risk: Command templates include user-controlled database names, metrics, and issue text.

Mitigation: Run dbskiter with structured arguments or strict input validation instead of interpolating user input into shell commands.

Risk: Use in environments with database access can expose operational data or affect sensitive systems.

Mitigation: Install only where dbskiter is trusted, configured for intended databases, and reviewed before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/magicczc/skills/dbskiter-db-inspector)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with dbskiter shell commands and references to generated HTML, Markdown, or JSON reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a trusted dbskiter installation, explicit database target confirmation, and validated command arguments.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
