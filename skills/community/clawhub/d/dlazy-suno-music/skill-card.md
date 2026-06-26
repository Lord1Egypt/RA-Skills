## Description: <br>
Suno music generation model that supports inspiration mode with automatic lyrics and custom mode with manual lyrics, with or without vocals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to invoke dLazy's hosted Suno music generation workflow from an agent. It helps create songs from prompts, optional custom lyrics, style controls, vocal settings, and async generation options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive dLazy API credentials. <br>
Mitigation: Use a scoped API key, keep it in the documented dLazy configuration or environment variable, and rotate or revoke it from the dLazy dashboard when access changes. <br>
Risk: Prompts and referenced local media files may be sent to hosted dLazy endpoints for generation. <br>
Mitigation: Review prompts and file paths before execution, avoid submitting confidential content, and use dry-run or no-wait options when checking payloads or async behavior. <br>
Risk: Server security evidence marks the release as suspicious and advises caution with high-impact account or content actions. <br>
Mitigation: Install only from trusted publisher channels, inspect commands before running them, and require explicit user confirmation for account, moderation, or content-changing actions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dlazyai/dlazy-suno-music) <br>
- [dLazy CLI Homepage](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm Package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy Homepage](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a dLazy API key and may return asynchronous task identifiers or generated media URLs.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
