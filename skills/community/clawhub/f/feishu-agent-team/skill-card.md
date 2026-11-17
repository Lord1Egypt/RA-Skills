## Description:

Build a configurable OpenClaw multi-agent team in which a Coordinator receives Feishu group @mentions and routes tasks to specialist agents by keyword.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mars82311111](https://clawhub.ai/user/mars82311111)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to configure a coordinator-and-specialist agent team for routing Feishu group chat tasks to business analysis, development, marketing, or custom roles. It is most useful as a starting point for OpenClaw team routing and configuration workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review classifies the release as suspicious because the documented Feishu, MQ, and LangGraph automation is broader than the shipped implementation.

Mitigation: Treat it as prototype-quality, review and pin dependencies, and verify missing Feishu, MQ, and LangGraph pieces before running listeners.

Risk: Feishu app secrets and group chat content may be exposed if real credentials or sensitive group data are used before access controls and privacy handling are added.

Mitigation: Avoid placing real Feishu app secrets or sensitive group content into the skill until those controls are reviewed and implemented.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mars82311111/skills/feishu-agent-team)
- [Publisher profile](https://clawhub.ai/user/mars82311111)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON/YAML configuration examples, and Python code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces routing decisions and setup guidance; shipped listener integration code contains placeholders for MQ and Feishu API behavior.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact src/__init__.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
