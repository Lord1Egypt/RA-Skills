## Description:

Set up the full OpenClaw agent memory system with 3-tier memory (HOT/WARM/COLD), daily logs, semantic search (QMD), and lossless context management (Lossless Claw).

This skill is ready for commercial/non-commercial use.

## Publisher:

[autosolutionsai-didac](https://clawhub.ai/user/autosolutionsai-didac)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to initialize OpenClaw workspaces with persistent agent memory, semantic memory search, context compaction, and setup and verification guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory setup can store and reload personal or shared workspace context.

Mitigation: Install only in the intended workspace after reviewing the AGENTS.md template and deciding which memory files the agent may read and update.

Risk: The setup can persistently change agent behavior through memory instructions and OpenClaw configuration.

Mitigation: Review the generated workspace instructions and configuration before enabling them, especially in shared or multi-agent workspaces.

Risk: The setup can automatically install an unpinned Lossless Claw plugin and may require an OpenClaw gateway restart.

Mitigation: Prefer pinned, reviewed versions of QMD, OpenClaw, and Lossless Claw, and avoid automatic plugin install or gateway restart unless those environment changes are expected.

## Reference(s):

- [AGENTS_TEMPLATE.md](artifact/references/AGENTS_TEMPLATE.md)
- [OpenClaw homepage](https://github.com/nichochar/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands, JSON configuration snippets, and workspace file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or preserve memory files in the target workspace and may attempt an OpenClaw plugin install when openclaw is available.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
