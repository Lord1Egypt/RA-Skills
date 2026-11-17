## Description:

Enables Codex to run coding tasks end to end with fewer avoidable confirmations, including self-managed terminal waits, polling, tests, builds, and verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vyctorbrzezowski](https://clawhub.ai/user/vyctorbrzezowski)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using Codex use this skill when they want an agent to carry a coding task through normal reads, edits, commands, waits, tests, and verification without avoidable confirmation prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill intentionally reduces confirmation prompts for routine coding steps, which may be inappropriate for work that requires approval before each file edit, dependency install, long-running command, or local server launch.

Mitigation: Enable it only for tasks where autonomous execution is desired, and avoid using it for workflows that require step-by-step confirmation.

Risk: Autonomous execution can continue through waits, polling, tests, builds, and verification, increasing the importance of clear task boundaries.

Mitigation: Use explicit user instructions for destructive, external, credentialed, paid, or production-affecting actions; the skill directs the agent to stop for those blockers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vyctorbrzezowski/skills/codex-run-to-completion)
- [Publisher profile](https://clawhub.ai/user/vyctorbrzezowski)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Agent instructions and progress summaries, often with markdown, code snippets, shell commands, or configuration changes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill changes the agent's operating posture; it does not define a separate data format or artifact schema.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
