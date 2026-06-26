## Description: <br>
Fast response and generation of short videos with Google Veo 3.1 Fast. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to invoke the dLazy CLI for Google Veo 3.1 Fast short video generation from text, image frames, or video-extension inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive credentials for the dLazy API and stores authentication in local CLI configuration or accepts DLAZY_API_KEY per invocation. <br>
Mitigation: Install and run it only in an environment intended for dLazy access, rotate or revoke API keys from the dLazy dashboard when needed, and avoid exposing local CLI configuration to unrelated agents. <br>
Risk: The authoritative security verdict is suspicious and warns about high-authority workflows and approval bypass in the scanned skill set. <br>
Mitigation: Review commands before execution, avoid approval-bypass modes, and limit the environment to credentials and account permissions that are appropriate for the requested generation task. <br>
Risk: Prompts and referenced local media files are sent to dLazy API and file-hosting endpoints for processing. <br>
Mitigation: Do not submit confidential or restricted prompts, images, videos, or audio unless the user has approved use of the external dLazy service. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dlazyai/dlazy-veo-3-1-fast) <br>
- [dLazy CLI Source](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm Package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy Homepage](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, JSON, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return generated media URLs or an asynchronous task identifier from the dLazy service.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
