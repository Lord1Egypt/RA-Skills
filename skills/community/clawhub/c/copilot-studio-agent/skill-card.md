## Description:

Create and configure custom agents in Microsoft Copilot Studio through guided web app steps covering triggers, knowledge, tools, topics, authentication, testing, and publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[saikiranparamkusham09](https://clawhub.ai/user/saikiranparamkusham09)

### License/Terms of Use:


## Use Case:

Makers, consultants, and developers use this skill to plan and configure Microsoft Copilot Studio agents, including agent basics, topics, triggers, knowledge sources, Power Automate tools, authentication, testing, and publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Event triggers and Power Automate actions can run with the agent maker's credentials, which may expose data or perform actions under the wrong account.

Mitigation: Confirm which account supplies credentials for each action, prefer user-scoped permissions where available, and review run-only permissions before publishing.

Risk: Autonomous triggers can broaden data exposure and increase Copilot Credits billing after publication.

Mitigation: Limit trigger scope, test trigger behavior before publishing, and review data exposure and billing impact for the target environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/saikiranparamkusham09/skills/copilot-studio-agent)
- [Microsoft Learn: Create an agent in Copilot Studio](https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-first-bot)
- [Microsoft Learn training: Build initial agent training](https://learn.microsoft.com/en-us/training/modules/create-copilots-copilot-studio/)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with numbered steps, tables, and documentation links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; no code, files, shell commands, or API calls are generated.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
