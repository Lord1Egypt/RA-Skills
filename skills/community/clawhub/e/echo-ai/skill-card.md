## Description:

Connect to Echo AI, a customer interaction platform, to list assistants, retrieve knowledge bases, and chat with AI-powered Echos built by businesses and creators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darthdens](https://clawhub.ai/user/darthdens)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to connect an agent to Echo AI assistants for customer support, sales, knowledge-base lookup, and confirmed chat interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses ECHO_API_KEY to access Echo AI on the user's behalf.

Mitigation: Keep ECHO_API_KEY private and prefer assistant-scoped keys when possible.

Risk: Chat requests send user messages to Echo AI and may consume the Echo owner's credits.

Mitigation: Approve chat requests only when comfortable sending the message to Echo AI and consuming credits.

## Reference(s):

- [Echo AI](https://echoai.so)
- [Echo API Documentation](https://echoai.so/help)
- [Echo AI API Reference](references/api-reference.md)
- [OpenClaw Skills Documentation](https://docs.openclaw.ai/skills)
- [ClawHub Skill Page](https://clawhub.ai/darthdens/skills/echo-ai)
- [Publisher Profile](https://clawhub.ai/user/darthdens)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Markdown, Configuration]

**Output Format:** [Markdown guidance with HTTP request examples and JSON response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses ECHO_API_KEY for authenticated Echo AI requests; chat calls require user confirmation and may consume credits.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
