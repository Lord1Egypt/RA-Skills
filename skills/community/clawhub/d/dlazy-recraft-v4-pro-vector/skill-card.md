## Description: <br>
High-fidelity text-to-vector model with 4MP-tier quality for production-grade SVG assets and detailed illustrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative teams use this skill to generate vector-style image assets and detailed illustrations through dLazy's hosted Recraft V4 Pro Vector service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a third-party hosted dLazy service, so prompts, parameters, and any provided media inputs may be sent to dLazy API and file endpoints. <br>
Mitigation: Use it only with content appropriate for dLazy processing, avoid confidential inputs unless approved, and review the service terms before use. <br>
Risk: The skill requires a dLazy API key and can store that credential in the local CLI configuration. <br>
Mitigation: Treat the API key as sensitive, prefer the pinned CLI version or npx invocation, and rotate or revoke the key from the dLazy dashboard if it may be exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-recraft-v4-pro-vector) <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy service homepage](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands; command responses are JSON containing generated image URLs or async task status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a dLazy API key and supports prompt, aspect ratio, dry-run, no-wait, and timeout options.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
