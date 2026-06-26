## Description: <br>
Dlazy Motion Graphics helps create code-driven motion graphics, kinetic typography, animated text videos, animated infographics, and explainer animations using Remotion code rather than AI-generated footage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and external users use this skill to start or continue hosted dLazy motion-graphics projects for animated text, data-driven visuals, logo animations, transitions, infographics, and explainer videos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a dLazy API key and stores credentials in local CLI configuration unless an environment variable is used. <br>
Mitigation: Use scoped organization keys, restrict local config file access, rotate or revoke keys from the dLazy dashboard when access changes, and avoid pasting secrets into prompts or logs. <br>
Risk: The skill sends prompts and selected file attachments to dLazy hosted API and file-storage endpoints. <br>
Mitigation: Review files before using --files, avoid sending sensitive or regulated content unless approved for that service, and confirm organizational policies before use. <br>
Risk: The skill asks the agent to run CLI commands that may install or invoke @dlazy/cli. <br>
Mitigation: Use the pinned package version in the skill metadata, review proposed commands before execution, and prefer npx for one-off use when a persistent global install is not needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-motion-graphics) <br>
- [dLazy homepage](https://dlazy.com) <br>
- [dLazy CLI source repository](https://github.com/dlazyai/cli) <br>
- [@dlazy/cli npm package](https://www.npmjs.com/package/@dlazy/cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May stream hosted agent replies; files attached with --files are uploaded to dLazy storage before use.] <br>

## Skill Version(s): <br>
1.2.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
