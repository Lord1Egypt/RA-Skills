## Description:

Checks Node.js, npm, global npm packages, and project dependency updates on a weekly or manual schedule.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axelhu](https://clawhub.ai/user/axelhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to check Node.js and npm dependency status, generate a dependency report, and send the report to a configured Feishu recipient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Package inventory and dependency update information may be shared outside the local environment through Feishu.

Mitigation: Configure and verify the Feishu recipient before use, and limit global package reporting if project-only dependency tracking is sufficient.

## Reference(s):

- [Dependency Tracker detailed specification](artifact/references/spec.md)

## Skill Output:

**Output Type(s):** [markdown, text, guidance]

**Output Format:** [Markdown report and Feishu message text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a dated dependency report under data/exec-logs/dependency-tracker and sends it to the configured Feishu recipient.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
