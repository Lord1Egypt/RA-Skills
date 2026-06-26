## Description: <br>
Generate realistic digital human broadcast videos from portrait images and audio/text using Jimeng OmniHuman 1.5. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to invoke dLazy's Jimeng OmniHuman 1.5 workflow for generating digital-human broadcast videos from a portrait image and audio or text prompt. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a dLazy API key that may be stored in local CLI configuration or supplied through an environment variable. <br>
Mitigation: Use scoped dLazy organization keys, keep local config access restricted, and rotate or revoke keys from the dLazy dashboard when access changes. <br>
Risk: Prompts and selected image or audio files are sent to dLazy's hosted API and media storage. <br>
Mitigation: Do not submit media or prompts that are not approved for dLazy's hosted service, and review service terms and privacy requirements before use. <br>
Risk: The install commands use @dlazy/cli@latest, so CLI behavior may change as the npm package is updated. <br>
Mitigation: Review the package or source before installation and pin a tested @dlazy/cli version when reproducibility is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-jimeng-omnihuman-1-5) <br>
- [Publisher profile](https://clawhub.ai/user/dlazyai) <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy service homepage](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The invoked CLI returns JSON containing result URLs or asynchronous task status.] <br>

## Skill Version(s): <br>
1.2.0 (source: evidence.release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
