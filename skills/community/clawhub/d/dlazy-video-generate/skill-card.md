## Description: <br>
Dlazy Video Generate helps an agent select and run an appropriate dLazy CLI video model from a user prompt. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and creative operators use this skill to route video-generation requests to dLazy CLI models for text-to-video, image-to-video, lip-sync, segmentation, and related video workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses dLazy cloud services, so prompts and user-provided media paths may be uploaded for generation. <br>
Mitigation: Use it only when uploading those prompts and media to dLazy is acceptable for the user's data-handling requirements. <br>
Risk: The CLI requires a dLazy API key that may be saved in the local user configuration. <br>
Mitigation: Prefer per-invocation credentials or rotate and revoke saved API keys when they are no longer needed. <br>
Risk: Generation may consume paid dLazy credits. <br>
Mitigation: Confirm account credit availability before running workflows that may incur cost. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-video-generate) <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke cloud video generation and return dLazy-hosted media URLs through the CLI.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
