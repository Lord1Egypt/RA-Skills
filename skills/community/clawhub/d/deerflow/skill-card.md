## Description:

Submits and monitors multi-step deep research tasks against a running DeerFlow LangGraph API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bevanding](https://clawhub.ai/user/bevanding)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to send research prompts to an existing DeerFlow service and retrieve task status or results from the LangGraph API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research prompts and task results are sent to the configured DeerFlow LangGraph endpoint.

Mitigation: Connect only to a trusted DeerFlow instance, keep it on localhost or behind authenticated TLS, and avoid sending sensitive prompts to untrusted remote endpoints.

Risk: Optional DeerFlow deployment steps rely on external Docker images and configuration outside this skill.

Mitigation: Review or pin the upstream DeerFlow Docker deployment before running it; this skill only connects to an already running DeerFlow API.

## Reference(s):

- [ClawHub Deerflow skill page](https://clawhub.ai/bevanding/skills/deerflow)
- [DeerFlow upstream project](https://github.com/bytedance/deer-flow)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Text and JSON with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns DeerFlow thread and run identifiers, then polls configured LangGraph endpoints for task status and results.]

## Skill Version(s):

1.1.3 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
