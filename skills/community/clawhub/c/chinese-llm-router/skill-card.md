## Description:

Routes OpenClaw chats to Chinese LLM providers through a unified OpenAI-compatible interface with model selection, recommendations, fallback, testing, and cost tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xdd-xund](https://clawhub.ai/user/xdd-xund)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to configure and route conversations across Chinese LLM providers, compare models, select task-specific models, test connectivity, and manage fallback behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys are stored in a local JSON configuration file and may be exposed if file permissions are weak.

Mitigation: Restrict permissions on the configuration file and do not share or commit it.

Risk: Prompts and credentials can be sent to configurable external provider endpoints.

Mitigation: Use only trusted HTTPS base URLs and avoid regulated or confidential data unless the selected providers and workflow are approved.

## Reference(s):

- [Chinese LLM API Reference](references/api-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/xdd-xund/skills/chinese-llm-router)
- [Publisher Profile](https://clawhub.ai/user/xdd-xund)
- [AI Plaza](https://ai.xudd-v.com)
- [Feedback](https://ai.xudd-v.com/connect.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and text results from model listing, recommendation, and connectivity commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include selected model names, provider names, API connectivity status, token usage, and estimated cost information.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
