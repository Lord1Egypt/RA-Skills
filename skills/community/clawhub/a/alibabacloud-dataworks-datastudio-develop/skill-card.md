## Description:

DataWorks data development skill for creating, configuring, validating, deploying, updating, moving, and renaming DataWorks nodes, workflows, components, file resources, and UDF functions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and data engineers use this skill to manage Alibaba Cloud DataWorks DataStudio development workflows. It helps produce and validate FlowSpec definitions, CLI commands, Python SDK examples, scheduling settings, deployment steps, and Data Integration task guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask the agent to run an unverified remote Aliyun CLI installer.

Mitigation: Install or update Aliyun CLI through a pinned, trusted, verifiable method before using the skill, and avoid the curl-to-shell path when possible.

Risk: The skill may make persistent Aliyun CLI and plugin changes.

Mitigation: Review plugin installation and update steps before approval, and use a controlled CLI profile for the target DataWorks project.

Risk: The skill can guide broad cloud mutations in Alibaba Cloud DataWorks resources.

Mitigation: Use least-privilege RAM credentials scoped to the target project and require explicit review before update, move, rename, publish, or other mutating operations.

## Reference(s):

- [Skill Source](artifact/SKILL.md)
- [CLI Installation and Configuration Guide](artifact/references/cli-installation-guide.md)
- [FlowSpec Field Reference](artifact/references/flowspec-guide.md)
- [Workflow Development Guide](artifact/references/workflow-guide.md)
- [Scheduling Guide](artifact/references/scheduling-guide.md)
- [Publishing and Deployment Guide](artifact/references/deploy-guide.md)
- [Data Integration Guide](artifact/references/di-guide.md)
- [RAM Policies](artifact/references/ram-policies.md)
- [Acceptance Criteria](artifact/references/acceptance-criteria.md)
- [Troubleshooting](artifact/references/troubleshooting.md)
- [Related Commands](artifact/references/related-commands.md)
- [Alibaba Cloud DataWorks API Metadata](https://api.aliyun.com/meta/v1/products/dataworks-public/versions/2024-05-18/apis/{APIName}/api.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON FlowSpec/spec examples, configuration snippets, and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are proposals for DataWorks resource operations and should be reviewed before execution.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
