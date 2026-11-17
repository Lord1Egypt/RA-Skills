## Description:

Manage conversations and sessions in Google Dialogflow CX via REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yash-kavaiya](https://clawhub.ai/user/yash-kavaiya)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to test Dialogflow CX conversation sessions, detect or match intents, and create conversation test cases through REST API examples and a small Python CLI wrapper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected conversation text may be sent to Google Dialogflow CX with the user's Google credentials.

Mitigation: Use only projects with appropriate data controls, avoid sensitive or regulated content unless approved, and confirm the target agent and session before sending messages.

Risk: Bearer tokens and service-account files are required for authenticated API use.

Mitigation: Treat access tokens and service-account JSON files as secrets, keep them out of prompts and logs, and prefer short-lived credentials where possible.

## Reference(s):

- [Conversations & Testing API Reference](references/conversations.md)
- [ClawHub skill page](https://clawhub.ai/yash-kavaiya/skills/dialogflow-cx-conversations)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with REST examples, shell commands, and Python CLI usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce API request examples that send selected conversation text to Google Dialogflow CX using the user's credentials.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
