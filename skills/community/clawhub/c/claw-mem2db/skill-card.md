## Description:

Provides OpenClaw agents with persistent local semantic memory by capturing chat and tool-call observations into SQLite FTS5, recalling relevant history into future prompts, and exposing memory search, status, deletion, import, export, pruning, and configuration workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ngplateform](https://clawhub.ai/user/ngplateform)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when they want an OpenClaw agent to retain searchable decisions, preferences, session summaries, and tool-call context across restarts, compaction, or new sessions. It is also useful for controlled memory maintenance through agent tools or the OpenClaw CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates long-lived agent memory and broadly stores and reinjects chat and tool history by default.

Mitigation: Install only when persistent memory is intended, configure retention pruning, and restrict or disable automatic prompt injection for sensitive deployments.

Risk: Installation guidance includes a safety-check bypass and a manual install fallback.

Mitigation: Pin and verify the npm package, prefer the normal OpenClaw plugin install path, and avoid the manual bypass path unless the source and environment are trusted.

Risk: Stored observations or tool outputs may contain secrets or regulated data.

Mitigation: Expand skipped tool capture for sources likely to contain secrets, use memory deletion and pruning commands, and avoid on-chain or P2P backup for private data without strong encryption and deletion planning.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ngplateform/skills/claw-mem2db)
- [npm package @chainofclaw/claw-mem](https://www.npmjs.com/package/@chainofclaw/claw-mem)
- [CLI Reference](references/cli.md)
- [Configuration](references/config.md)
- [Observer and Session Hooks](references/observer.md)
- [Programmatic API](references/programmatic-api.md)
- [coc-soul companion skill](https://clawhub.ai/ngplateform/coc-soul)
- [coc-node companion skill](https://clawhub.ai/ngplateform/coc-node)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with CLI commands, JSON configuration snippets, and TypeScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces memory context that is token-budgeted for prompt injection; exported memory data can be JSON.]

## Skill Version(s):

2.3.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
