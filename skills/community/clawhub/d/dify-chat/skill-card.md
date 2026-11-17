## Description:

Dify工作流调用 lets OpenClaw users send questions to a configured Dify knowledge-base chat API and receive answers from the command line.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yep123456](https://clawhub.ai/user/yep123456)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and developers use this skill to query an organization's Dify-backed knowledge base from OpenClaw for document lookup, internal Q&A, and support workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Questions and the Dify API token can be sent to an unrestricted or unencrypted endpoint.

Mitigation: Review DIFY_API_BASE before use, prefer a trusted HTTPS Dify endpoint, and avoid sending secrets or highly sensitive company data in prompts.

Risk: The advertised multi-turn and streaming behavior may be unreliable.

Mitigation: Validate conversation ID handling and response behavior in a controlled environment before relying on the skill for operational workflows.

## Reference(s):

- [Dify API Documentation](https://docs.dify.ai/)
- [Dify Workflow Run API](https://docs.dify.ai/reference/dify-api/apis/workflow-run)
- [OpenClaw CLI Tools](https://docs.openclaw.ai/cli-tools)
- [Server-Sent Events](https://developer.mozilla.org/zh-CN/docs/Web/API/Server-sent_events)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Plain text CLI responses with optional conversation IDs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DIFY_API_KEY and a trusted DIFY_API_BASE configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill changelog dated 2026-04-14)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
