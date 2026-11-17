## Description:

飞书知识库查询 helps an agent search and retrieve documents from the openclaw Feishu knowledge base so it can reuse existing guides, best practices, and historical records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[subwukong](https://clawhub.ai/user/subwukong)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill when they need an agent to consult the openclaw Feishu knowledge base for prior operating procedures, installation guides, security practices, and related historical references before acting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Knowledge-base documents may influence the agent's work even when contents are stale, overly broad, or outside the user's intent.

Mitigation: Review the Feishu knowledge-base permissions and contents, and keep trigger wording scoped to tasks that explicitly call for prior knowledge or procedure lookup.

Risk: Retrieved operating guidance can become outdated.

Mitigation: Confirm time-sensitive procedures before execution and update the knowledge base when stale content is found.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/subwukong/skills/feishu-knowledge-query)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Markdown or plain text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include summarized or cited content retrieved from the configured Feishu knowledge base.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
