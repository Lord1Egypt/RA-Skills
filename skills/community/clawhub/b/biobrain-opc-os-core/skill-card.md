## Description:

AI-native one-person company operating system with 7 autonomous agent departments, governance, cron automation, revenue funnel, and inter-agent communications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ygq19901001](https://clawhub.ai/user/ygq19901001)

### License/Terms of Use:

MIT-0

## Use Case:

Independent operators and developers use this skill as an operating playbook for structuring a one-person company around autonomous agent departments, scheduled reporting, governance rules, communication channels, and monetization workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent cron workflows can write shared files, send notifications, and run without close supervision.

Mitigation: Enable scheduled jobs only after setting explicit output directories, notification recipients, cloud-document permissions, retention rules, and failure alerts.

Risk: Autonomous public posting or skill republishing can publish material before a human has reviewed it.

Mitigation: Require human approval gates for public posts, SkillHub publishing, and monthly republishing unless that authority is intentionally delegated.

Risk: Shared and cloud communication channels can expose internal operating data if permissions are too broad.

Mitigation: Scope channel access by department, review cloud-document permissions, and retain audit trails for cross-department handoffs.

## Reference(s):

- [Server-resolved GitHub provenance: Ygq19901001/biobrain-opc-os-core](https://github.com/Ygq19901001/biobrain-opc-os-core)
- [Communication Protocols](references/communication-protocols.md)
- [Cron Orchestration](references/cron-orchestration.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code blocks and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational guidance for directories, scheduled agent tasks, communications, review gates, and publishing workflows.]

## Skill Version(s):

0.1.2 (source: ClawHub release evidence; artifact frontmatter says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
