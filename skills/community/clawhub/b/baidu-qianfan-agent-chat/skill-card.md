## Description:

Calls the Baidu Qianfan application conversation API for agent chat interactions, including streaming or non-streaming responses, function-call tool reporting, file IDs, and multi-turn sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lilitong9607](https://clawhub.ai/user/lilitong9607)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to send chat prompts to Baidu Qianfan applications, manage conversation IDs, and pass optional function-call, file, metadata, and action parameters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chat prompts and selected request metadata are sent to Baidu Qianfan.

Mitigation: Use the skill only for authorized data and avoid sending sensitive information unless the deployment permits it.

Risk: QIANFAN_API_KEY is required for API access.

Mitigation: Keep the key in a private environment variable and do not commit or log it.

Risk: The wrapper may save a conversation ID locally for follow-up calls.

Mitigation: Delete or protect artifact/state/session.json when conversation linkage should not persist on the machine.

## Reference(s):

- [Qianfan API reference](artifact/references/api.md)
- [Baidu Qianfan conversation API documentation](https://cloud.baidu.com/doc/qianfan-api/s/7m7wqq361)
- [Baidu Qianfan developer center](https://cloud.baidu.com/product/wenxinworkshop)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls]

**Output Format:** [Markdown guidance, shell command examples, and Baidu Qianfan text or JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires QIANFAN_API_KEY; may store a conversation ID in artifact/state/session.json for follow-up calls.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
