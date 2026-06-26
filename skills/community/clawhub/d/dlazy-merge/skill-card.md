## Description: <br>
Audio/video merging tool for merging multiple video and audio tracks based on clips and timeline config, suitable for final cuts, scoring, and post-production. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, editors, and production teams use this skill to ask an agent to prepare and run dLazy CLI media-merge commands for combining video and audio tracks into generated output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local media paths supplied to the CLI may be uploaded to dLazy-hosted services. <br>
Mitigation: Use the skill only with media that is appropriate to send to dLazy, and avoid sensitive media unless dLazy's terms and controls fit the use case. <br>
Risk: Authentication can persist a dLazy API key in the user's local CLI configuration. <br>
Mitigation: Prefer per-invocation DLAZY_API_KEY or npx when less local persistence is desired, and rotate or revoke keys from the dLazy dashboard when needed. <br>
Risk: The broad merge trigger can lead an agent to prepare or run an unintended media-merge command. <br>
Mitigation: Review the generated dlazy merge command and selected input files before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-merge) <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy homepage](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference asynchronous task IDs or hosted output URLs returned by the dLazy service.] <br>

## Skill Version(s): <br>
1.1.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
