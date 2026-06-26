## Description: <br>
Search the ElevenLabs voice library by keyword, source, and category, returning playable previews for matched voices before TTS use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search ElevenLabs voices through the dLazy CLI, filter by source and category, and choose a playable preview before running text-to-speech work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a dLazy API key and stores credentials locally or reads them from the DLAZY_API_KEY environment variable. <br>
Mitigation: Use a scoped organization key, store it only in the documented CLI config or environment variable, and rotate or revoke it from the dLazy dashboard when access changes. <br>
Risk: Search prompts and parameters are sent to dLazy cloud endpoints, and artifact evidence lists api.dlazy.com and files.dlazy.com as service endpoints. <br>
Mitigation: Do not submit sensitive voice-search prompts or files unless the deployment has approved dLazy for that data. <br>
Risk: The install metadata uses @latest, which can change the CLI behavior after review. <br>
Mitigation: Pin and review a specific @dlazy/cli version before production deployment. <br>
Risk: Security evidence notes a mismatch between the voice-search purpose and an image-style documented output schema. <br>
Mitigation: Validate actual CLI output in a test environment before wiring downstream automation to the documented JSON fields. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-elevenlabs-search) <br>
- [dLazy CLI homepage](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy service homepage](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [CLI instructions and JSON command results with voice search outputs, preview URLs, or async task status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires npm or npx and a dLazy API key; the documented output schema should be reviewed because evidence notes a voice-preview versus image-output mismatch.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
