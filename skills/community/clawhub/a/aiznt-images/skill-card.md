## Description:

TS Images provides OpenAI-style image generation and Gemini generateContent image workflows through configured AIZNT proxy endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangshengli0421](https://clawhub.ai/user/wangshengli0421)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to call synchronous or asynchronous image generation flows and Gemini generateContent image models from an environment configured with TS_TOKEN and AIZNT_PROXY_URLS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bearer tokens and prompt or image request data may be sent to unintended configured URLs.

Mitigation: Install only when TS_TOKEN and AIZNT_PROXY_URLS come from a trusted source, and verify each configured URL points to the intended HTTPS service before use.

Risk: Sensitive prompts or source images may be transmitted to the configured image service.

Mitigation: Avoid sending sensitive prompts or images unless required for the task and acceptable under the user's data handling policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangshengli0421/skills/aiznt-images)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill's scripts print JSON responses from configured image generation endpoints.]

## Skill Version(s):

1.0.0 (source: server release and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
