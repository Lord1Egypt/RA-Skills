## Description: <br>
Synthesize text into natural and fluent speech using Doubao TTS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to invoke dLazy's Doubao TTS CLI, select voice and speech options, and generate speech from text through dLazy's hosted service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a dLazy API key that may be saved in the local CLI configuration. <br>
Mitigation: Use the DLAZY_API_KEY environment variable for per-invocation credentials when persistence is not desired, and rotate or revoke exposed keys from the dLazy dashboard. <br>
Risk: Prompt text and selected parameters are sent to dLazy's hosted service for speech synthesis. <br>
Mitigation: Review input text before invocation and avoid sending private or regulated content unless that use is approved for the service. <br>
Risk: Unreviewed generation requests may consume credits unexpectedly. <br>
Mitigation: Use the documented --dry-run option to inspect the payload and cost estimate before submitting a request. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dlazyai/dlazy-doubao-tts) <br>
- [dLazy CLI Source](https://github.com/dlazyai/cli) <br>
- [@dlazy/cli npm Package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy Homepage](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON CLI responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires npm or npx, a dLazy API key, and network access to dLazy API and file endpoints.] <br>

## Skill Version(s): <br>
1.2.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
