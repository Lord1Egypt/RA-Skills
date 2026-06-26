## Description: <br>
fal.ai sync-lipsync v3 generates a new video where a speaker's lip movement matches supplied audio, supporting dubbing, localization, and virtual presenter re-syncing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to call the dLazy CLI for lip-sync video generation from input video and audio, including dubbing, localization, and virtual presenter workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The install path uses @latest for @dlazy/cli, so the installed CLI can change over time. <br>
Mitigation: Review the @dlazy/cli package or source before installation when supply-chain stability matters. <br>
Risk: The skill requires a dLazy API key and may save it in the local CLI config. <br>
Mitigation: Use per-invocation DLAZY_API_KEY when persistent local credential storage is not desired. <br>
Risk: Local video and audio files passed to the CLI are uploaded to dLazy-hosted services for processing. <br>
Mitigation: Only provide media files intended for upload to dLazy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-sync-lipsync-3) <br>
- [dLazy CLI project](https://github.com/dlazyai/cli) <br>
- [@dlazy/cli npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy CLI metadata homepage](https://github.com/dlazyai/cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return hosted media URLs or asynchronous task identifiers from the dLazy service.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
