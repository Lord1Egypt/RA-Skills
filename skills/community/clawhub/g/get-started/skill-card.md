## Description:

Connect to Flow Relay, inspect accessible workspaces and projects, set the active project and choose the first workflow. Use right after installing the plugin or when no active project is selected.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flow-relay](https://clawhub.ai/user/flow-relay)

### License/Terms of Use:

MIT-0

## Use Case:

Flow Relay users can use this skill after installation or when no active project is selected. It helps them inspect accessible workspaces, select a project, and choose a first workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selecting a project changes the active project context for the session.

Mitigation: Confirm the user's choice and ask before setting a project active when they have not requested a switch.

Risk: Workspace access and available actions depend on the user's OAuth consent scopes.

Mitigation: If a scope error occurs, explain which permission is needed and do not retry blindly.

## Reference(s):

- [Get Started on ClawHub](https://clawhub.ai/flow-relay/skills/get-started)
- [Flow Relay publisher profile](https://clawhub.ai/user/flow-relay)

## Skill Output:

**Output Type(s):** [API Calls, Guidance, Text]

**Output Format:** [Conversational guidance and Flow Relay tool calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
