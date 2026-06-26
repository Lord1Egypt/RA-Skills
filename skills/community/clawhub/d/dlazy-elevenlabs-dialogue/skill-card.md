## Description: <br>
Generates multi-voice ElevenLabs dialogue audio by assigning voices to dialogue lines and supporting audio tags for character effects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to invoke the dLazy CLI for ElevenLabs multi-speaker dialogue generation for character dialogue, podcasts, and short skits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a dLazy API key that may be saved in local CLI configuration. <br>
Mitigation: Use DLAZY_API_KEY for per-invocation authentication when persistence is not desired, protect the local config file, and rotate or revoke keys from the dLazy dashboard when needed. <br>
Risk: The install instructions use the third-party @dlazy/cli package at @latest, so installed CLI behavior may change over time. <br>
Mitigation: Review the @dlazy/cli package before installing and prefer npx for one-off execution when a persistent global install is unnecessary. <br>
Risk: Local files passed to media fields are uploaded to dLazy-hosted storage for processing. <br>
Mitigation: Avoid passing local file paths unless the user intends those files to be uploaded to dLazy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-elevenlabs-dialogue) <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [@dlazy/cli npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy homepage](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON CLI results containing generated media URLs or async task status] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a dLazy API key; generated outputs are hosted on files.dlazy.com and async tasks may require polling with dlazy status.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
