## Description: <br>
Alibaba Bailian qwen3-tts text-to-speech. Choose from curated system voices, including dialects, or design a custom voice from a natural-language description. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate text-to-speech audio through the dLazy hosted Qwen TTS service, selecting predefined voices or describing a custom voice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a dLazy API key and stores credentials locally or accepts them through an environment variable. <br>
Mitigation: Use the documented dLazy login or auth command, keep the key scoped to the intended organization, and rotate or revoke it from the dLazy dashboard when needed. <br>
Risk: Prompts, parameters, and selected media paths may be sent to the dLazy hosted API and file service. <br>
Mitigation: Use the skill only when sharing the requested inputs with the dLazy service is acceptable, and prefer dry runs or local review before submitting sensitive content. <br>
Risk: A persistent global CLI install may increase local dependency footprint. <br>
Mitigation: Use the documented npx invocation when a one-time or non-persistent CLI execution is preferred. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-qwen-tts) <br>
- [dLazy CLI package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy CLI homepage](https://github.com/dlazyai/cli) <br>
- [dLazy website](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return hosted result URLs or an asynchronous generation task ID through the dLazy CLI.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
