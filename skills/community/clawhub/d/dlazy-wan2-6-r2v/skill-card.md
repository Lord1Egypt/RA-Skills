## Description: <br>
Accurately generate continuous videos based on reference images using Wan 2.6 R2V. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative users use this skill to invoke dLazy's hosted Wan 2.6 R2V workflow for reference-image-to-video generation from an agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a third-party npm CLI and a dLazy API key. <br>
Mitigation: Use the pinned CLI version or npx for one-off runs, keep the API key private, and rotate or revoke it from the dLazy dashboard if needed. <br>
Risk: Prompts and selected local media paths may be sent to dLazy's cloud service for generation. <br>
Mitigation: Avoid passing private or sensitive media that should not be uploaded to dLazy. <br>
Risk: Cloud generation can consume dLazy API credits. <br>
Mitigation: Use dry-run or monitor account usage before running large or repeated generation jobs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-wan2-6-r2v) <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy service](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with bash commands and JSON CLI responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return generated media URLs or asynchronous task IDs from dLazy.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
