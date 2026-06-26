## Description: <br>
Generate multilingual, highly natural audio using Gemini 2.5 text-to-speech. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to generate speech audio from text prompts through the dLazy CLI and hosted Gemini 2.5 text-to-speech service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and referenced media may be processed by dLazy-hosted services. <br>
Mitigation: Use explicit text-to-speech requests and avoid sending private or sensitive content unless that processing is intended. <br>
Risk: The workflow depends on a local or API-key-based dLazy CLI authentication setup. <br>
Mitigation: Store API keys using the documented dLazy CLI flow or environment variable, and rotate or revoke keys from the dLazy dashboard when needed. <br>
Risk: Using the skill may install or run the third-party @dlazy/cli package. <br>
Mitigation: Review the CLI package or source before using it for sensitive work, and prefer the pinned version documented by the release. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dlazyai/dlazy-gemini-2-5-tts) <br>
- [dLazy CLI Source](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm Package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy Homepage](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON result examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires npm or npx, a dLazy API key, and network access to dLazy-hosted services.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
