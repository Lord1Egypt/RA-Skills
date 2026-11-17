## Description:

EngramClaw helps agents use Engram persistent memory across sessions to save significant technical findings, search prior work, restore project context, and write end-of-session summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dragonjar](https://clawhub.ai/user/dragonjar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use EngramClaw to connect agents to an Engram MCP memory backend so agents can retain curated technical context, find prior work, and preserve session summaries across coding sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory may retain confidential code, secrets, customer data, personal information, prompts, or preferences.

Mitigation: Use explicit project scoping, save only significant technical context, redact secrets before saving, and avoid raw prompts or preferences unless they are necessary.

Risk: Broad automatic retention and recall can exceed user expectations when consent, minimization, or retention controls are unclear.

Mitigation: Apply a clear retention policy before deployment, avoid saving every message or tool call, and review recalled context before using it in sensitive work.

Risk: The skill depends on downloaded mcporter and engram binaries or packages.

Mitigation: Verify package and release sources before installation and prefer approved package channels for the deployment environment.

Risk: Hard deletion of stored observations is irreversible.

Mitigation: Prefer soft delete for routine cleanup and reserve hard delete for confirmed removal requests or retention-policy enforcement.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dragonjar/skills/engramclaw)
- [Engram project](https://github.com/Gentleman-Programming/engram)
- [Engram releases](https://github.com/Gentleman-Programming/engram/releases)
- [MCPorter project](https://github.com/steipete/mcporter)
- [MCPorter releases](https://github.com/steipete/mcporter/releases)
- [OpenClaw framework](https://github.com/gentleman-programming/openclaw)
- [Engram MCP tools reference](artifact/references/tools.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and MCP tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires mcporter and engram binaries; stores and retrieves persistent memory through an Engram MCP server.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
