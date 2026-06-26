## Description: <br>
Extracts the first frame and audio from a video, analyzes it with a prompt, and returns a Seedance 2.0 replicate bundle. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and creators use this skill to call the dLazy hosted video-replicate workflow from an agent, supplying video inputs and receiving generated media outputs or async task IDs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a dLazy API key and may store it in local CLI configuration. <br>
Mitigation: Use organization-scoped keys, keep local config access restricted to the OS user, and rotate or revoke keys from the dLazy dashboard when needed. <br>
Risk: Video, image, or audio paths passed to the CLI may be uploaded to dLazy hosted services for processing. <br>
Mitigation: Only submit media approved for third-party processing and avoid passing sensitive local files unless the user has confirmed the upload. <br>
Risk: The skill relies on npm or npx execution of a third-party CLI. <br>
Mitigation: Review commands before running them and prefer documented safer modes such as dry-run or explicit confirmation when broad local authority is not needed. <br>


## Reference(s): <br>
- [Dlazy Video Replicate on ClawHub](https://clawhub.ai/dlazyai/dlazy-video-replicate) <br>
- [dLazy](https://dlazy.com) <br>
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with bash commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the dLazy CLI and may return hosted media URLs, synchronous JSON outputs, or async task IDs.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
