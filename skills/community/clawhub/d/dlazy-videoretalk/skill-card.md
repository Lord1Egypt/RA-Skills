## Description: <br>
Dlazy Videoretalk helps an agent use Tongyi VideoRetalk to regenerate a talking-person video so the speaker's mouth movement matches a provided audio track, with an optional reference face image for multi-person videos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to invoke dLazy's hosted VideoRetalk service for lip-syncing a person video to new speech. It is intended for workflows that can send the selected media and parameters to dLazy's hosted API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected video, audio, optional face image, prompts, and parameters are sent to dLazy's hosted service. <br>
Mitigation: Use the skill only for media that can be shared with dLazy's API, and avoid sensitive or non-consensual media. <br>
Risk: A dLazy API key is required and may be stored in the local CLI configuration or supplied by environment variable. <br>
Mitigation: Keep the key scoped to the intended organization, restrict local config access, and rotate or revoke the key if it is exposed. <br>
Risk: The skill depends on the third-party @dlazy/cli package. <br>
Mitigation: Prefer on-demand npx execution or review the package/source before global installation. <br>
Risk: The security summary notes documentation mistakes in examples. <br>
Mitigation: Check current command options with dlazy videoretalk -h and use dry-run behavior where appropriate before paid or sensitive generation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-videoretalk) <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy homepage](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The invoked CLI may return hosted media URLs or an asynchronous generateId for later polling.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
