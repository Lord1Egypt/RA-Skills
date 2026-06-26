## Description: <br>
ElevenLabs text-to-sound model - generates 1-22s short sound effects from a description. Suitable for foley, ambience, alerts, and game SFX. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and audio creators use this skill to call dLazy's ElevenLabs sound-effects generation service for short foley, ambience, alert, and game SFX from text prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a dLazy API key, which may be stored in local CLI configuration or supplied through an environment variable. <br>
Mitigation: Use the CLI only on trusted machines, prefer temporary environment variables for one-off use, and rotate or revoke the key when access is no longer needed. <br>
Risk: Prompts and explicitly provided media files are sent to dLazy-hosted services for generation. <br>
Mitigation: Avoid sending confidential or restricted content unless the user has approved that service use and data handling. <br>
Risk: Global installation adds a third-party npm CLI to the environment. <br>
Mitigation: Use npx @dlazy/cli@latest for one-off runs when a persistent global install is not needed, and review the third-party package before persistent installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-elevenlabs-sfx) <br>
- [dLazy CLI repository](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy website](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration guidance, JSON] <br>
**Output Format:** [Markdown guidance with bash commands and JSON CLI results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a dLazy API key; generated result URLs are hosted by files.dlazy.com.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
