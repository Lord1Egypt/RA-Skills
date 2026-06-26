## Description: <br>
Dlazy Audio Generate selects an appropriate dLazy CLI audio, music, sound effect, text-to-speech, or voice-cloning model for a user's prompt. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agent users use this skill to generate audio outputs through the dLazy CLI, including text-to-speech, music, sound effects, dialogue, and voice-clone workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a dLazy API key and stores or reads credentials through the dLazy CLI configuration or DLAZY_API_KEY. <br>
Mitigation: Use only trusted dLazy accounts, rotate or revoke keys from the dLazy dashboard when needed, and avoid sharing logs that may expose credentials. <br>
Risk: Prompts, parameters, and referenced media files may be sent to dLazy API and file-hosting endpoints. <br>
Mitigation: Confirm each local file path before upload and avoid submitting sensitive, confidential, or regulated media unless approved for dLazy processing. <br>
Risk: The artifact instructs agents to run broad dLazy CLI commands and the security summary says the instructions are broader than an audio-only skill. <br>
Mitigation: Prefer explicit audio-specific subcommands, review command help before execution, and consider npx or a pinned reviewed CLI version instead of a persistent global install. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-audio-generate) <br>
- [dLazy CLI homepage](https://github.com/dlazyai/cli) <br>
- [@dlazy/cli npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy service homepage](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI JSON result references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides selection and execution of dLazy CLI subcommands; generated media is returned through dLazy-hosted output URLs.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
