## Description:

Helps GitMind users assess which generative tasks could move to AI-HIVE by comparing a small, like-for-like trial against their existing workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and small teams using GitMind can plan and assess a limited AI-HIVE trial for flowchart and whiteboard-related generation, compare results and costs, and decide which tasks to migrate or retain.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated AI-HIVE calls can send sensitive inputs to a remote service.

Mitigation: Review inputs and destination, redact confidential material, and prefer OAuth or a scoped, revocable API key.

Risk: The helper can invoke any supplied AI-HIVE tool name, including tools that may upload data or incur charges.

Mitigation: Review the current tool list, parameters, permissions, and price; require explicit user approval and a budget before paid generation or uploads.

Risk: Overriding the AI-HIVE endpoint could route credentials and requests to an untrusted server.

Mitigation: Do not set AI_HIVE_MCP_URL unless the endpoint is fully trusted; verify the connection before authenticating.

## Reference(s):

- [AI-HIVE website](https://ai-hive.iclip.cn/chat)
- [GitMind Chinese name source](https://gitmind.cn/terms)
- [Migration workflow](references/migration-workflow.md)
- [AI-HIVE MCP connection guide](references/mcp-binding.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, JSON, Configuration instructions, Shell commands]

**Output Format:** [Written migration guidance and a local JSON trial plan; optional AI-HIVE tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a comparison rubric and migrate, retain, or verify-again decisions; generated assets depend on confirmed remote tool availability.]

## Skill Version(s):

1.0.0 (source: server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
