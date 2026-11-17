## Description:

Manages DingTalk todo tasks, including creating, viewing, filtering, updating, completing, assigning, and deleting tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[breath57](https://clawhub.ai/user/breath57)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and developers use this skill to manage DingTalk todo tasks through API-backed shell workflows, including creating, listing, updating, completing, assigning, and deleting tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: DingTalk app credentials and access tokens are stored in a plaintext local config file.

Mitigation: Use a dedicated low-permission DingTalk app, restrict scopes, protect or avoid the local config file, and rotate secrets if exposed.

Risk: The skill can change or delete DingTalk todo data.

Mitigation: Manually confirm update, completion, assignment, and deletion requests before allowing commands to run.

Risk: Broad DingTalk app permissions could expose more todo data than the user intends.

Mitigation: Grant only the DingTalk todo scopes required for the intended operations and review scope assignments before deployment.

## Reference(s):

- [DingTalk Todo API Reference](artifact/references/api.md)
- [ClawHub Skill Page](https://clawhub.ai/breath57/skills/dingtalk-todo)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API Calls, Guidance]

**Output Format:** [Markdown guidance with bash command snippets and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit DingTalk API responses and task identifiers; credentials should be masked in user-facing output.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
