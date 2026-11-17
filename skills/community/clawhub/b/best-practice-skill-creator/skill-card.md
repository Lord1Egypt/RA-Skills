## Description:

Create OpenClaw skills from best practice videos or image sequences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diffusefuturetech](https://clawhub.ai/user/diffusefuturetech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation authors use this skill to turn best practice videos, screenshots, and task descriptions into OpenClaw skill directories for review, installation, or publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default configuration includes a plaintext API key.

Mitigation: Remove the bundled key, rotate it if it belongs to you, and provide secrets through environment variables or a trusted secret store.

Risk: Screenshots or video frames may be sent to a nonstandard remote endpoint.

Mitigation: Use a trusted provider endpoint and process only media that is safe to disclose to that provider.

Risk: Generated SKILL.md output may contain incorrect or unsafe agent instructions.

Mitigation: Manually inspect and scan generated skill files before installing or publishing them.

## Reference(s):

- [Best Practice Skill Creator on ClawHub](https://clawhub.ai/diffusefuturetech/skills/best-practice-skill-creator)
- [Configured OpenAI-compatible endpoint](https://api.cloubic.com/v1)
- [Configured Gemini API endpoint](https://generativelanguage.googleapis.com/v1beta)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Generated OpenClaw skill directory containing SKILL.md frontmatter and instruction content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires media input, a task description, and a configured multimodal LLM provider.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
