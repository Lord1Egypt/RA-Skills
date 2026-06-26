## Description: <br>
Idea-to-video planning tool for CLI and external agents that returns a logical plan template with control flow and an expanded flat shape list ready for canvas rendering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to call the dLazy CLI for video planning, including prompt-based scenario and style selection. It is suited for workflows that intentionally send planning prompts and referenced media to dLazy services and receive structured planning output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generic `plan` trigger can cause ordinary planning requests to invoke `dlazy plan` and send prompts or file references to dLazy services unintentionally. <br>
Mitigation: Require explicit user confirmation before running `dlazy plan`, and avoid enabling the skill with a generic trigger in environments where routine planning requests are common. <br>
Risk: The skill requires a dLazy API key and may send prompts or referenced media to `api.dlazy.com` and `files.dlazy.com`. <br>
Mitigation: Use only scoped, rotatable organization keys; avoid sending secrets or sensitive media; and rotate or revoke the key from the dLazy dashboard if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/dlazyai/dlazy-plan) <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy homepage](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires npm or npx, dLazy CLI 1.0.9, and a dLazy API key stored in CLI config or supplied through DLAZY_API_KEY.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata; artifact frontmatter reports 1.1.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
