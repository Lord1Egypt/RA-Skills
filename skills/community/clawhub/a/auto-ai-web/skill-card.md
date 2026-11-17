## Description:

Auto-AI Web Bridge helps an agent use Claude AI for code tasks and Gemini for image generation through their web interfaces when official APIs are unavailable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[metiu1](https://clawhub.ai/user/metiu1)

### License/Terms of Use:


## Use Case:

Developers and agent users can use this skill to route code generation, code analysis, and image-generation requests to logged-in Claude AI or Gemini web sessions when direct API access is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may prompt users for Claude or Gemini credentials and may use logged-in web sessions.

Mitigation: Users should log in directly through the provider-controlled browser and avoid sharing passwords, MFA codes, cookies, or recovery credentials with the agent.

Risk: Prompts, source code, or generated content may be sent to external AI providers.

Mitigation: Avoid using this skill with secrets, proprietary source, customer data, or regulated information unless explicitly approved.

Risk: The security verdict is suspicious because the skill combines credential handling guidance with automatic web submission to third-party AI services.

Mitigation: Review the skill before deployment and restrict use to environments where third-party web AI services are permitted.

## Reference(s):

- [Auto-AI Web Bridge on ClawHub](https://clawhub.ai/metiu1/skills/auto-ai-web)
- [Claude AI](https://claude.ai)
- [Gemini](https://gemini.google.com)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown with code blocks and generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save generated image files to the configured downloads folder.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
