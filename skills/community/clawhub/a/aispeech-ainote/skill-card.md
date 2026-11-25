## Description:

Connects OpenClaw with 思必驰 AI office notebooks and recording cards to manage notes, paper notebooks, todos, personal and label knowledge, and hotwords.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fairylong](https://clawhub.ai/user/fairylong)

### License/Terms of Use:

MIT-0

## Use Case:

Employees using 思必驰 AI office notebooks or recording cards can retrieve and manage notes, paper notebooks, and todos; search personal and label knowledge; and manage hotwords.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill accesses personal notebook, note, and todo data using an authorization token.

Mitigation: Protect AIWORK_AUTH_TOKEN in the OpenClaw environment and grant only the scopes needed for the requested tasks.

Risk: The skill documents operations that delete notes, note groups, and todos.

Mitigation: Confirm the target item and intended deletion before invoking a delete operation.

## Reference(s):

- [API Reference](api_reference.md)
- [API Details](references/api-details.md)
- [AIWorks](https://aiworks.cn)
- [ClawHub Release](https://clawhub.ai/fairylong/skills/aispeech-ainote)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Natural-language responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may contain personal notebook, note, and todo information.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
