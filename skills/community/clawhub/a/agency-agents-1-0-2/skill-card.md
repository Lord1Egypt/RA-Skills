## Description:

AI Agent team skill that provides specialized agents across business departments for single-agent tasks, multi-agent orchestration, and department-level collaboration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gyzx](https://clawhub.ai/user/gyzx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and teams use this skill to select specialized agents for engineering, marketing, project management, testing, and related workflow tasks, or to coordinate several agents through an orchestrator for larger projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Manual clone installation can bypass the server-resolved release path and increase provenance uncertainty.

Mitigation: Install through ClawHub and verify the release hash and publisher profile before deployment.

Risk: Backend deployment examples include placeholder credentials, plaintext service URLs, Kafka plaintext listeners, and unpinned container images.

Mitigation: Replace example credentials, require secure transport, pin reviewed images, and run a deployment security review before using generated infrastructure examples.

Risk: Agent outputs may be retained under ~/clawd/agency-agents, which can preserve sensitive project data locally.

Mitigation: Avoid submitting secrets or regulated data unless storage, access controls, retention, and cleanup behavior have been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gyzx/skills/agency-agents-1-0-2)
- [Publisher profile](https://clawhub.ai/user/gyzx)
- [README](README.md)
- [Quickstart guide](docs/QUICKSTART.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with code blocks and task-specific deliverables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include implementation plans, project reports, code snippets, configuration examples, quality checks, and follow-up recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json; display metadata: Agency Agents 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
