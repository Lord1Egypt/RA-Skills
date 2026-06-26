## Description: <br>
A comprehensive generation skill that can generate images, videos, and audio by automatically selecting the appropriate dLazy CLI model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and content teams use this skill to ask an agent to choose and run the appropriate dLazy CLI model for image, video, or audio generation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, parameters, and referenced media files may be sent to dLazy services for cloud generation. <br>
Mitigation: Use the skill only with content approved for dLazy processing, and avoid sensitive prompts or media unless the user has accepted that data flow. <br>
Risk: The skill requires a dLazy API key, which may be stored in local CLI configuration or supplied through the environment. <br>
Mitigation: Prefer per-invocation environment credentials or npx when persistent local credentials or a global install are not desired, and rotate or revoke keys from the dLazy dashboard when needed. <br>
Risk: Generation requests can consume paid credits, and the trigger wording covers broad image, video, and audio requests. <br>
Mitigation: Confirm the intended media type, model, and command before execution when cost or quota impact is a concern. <br>


## Reference(s): <br>
- [dLazy homepage](https://dlazy.com) <br>
- [@dlazy/cli npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy CLI repository listed in release metadata](https://github.com/dlazyai/cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI output references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The invoked dLazy CLI may return hosted media URLs and JSON envelopes for generated image, video, or audio outputs.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
