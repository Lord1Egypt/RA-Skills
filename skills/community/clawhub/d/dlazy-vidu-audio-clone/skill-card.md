## Description: <br>
Clone voice and generate new text reading audio with Vidu Audio Clone through the dLazy CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to invoke dLazy's Vidu Audio Clone workflow for voice cloning and text-to-speech generation from prompts and optional audio references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a dLazy API key and stores or accepts credentials for CLI use. <br>
Mitigation: Use per-invocation credentials when appropriate, keep the local config private, and rotate the dLazy API key if it is exposed. <br>
Risk: Prompts and audio files provided to the skill are sent to dLazy-hosted endpoints for processing. <br>
Mitigation: Avoid uploading confidential audio or audio you do not have rights to use, and review dLazy service terms before production use. <br>
Risk: The workflow depends on a third-party npm CLI. <br>
Mitigation: Use the documented npx invocation to avoid a persistent global install, or review the CLI package before installing it globally. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-vidu-audio-clone) <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy homepage](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return hosted generated media URLs or asynchronous task identifiers from the dLazy service.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
