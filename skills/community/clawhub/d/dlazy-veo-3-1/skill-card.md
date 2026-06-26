## Description: <br>
Generate high-quality cinematic effects videos with Google Veo 3.1. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate or extend cinematic videos from prompts, images, or video inputs through the dLazy CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a dLazy API key and can store it in the local CLI configuration. <br>
Mitigation: Use an organization-scoped key, rotate or revoke it when needed, and prefer per-invocation environment variables when persistent local storage is not desired. <br>
Risk: Prompts and user-selected media files are sent to dLazy hosted endpoints for generation. <br>
Mitigation: Avoid private or sensitive prompts and media unless the user intends to upload them to the dLazy service. <br>
Risk: The skill depends on the external @dlazy/cli package. <br>
Mitigation: Use the pinned @dlazy/cli version from the skill metadata and prefer npx for on-demand execution when a persistent global binary is unnecessary. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dlazyai/dlazy-veo-3-1) <br>
- [dLazy Homepage](https://dlazy.com) <br>
- [dLazy CLI Repository](https://github.com/dlazyai/cli) <br>
- [@dlazy/cli npm Package](https://www.npmjs.com/package/@dlazy/cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown instructions with shell commands and JSON result examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The generated media is returned through dLazy result URLs; async mode can return a task identifier for polling.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
