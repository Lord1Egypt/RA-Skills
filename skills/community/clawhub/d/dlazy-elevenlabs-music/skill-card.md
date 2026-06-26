## Description: <br>
ElevenLabs music_v1 model generates 10-300 second original music from a natural-language prompt for background music, ads, and short-video soundtracks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate short original music through the dLazy CLI and hosted music generation service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a hosted dLazy API and stores or reads a dLazy API key for authenticated requests. <br>
Mitigation: Install only if you are comfortable with the hosted service, prefer npx for non-persistent CLI use, and rotate or revoke the API key from the dLazy dashboard when needed. <br>
Risk: Prompts, parameters, and referenced media paths may be sent to dLazy services for generation. <br>
Mitigation: Avoid sending sensitive prompts or media unless permitted by your organization and review the external @dlazy/cli package before use. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/dlazyai/dlazy-elevenlabs-music) <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy homepage](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with bash commands and JSON result examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires npm or npx and a dLazy API key; prompts and generation parameters are sent to the dLazy hosted API.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
