## Description: <br>
Powerful video generation with Kling v3, supporting high-quality text-to-video and image-to-video workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, marketers, and developers use this skill to invoke dLazy's Kling v3 hosted API for text-to-video and image-to-video generation through the dLazy CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a dLazy API key and may store it in the local dLazy CLI configuration. <br>
Mitigation: Use the documented login or per-invocation environment variable flow, keep the config file restricted to the OS user, and rotate or revoke the key from the dLazy dashboard if needed. <br>
Risk: Prompts and selected local media files are sent to dLazy cloud endpoints for generation. <br>
Mitigation: Confirm prompts and files are appropriate to share with dLazy before upload, and avoid passing sensitive local media paths. <br>
Risk: Using the skill runs a third-party CLI package. <br>
Mitigation: Prefer the npx path or review the @dlazy/cli package before installing it globally. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-kling-v3) <br>
- [dLazy CLI homepage](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy website](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Generated media URLs, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON CLI responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires npm or npx and a dLazy API key; local media paths may be uploaded to dLazy for generation.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
