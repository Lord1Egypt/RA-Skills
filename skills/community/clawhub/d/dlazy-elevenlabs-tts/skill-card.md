## Description: <br>
ElevenLabs eleven_v3 text-to-speech with 12 curated multilingual voices and stability, similarity, and style controls for dubbing, audiobooks, and character dialogue. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agent users use this skill to run dLazy's ElevenLabs text-to-speech CLI for multilingual speech generation with selectable voices and voice-tuning parameters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a dLazy API key that may be saved in local CLI configuration. <br>
Mitigation: Use DLAZY_API_KEY for per-invocation authentication or review local config handling before saving credentials persistently. <br>
Risk: Prompts, parameters, and any user-supplied media paths are sent to hosted dLazy endpoints. <br>
Mitigation: Review the external @dlazy/cli package and dLazy service trust boundary before sending sensitive content. <br>
Risk: Installing the CLI globally adds an external package to the user's environment. <br>
Mitigation: Use the pinned npx invocation when persistent global installation is not needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dlazyai/dlazy-elevenlabs-tts) <br>
- [Publisher Profile](https://clawhub.ai/user/dlazyai) <br>
- [dLazy CLI Source](https://github.com/dlazyai/cli) <br>
- [@dlazy/cli npm Package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy Homepage](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration guidance, Text, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The CLI can return hosted output URLs or an asynchronous task identifier when invoked with --no-wait.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
