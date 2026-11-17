## Description:

Claude Memory Pro guides an agent in maintaining a five-layer local memory system with token budget management, cost tracking, and cross-session learning workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[e2e5g](https://clawhub.ai/user/e2e5g)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to organize persistent local memory, categorize retained user and project context, manage token budgets, and track cost-sensitive interaction patterns across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to create and retain local cross-session memory, which can preserve information longer than intended.

Mitigation: Install only when local memory retention is desired, review the memory directory periodically, and delete stale entries.

Risk: Sensitive information could be stored in local memory if users or agents save it intentionally or by mistake.

Mitigation: Do not store secrets, credentials, private personal details, or sensitive project material unless retention on disk is intentional and approved.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with example shell commands, directory layouts, decision trees, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local memory-management guidance; does not require API keys or external tool integrations according to discovery.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
