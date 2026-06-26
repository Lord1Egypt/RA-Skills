## Description: <br>
Generate matching scene sound effects based on text descriptions or video frames using Kling SFX. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creators use this skill to invoke dLazy's Kling SFX workflow for generating sound effects from text prompts or video frames. The workflow is intended for agents that can run the dLazy CLI with an authenticated dLazy account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a dLazy API key and may use local CLI configuration or the DLAZY_API_KEY environment variable. <br>
Mitigation: Use authorized credentials only, restrict access to local config files, and rotate or revoke keys from the dLazy dashboard when needed. <br>
Risk: Prompts and selected local media can be sent to dLazy cloud services for generation and hosted output. <br>
Mitigation: Avoid submitting confidential prompts or media unless approved for that service, and review file paths before invoking the CLI. <br>
Risk: Execution depends on the third-party @dlazy/cli npm package and dLazy cloud services. <br>
Mitigation: Use npx for temporary execution when preferred, or install the pinned CLI package only after reviewing the package and source links. <br>


## Reference(s): <br>
- [Dlazy Keling Sfx on ClawHub](https://clawhub.ai/dlazyai/dlazy-keling-sfx) <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [@dlazy/cli npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with CLI commands; CLI responses are JSON with generated output URLs or async task status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires npm or npx, a dLazy API key, and network access to dLazy cloud services.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
