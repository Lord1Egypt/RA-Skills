## Description: <br>
Alibaba Bailian qwen3-tts voice cloning that uploads a clean voice sample to create a custom voice for later TTS use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call the dLazy CLI for Qwen audio voice cloning, providing a clean voice sample and metadata to create a reusable custom voice for TTS workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice samples and related metadata are sent to dLazy hosted services. <br>
Mitigation: Use only audio that the user is authorized to provide, and avoid sensitive voice samples unless the user accepts dLazy processing. <br>
Risk: The skill requires a dLazy API key that may be stored in the local CLI configuration. <br>
Mitigation: Prefer per-session credentials when appropriate, protect the local config file, and rotate or revoke the key from the dLazy dashboard if exposure is suspected. <br>
Risk: The security summary notes documentation mismatches in the skill. <br>
Mitigation: Verify `dlazy qwen-audio-clone -h` before automation and rely on current CLI help for required flags and output behavior. <br>
Risk: A global CLI install increases persistence of third-party tooling on the host. <br>
Mitigation: Prefer `npx @dlazy/cli@latest` or review the `@dlazy/cli` package before installing globally. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-qwen-audio-clone) <br>
- [dLazy CLI homepage](https://github.com/dlazyai/cli) <br>
- [@dlazy/cli npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy homepage](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, json, guidance] <br>
**Output Format:** [Command-line invocation guidance and JSON result envelopes from the dLazy CLI.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires npm or npx and a dLazy API key; local audio paths may be uploaded to dLazy hosted services; async runs can return a generateId for later polling.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
