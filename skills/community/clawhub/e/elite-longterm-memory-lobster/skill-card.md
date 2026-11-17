## Description:

Provides agent-facing guidance and CLI commands for maintaining durable long-term memory through session files, semantic recall configuration, git notes, curated archives, and optional cloud memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mjscjj](https://clawhub.ai/user/mjscjj)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to set up durable memory workflows for Clawdbot, Moltbot, Claude Code, GPT agents, and similar agent environments. It helps agents preserve active context, record decisions, organize daily memory files, and configure optional semantic or cloud-backed recall.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Durable memory can retain sensitive, secret, or regulated conversation details.

Mitigation: Treat memory capture as opt-in, review memory files regularly, and avoid storing secrets or regulated data.

Risk: Optional cloud memory can upload retained context outside the local workspace.

Mitigation: Do not enable cloud memory until upload behavior and privacy controls have been reviewed.

Risk: Broad or silent memory capture can preserve more context than intended.

Mitigation: Use explicit capture thresholds and periodically audit or delete low-value memory entries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mjscjj/skills/elite-longterm-memory-lobster)
- [Publisher profile](https://clawhub.ai/user/mjscjj)
- [npm package: elite-longterm-memory](https://www.npmjs.com/package/elite-longterm-memory)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash, JSON, and JavaScript snippets plus CLI-generated Markdown files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI can create or inspect local memory files such as SESSION-STATE.md, MEMORY.md, and memory/YYYY-MM-DD.md.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and package.json declare 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
