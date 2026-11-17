## Description:

Manage task lists via cognary-cli, including listing, adding, updating, completing, uncompleting, and deleting tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dboyne](https://clawhub.ai/user/dboyne)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to manage Cognary task lists through cognary-cli, including viewing, creating, updating, completing, reactivating, and deleting tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install an unpinned global CLI.

Mitigation: Install cognary-cli only from a version and publisher the user trusts.

Risk: The skill requires an API key for Cognary task access.

Mitigation: Configure COGNARY_API_KEY through a local secret mechanism rather than chat.

Risk: The skill can mutate or delete external tasks.

Mitigation: Require explicit user confirmation before update, completion, uncompletion, or deletion commands.

## Reference(s):

- [Cognary Tasks ClawHub listing](https://clawhub.ai/dboyne/skills/cognary-ai-tasks)
- [dboyne ClawHub publisher profile](https://clawhub.ai/user/dboyne)
- [Cognary Tasks web app](https://tasks.cognary.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown summaries with CLI commands and JSON-backed task results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires cognary-cli and COGNARY_API_KEY for task API access.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
