## Description:

Codex+OMX orchestration keeps the current Codex session as decision maker and integrator while using bounded native subagents and runtime-resolved OMX roles for search, reading, research, testing, review, and mutually exclusive writes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[its-how](https://clawhub.ai/user/its-how)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to route non-trivial Codex work through the lowest-sufficient mix of native capability, OMX surfaces, subagents, review, and verification while preserving confirmation gates and final integration in the main session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or upgrading from a moving source can introduce unreviewed changes.

Mitigation: Prefer a reviewed release or pinned commit before installing or upgrading.

Risk: OMX orchestration and delegation can expand cost, persistence, worktree use, or autonomous activity.

Mitigation: Require confirmation for high-cost, persistent, worktree, or autonomous activity and keep the primary Codex session responsible for final integration.

Risk: Delegation or handoff material can expose sensitive session details if boundaries are not enforced.

Mitigation: Keep credentials, tokens, cookies, browser session material, provider state, and live account state out of subagent and out-of-session handoffs.

## Reference(s):

- [Capability Orchestration](references/capability-orchestration.md)
- [aha-orch Repository](https://github.com/its-How/aha-orch)
- [Codex CLI](https://github.com/openai/codex)
- [oh-my-codex](https://github.com/Yeachan-Heo/oh-my-codex)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with inline command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent-facing orchestration guidance; no persistent state is maintained by the skill.]

## Skill Version(s):

1.1.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
