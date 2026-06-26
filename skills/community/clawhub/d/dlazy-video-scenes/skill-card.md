## Description: <br>
Detects and splits videos into scene clips through the dLazy CLI and returns hosted clip URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content automation teams use this skill to call dLazy video scene processing from an agent workflow, authenticate with a dLazy API key, and receive clip URLs or asynchronous task handles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected videos, prompts, and parameters may be sent to dLazy hosted services. <br>
Mitigation: Use only media and prompts approved for dLazy processing, and avoid highly sensitive videos unless the processing pipeline is clarified. <br>
Risk: The documentation conflicts about whether the service only splits scenes or also performs video understanding. <br>
Mitigation: Treat the processing behavior as uncertain and validate it with the publisher before using the skill for sensitive or regulated media. <br>
Risk: A dLazy API key may be stored locally for CLI authentication. <br>
Mitigation: Use the documented key rotation and revocation controls, restrict local config access, or provide the key per invocation with DLAZY_API_KEY when appropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-video-scenes) <br>
- [dLazy homepage](https://dlazy.com) <br>
- [@dlazy/cli npm package](https://www.npmjs.com/package/@dlazy/cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a dLazy API key; selected video inputs, prompts, and parameters may be sent to dLazy hosted services and result URLs may be hosted on files.dlazy.com.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata; artifact frontmatter lists 1.1.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
