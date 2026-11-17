## Description:

Deepseek V3 Lite Agent helps an assistant adopt a DeepSeek-V3 content-creator persona for content creation tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvinecarn](https://clawhub.ai/user/alvinecarn)

### License/Terms of Use:


## Use Case:

External users and developers can use this prompt-only skill to steer an agent toward content creation in a DeepSeek-branded creator persona.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The persona wording may make outputs sound branded or role-specific in contexts where that is not intended.

Mitigation: Review the identity-style wording before deployment and adjust it to match the intended assistant identity.

Risk: Template variables such as $DATE$ may remain visible if runtime substitution is not configured.

Mitigation: Confirm template substitution behavior or remove unresolved variables before release.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/alvinecarn/skills/deepseek-v3-lite-agent)
- [ClawHub Publisher Profile](https://clawhub.ai/user/alvinecarn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt-only persona guidance; no artifact evidence of code execution, tools, persistence, or data access.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
