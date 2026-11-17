## Description:

Claw Problem Diagnoser helps diagnose OpenClaw configuration, dependency, service, permission, performance, and integration issues and can produce repair guidance or reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[betsymalthus](https://clawhub.ai/user/betsymalthus)

### License/Terms of Use:

MIT

## Use Case:

Developers, OpenClaw users, and system administrators use this skill to troubleshoot OpenClaw setup and runtime problems, generate diagnostic reports, and receive concrete repair recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic repair behavior may install Python packages, initialize or start OpenClaw, or change permissions under the user's OpenClaw directory.

Mitigation: Run diagnosis and report modes first, avoid sudo, and enable auto-fix only after reviewing the proposed actions.

Risk: Diagnostic reports can include host, platform, configuration-path, and environment details.

Mitigation: Treat generated reports as sensitive and review them before sharing outside the deployment team.

## Reference(s):

- [Claw Problem Diagnoser on ClawHub](https://clawhub.ai/betsymalthus/skills/claw-problem-diagnoser)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Console text, JSON, or Markdown diagnostic reports with suggested commands and repair steps.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports can include host and environment details; auto-fix mode can run package installation, OpenClaw initialization or startup commands, and permission changes.]

## Skill Version(s):

0.1.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
