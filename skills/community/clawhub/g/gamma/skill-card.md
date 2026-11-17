## Description:

Generate AI-powered presentations, documents, and social posts using Gamma.app API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucassynnott](https://clawhub.ai/user/lucassynnott)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to create Gamma presentations, pitch decks, documents, reports, and social media carousels from topic or content prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shell wrapper has a confirmed argument-handling flaw that can execute local commands if attacker-controlled options are passed.

Mitigation: Review before installing and avoid untrusted prompts or agent-generated command options until numeric and option fields are validated before API requests or wait loops.

Risk: Submitted content is sent to Gamma's external service.

Mitigation: Avoid regulated, confidential, or secret material unless that use is approved for the configured Gamma account.

## Reference(s):

- [ClawHub Gamma skill page](https://clawhub.ai/lucassynnott/skills/gamma)
- [Gamma API generations endpoint](https://public-api.gamma.app/v1.0/generations)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and Gamma generation URLs or status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GAMMA_API_KEY and sends submitted content to Gamma's external API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
