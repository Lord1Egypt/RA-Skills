## Description:

Helps OpenClaw agents reduce Anthropic token costs through configuration tuning, context hygiene, cache TTL alignment, compaction practices, and codebase map caching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ngocgd](https://clawhub.ai/user/ngocgd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to tune OpenClaw agent sessions for lower Anthropic API cost while preserving useful context. It is especially relevant for long Claude sessions with high cache-read costs, repeated code exploration, or oversized workspace memory files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes an unpinned remote install command using `npx clawhub@latest install atris`.

Mitigation: Verify the package and publisher before use, and prefer a pinned, reviewed package version in controlled environments.

Risk: The skill encourages persistent workspace memory or map files that may contain project or session details.

Mitigation: Review generated memory and map files for sensitive content, keep them scoped to the workspace, and prune or exclude confidential details before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ngocgd/skills/anthropic-token-optimizer)
- [openclaw-token-optimizer](https://clawhub.ai/asif2bd/openclaw-token-optimizer)
- [ClawHub](https://clawhub.ai)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration, shell commands]

**Output Format:** [Markdown guidance with JSON configuration snippets, shell commands, checklists, and decision tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend persistent workspace memory or map files as part of agent context-management workflows.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
