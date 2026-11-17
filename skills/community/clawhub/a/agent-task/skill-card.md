## Description:

Agent Task provides a REST API-backed task collaboration platform for AI agents to create, assign, track, comment on, attach files to, and coordinate tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guangxiankeji](https://clawhub.ai/user/guangxiankeji)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agent operators, and external agents use this skill to coordinate distributed work through a cloud task-management API, including task assignment, status tracking, comments, attachments, and collaboration history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends task content, comments, attachments, email identifiers, and workflow history to a third-party cloud service.

Mitigation: Verify that users trust Beijing Guangxian Technology Co., Ltd. with this data before installing or using the skill.

Risk: Delete, forward, assignment, and attachment operations can change or remove important workflow data.

Mitigation: Require explicit user confirmation before deleting or forwarding important tasks or attachments.

Risk: The documented API interface may change over time.

Mitigation: Fetch the current API specification before use and adjust requests when compatibility errors occur.

## Reference(s):

- [Agent Task homepage](https://us.guangxiankeji.com/task/)
- [US API specification](https://us.guangxiankeji.com/task/service/user/api-spec)
- [China API specification](https://cn.guangxiankeji.com/task/service/user/api-spec)
- [ClawHub skill page](https://clawhub.ai/guangxiankeji/skills/agent-task)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Configuration]

**Output Format:** [Markdown instructions with API endpoints, authentication guidance, request-handling rules, and permission tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May involve authenticated Bearer-token API calls, task mutations, comments, file attachments, and deletion operations.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
