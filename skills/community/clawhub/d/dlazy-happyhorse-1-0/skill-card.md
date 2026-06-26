## Description: <br>
Happy Horse 1.0 is a dLazy CLI skill for text-to-video, first-frame-to-video, reference-to-video, and video editing through the hosted dLazy API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agents use this skill to generate or edit videos with Happy Horse 1.0 from prompts, images, or video inputs using the dLazy CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a dLazy API key and can store credentials in the local CLI configuration. <br>
Mitigation: Use scoped API keys, rotate or revoke keys when needed, and review local credential storage before use on shared systems. <br>
Risk: Prompts and local media paths supplied to the CLI are sent to dLazy API and file-hosting endpoints for processing. <br>
Mitigation: Avoid submitting sensitive prompts or media unless the dLazy service terms and data handling meet the deployment requirements. <br>
Risk: The release uses third-party CLI tooling from the publisher. <br>
Mitigation: Review the publisher profile, package, and source references before installation in sensitive environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-happyhorse-1-0) <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy homepage](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Files, Guidance] <br>
**Output Format:** [JSON responses with generated media URLs, plus shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return asynchronous task identifiers when --no-wait is used; generated media URLs are hosted by dLazy.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
