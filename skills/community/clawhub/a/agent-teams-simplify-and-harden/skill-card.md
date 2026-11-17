## Description:

Agent Teams Simplify And Harden guides an agent through a two-phase implementation and audit loop using parallel implementation agents, read-only simplify, harden, and spec auditors, and repeated compile and test verification until exit conditions are met.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiao1804](https://clawhub.ai/user/xiao1804)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to coordinate multi-file feature implementation, code hardening, issue remediation, or review-driven refactoring when parallel implementation and structured audit loops are useful.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Implementation agents may be configured to act with permission checks bypassed.

Mitigation: Review the workflow before use, run it only in an isolated repository without unrelated credentials or private files, and avoid the bypassPermissions mode unless that behavior is intentional.

Risk: The documented third-party install command is not pinned.

Mitigation: Prefer a pinned or vendored installation source before installing the skill in a sensitive workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiao1804/skills/agent-teams-simplify-and-harden)

## Skill Output:

**Output Type(s):** [text, guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline shell command blocks and agent prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces task breakdowns, agent prompts, audit findings, verification steps, and final summaries for a human team lead to review.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
