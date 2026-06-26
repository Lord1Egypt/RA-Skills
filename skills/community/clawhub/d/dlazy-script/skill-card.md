## Description: <br>
Storyboard script generator that sends a brief and optional reference images to the dLazy CLI/API and returns structured storyboard script data plus a flat canvas shape list. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and creative teams use this skill to generate storyboard scripts from text prompts and optional image references through the dLazy service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A broad trigger word could cause unintended invocation of cloud API calls or file uploads. <br>
Mitigation: Review auto-invocation settings before installing and invoke the skill only when storyboard generation through dLazy is intended. <br>
Risk: Prompts and referenced local files may be sent to dLazy services. <br>
Mitigation: Use the skill only with data appropriate for dLazy processing and avoid passing sensitive local files unless that transfer is acceptable. <br>
Risk: The skill requires a dLazy API key that can be stored in local CLI configuration. <br>
Mitigation: Prefer the DLAZY_API_KEY environment variable when a persistent local credential is not desired, and rotate or revoke keys from the dLazy dashboard as needed. <br>


## Reference(s): <br>
- [ClawHub Dlazy Script release](https://clawhub.ai/dlazyai/dlazy-script) <br>
- [dLazy homepage](https://dlazy.com) <br>
- [dLazy CLI repository](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON returned by the dLazy CLI, with command and authentication guidance in Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return an asynchronous task identifier when invoked with --no-wait; local image inputs may be uploaded to dLazy media storage.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata; artifact frontmatter says 1.1.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
