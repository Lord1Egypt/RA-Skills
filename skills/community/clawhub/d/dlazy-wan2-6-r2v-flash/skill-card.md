## Description: <br>
Dlazy Wan2.6 R2v Flash helps agents generate dynamic short videos from reference images using Wan 2.6 Flash. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, developers, and agents use this skill to generate short videos from reference images through the dLazy CLI and hosted Wan 2.6 Flash API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and referenced media files may be sent to dLazy's hosted API and media storage. <br>
Mitigation: Confirm the user intends to use dLazy's hosted service before invocation and avoid sending sensitive media unless approved. <br>
Risk: The skill requires a dLazy API key and may consume account credits. <br>
Mitigation: Use the documented dLazy authentication flow, keep the key scoped to the user's organization, and rotate or revoke it from the dLazy dashboard if needed. <br>
Risk: A global CLI install persists a local executable and configuration. <br>
Mitigation: Prefer the pinned npx invocation or review the pinned CLI source before installing globally. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-wan2-6-r2v-flash) <br>
- [dLazy CLI repository](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown instructions with inline shell commands and JSON API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a dLazy API key; may upload prompts and referenced media to dLazy and return hosted output URLs.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
