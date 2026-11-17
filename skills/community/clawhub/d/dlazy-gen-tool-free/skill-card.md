## Description:

A Chinese-language agent skill that guides use of the dlazy CLI for text-to-image generation, basic image editing, foreground segmentation, and super-resolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to generate or edit images through the dlazy CLI for social media visuals, product concept images, personal project assets, foreground extraction, and super-resolution enhancement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to activate for broader AI, chat, orchestration, and automation tasks than its stated image-generation purpose supports.

Mitigation: Use it only for dlazy image generation or image editing tasks, and do not route general chat, agent orchestration, file search, or arbitrary automation requests to it.

Risk: Installing @dlazy/cli globally and running dlazy commands executes third-party code and calls an external service.

Mitigation: Review the package and commands before installation or execution, run them in a restricted environment where practical, and confirm that prompts and files may be sent to the external service.

Risk: The skill requires a dlazy API key, which can be exposed through hardcoded values, shared config files, shell history, or logs.

Mitigation: Prefer the DLAZY_API_KEY environment variable or an approved secret store, avoid committing credentials, and keep local config files limited to the current user.

Risk: Reference images and prompts may contain sensitive or unintended content.

Mitigation: Restrict reference images to intended files and avoid sending sensitive prompts or images unless the deployment policy allows that external processing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/dlazy-gen-tool-free)
- [ClawHub Publisher Profile](https://clawhub.ai/user/thcjp)
- [Artifact Skill Definition](artifact/SKILL.md)
- [dlazy API Key Dashboard](https://dlazy.com/dashboard/organization/api-key)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and Python code blocks plus dlazy CLI result references.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16+, the @dlazy/cli package, a dlazy API key, network access to the dlazy service, and user-provided prompts or reference images.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
