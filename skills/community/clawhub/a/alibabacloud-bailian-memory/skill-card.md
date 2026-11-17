## Description:

Manages conversation memories and user profiles in Alibaba Cloud Bailian (Model Studio) Memory Library via DashScope REST APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to persist, search, update, and delete user memories and structured profiles in Alibaba Cloud Bailian Memory Library while managing related memory projects and profile schemas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Normal use can rely on Alibaba Cloud or DashScope credentials and may bootstrap persistent cloud API keys.

Mitigation: Configure a least-privilege DASHSCOPE_API_KEY manually, review Alibaba Cloud CLI config handling, and avoid automatic CLI plugin or key creation unless explicitly intended.

Risk: Destructive memory deletion is irreversible and a wrong memory node identifier can delete the wrong context.

Mitigation: Fetch the target memory node, show its current content and identifier, require explicit confirmation, execute deletion only after confirmation, and verify the fragment is gone.

Risk: Persistent memory and profile writes can store sensitive or incorrect user information.

Mitigation: Confirm user_id, content, messages, profile schema, and profile value changes before writes; read current values before updates or deletes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-bailian-memory)
- [Alibaba Cloud Bailian Memory Library documentation](https://help.aliyun.com/zh/model-studio/memory-library)
- [Alibaba Cloud long-term memory API reference](https://help.aliyun.com/zh/model-studio/long-term-memory-api-reference)
- [API endpoints](references/api-endpoints.md)
- [RAM policies](references/ram-policies.md)
- [Error handling](references/error-handling.md)
- [Verification method](references/verification-method.md)
- [Acceptance criteria](references/acceptance-criteria.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, API calls]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands invoke Python scripts that print DashScope API JSON; write operations may return asynchronous event IDs.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
