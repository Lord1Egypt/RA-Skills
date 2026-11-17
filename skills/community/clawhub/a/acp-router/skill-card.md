## Description:

Route plain-language requests for Pi, Claude Code, Codex, OpenCode, Gemini CLI, or ACP harness work into either OpenClaw ACP runtime sessions or direct acpx-driven sessions ("telephone game" flow).

This skill is ready for commercial/non-commercial use.

## Publisher:

[yimeihuang1999-leaves](https://clawhub.ai/user/yimeihuang1999-leaves)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to route requests for Pi, Claude Code, Codex, OpenCode, Gemini CLI, Kimi, or ACP harness work into the correct ACP runtime or direct acpx session flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct agents to install packages, restart gateways, run external adapters, and modify ACPX configuration.

Mitigation: Require explicit approval for npm installs, gateway restarts, and any change to ~/.acpx/config.json.

Risk: The direct acpx path may rely on mutable external adapter packages.

Mitigation: Prefer pinned or locally reviewed adapter binaries instead of floating npx packages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yimeihuang1999-leaves/skills/acp-router)
- [Publisher profile](https://clawhub.ai/user/yimeihuang1999-leaves)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes session creation and recovery guidance; does not produce standalone files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
