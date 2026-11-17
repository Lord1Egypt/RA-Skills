## Description:

ClawVault is an agent memory system with a memory graph, context profiles, checkpoint and recovery workflows, structured storage, semantic search, and observational memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to store, search, recover, and retrieve structured session memory for OpenClaw workflows. It is intended for graph-aware context retrieval, checkpointing, handoff continuity, semantic memory search, and transcript repair rather than general file I/O.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation flow can fetch unpinned external code for the CLI and qmd dependency.

Mitigation: Pin exact package versions and review package metadata before installing.

Risk: The OpenClaw lifecycle hook can run during gateway, command, session, compaction, and cron events, while the hook source is not included in the published bundle.

Mitigation: Install the hook without enabling it, inspect the locally installed hook source, then enable it only after review.

Risk: Transcript repair and observe compression can access local session transcripts, and observe compression may use an API key for LLM calls.

Mitigation: Use transcript repair only with backups enabled and use observe compression only when local transcript and optional API-key exposure are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alvisdunlop/skills/alv-clawvault)
- [ClawVault homepage](https://clawvault.dev)
- [ClawVault npm package](https://www.npmjs.com/package/clawvault)
- [ClawVault GitHub repository](https://github.com/Versatly/clawvault)
- [OpenClaw](https://openclaw.ai)
- [qmd dependency](https://github.com/tobi/qmd)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to install and run local CLI tools, configure environment variables, inspect lifecycle hooks, and manage local memory files.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 2.5.11)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
