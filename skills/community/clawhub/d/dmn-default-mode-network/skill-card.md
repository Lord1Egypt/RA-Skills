## Description:

Dmn Default Mode Network is a background autonomous thinking skill that synthesizes personal memory and knowledge-base notes, generates session summaries, and proposes technical follow-up actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikonos](https://clawhub.ai/user/mikonos)

### License/Terms of Use:


## Use Case:

Developers and knowledge workers use this skill to run background reflection over personal memory files and knowledge bases, producing synthesis notes, open questions, and proposed engineering follow-up actions for later review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read broad personal memory and knowledge-base files while running as a background agent.

Mitigation: Review and narrow the configured memory and knowledge-base paths before installation or execution.

Risk: The skill can create persistent notes, state, and self-evolution queue entries without clear approval gates.

Mitigation: Disable or remove the `memory/evolve/candidates.md` handoff unless a separate manual approval process is in place.

Risk: Generated action proposals may suggest installs, repository clones, scripts, or project creation on the host.

Mitigation: Review suggested actions explicitly and run any accepted commands in a sandboxed environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mikonos/skills/dmn-default-mode-network)
- [Core Functions](artifact/references/core-functions.md)
- [Execution Flow](artifact/references/execution-flow.md)
- [Session Synthesis Template](artifact/assets/session-synthesis.md)
- [User Configuration](artifact/assets/user-config.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown notes and synthesis files with configuration/state JSON references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update persistent DMN state and queue proposed AI/workflow changes for later review.]

## Skill Version(s):

3.3.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
