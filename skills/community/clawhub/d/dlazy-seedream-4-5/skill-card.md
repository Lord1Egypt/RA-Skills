## Description: <br>
Generate smooth, high-quality videos with Doubao Seedream 4.5, supporting text-to-video and image-to-video workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to invoke the dLazy Seedream 4.5 video-generation CLI for prompt-based or image-guided media generation. It is suited for agents that need to prepare commands, configure authentication, and return generation results from the dLazy hosted API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a dLazy API key and can send prompts, parameters, and referenced local media to dLazy services. <br>
Mitigation: Use the skill only when the user intends to call dLazy, protect API keys, and avoid submitting sensitive media or prompts unless that upload is acceptable. <br>
Risk: The install command uses @dlazy/cli@latest, so the installed CLI behavior can change over time. <br>
Mitigation: Review the dLazy CLI source or npm package before installation and consider pinning a vetted CLI version in controlled deployments. <br>
Risk: Video generation can consume paid credits or return asynchronous task identifiers instead of completed outputs. <br>
Mitigation: Use --dry-run when appropriate to check cost, and poll asynchronous tasks with dlazy status when --no-wait is used. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-seedream-4-5) <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy homepage](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, JSON, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return hosted media URLs or asynchronous task identifiers from dLazy services.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
