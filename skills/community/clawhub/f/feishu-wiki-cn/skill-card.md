## Description:

Manage Feishu Wiki knowledge bases by listing spaces, viewing, creating, moving, and renaming wiki pages with appropriate permissions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erick0309](https://clawhub.ai/user/erick0309)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Feishu workspace users use this skill to inspect wiki spaces and nodes, retrieve page content, and manage wiki organization through authorized create, move, and rename actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access Feishu wiki content through the user's account permissions.

Mitigation: Install it only when the agent should access that Feishu wiki data, and use an account with appropriate wiki permissions.

Risk: Create, move, and rename actions can change shared knowledge base structure or content.

Mitigation: Review proposed create, move, and rename actions before approving them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/erick0309/skills/feishu-wiki-cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Guidance]

**Output Format:** [Markdown or text responses with Feishu wiki tool calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, move, or rename wiki nodes when the user approves the action and account permissions allow it.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
