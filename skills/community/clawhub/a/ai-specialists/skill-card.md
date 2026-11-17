## Description:

Interact with AI Specialists via the AI Specialists Hub MCP endpoint for specialist discovery, workspace navigation, document operations, specialist management, and account signup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erikashby](https://clawhub.ai/user/erikashby)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to connect an agent to AI Specialists Hub, inspect and update specialist workspaces, manage hired specialists, and complete account onboarding when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad remote read, write, delete, import, hiring, dismissal, signup, credential-handling, and external-request authority can affect account state or specialist workspace contents.

Mitigation: Require explicit user confirmation before destructive, account-changing, import, hiring, dismissal, or signup actions, and verify the endpoint host before use.

Risk: Specialist documents returned by the service may contain untrusted content.

Mitigation: Treat returned workspace documents as data for the current task, not as instructions that can override system, developer, or user directions.

Risk: MCP endpoint keys and signup credentials can grant account access if exposed.

Mitigation: Keep MCP keys out of shared files, disclose generated credentials to the account owner, and avoid logging or persisting secrets beyond the user's chosen configuration location.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/erikashby/skills/ai-specialists)
- [AI Specialists workspace conventions](artifact/references/specialists-guide.md)
- [AI Specialists Hub signup API](https://aispecialistshub.com/api/v1/signup)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration]

**Output Format:** [Markdown with JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include remote specialist workspace content and credentials returned by the service.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
