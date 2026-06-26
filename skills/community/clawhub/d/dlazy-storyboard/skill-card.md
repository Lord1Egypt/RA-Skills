## Description: <br>
Dlazy Storyboard helps an agent use the dLazy hosted storyboard workflow to turn scripts, characters, shot prompts, reference frames, voice, music, sound effects, and subtitles into a multi-shot animated short. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, creators, and developers use this skill to start or continue project-scoped dLazy storyboard sessions from an agent, including attaching local reference files when needed. It is intended for multi-shot animated shorts where character consistency and staged video assembly matter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and attached files are sent to dLazy as a third-party hosted service. <br>
Mitigation: Install and use the skill only when that data handling is acceptable for the task; avoid sending sensitive prompts or files unless approved. <br>
Risk: The skill requires a dLazy API key that may be stored in local CLI configuration. <br>
Mitigation: Use the documented dLazy login or auth setup, protect the local config, and rotate or revoke the key from the dLazy dashboard if needed. <br>
Risk: A global CLI install persists a third-party command on the system. <br>
Mitigation: Use the pinned npx command when a non-persistent CLI invocation is preferred. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/dlazyai/dlazy-storyboard) <br>
- [Publisher profile](https://clawhub.ai/user/dlazyai) <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy homepage](https://dlazy.com) <br>
- [dLazy API key dashboard](https://dlazy.com/dashboard/organization/api-key) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and streamed CLI responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a pinned dLazy CLI invocation; prompts and attached files may be sent to the dLazy hosted service and project context can continue across turns.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
