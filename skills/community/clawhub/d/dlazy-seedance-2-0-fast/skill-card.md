## Description: <br>
Fast version of ByteDance's Seedance 2.0. Generates videos faster with support for multi-modal references, first/last frame, and text-to-video. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent users use this skill to invoke dLazy's Seedance 2.0 Fast video generation through the dLazy CLI, supplying prompts and optional image, video, audio, first-frame, or last-frame references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive dLazy API credentials for normal operation. <br>
Mitigation: Review requested permissions before use, store the key with the dLazy CLI or DLAZY_API_KEY only as needed, and rotate or revoke organization keys when access should change. <br>
Risk: Prompts and local media references supplied to the CLI may be sent to dLazy API and storage endpoints. <br>
Mitigation: Avoid submitting sensitive media or confidential prompts unless the dLazy service terms and organization policy permit that workflow. <br>


## Reference(s): <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [@dlazy/cli npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy homepage](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Hosted media URLs] <br>
**Output Format:** [JSON response from the dlazy CLI with generated output URLs or async task status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a dLazy API key. Local media paths passed as inputs may be uploaded to dLazy-hosted storage for generation.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
