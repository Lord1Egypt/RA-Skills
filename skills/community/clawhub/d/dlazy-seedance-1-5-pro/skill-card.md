## Description: <br>
Convert images into dynamic dance videos using Doubao Seedance 1.5 Pro. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to invoke dLazy's hosted Doubao Seedance 1.5 Pro workflow for image-to-video dance and action generation from prompts and frame inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected image, video, or audio files are sent to dLazy's hosted API and media storage. <br>
Mitigation: Only submit media and prompts that are appropriate for dLazy processing, and treat generated output URLs as potentially sensitive. <br>
Risk: API credentials may be saved in the local dLazy CLI configuration. <br>
Mitigation: Use the DLAZY_API_KEY environment variable or npx for less local persistence, and rotate or revoke keys from the dLazy dashboard when needed. <br>
Risk: The skill depends on the external @dlazy/cli package and dLazy hosted service. <br>
Mitigation: Review the @dlazy/cli package before global installation and install only if the operator is comfortable using dLazy's service. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-seedance-1-5-pro) <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy homepage](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON result examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated media URLs may be returned from files.dlazy.com; asynchronous runs can return a task identifier for later polling.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
