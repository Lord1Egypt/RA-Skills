## Description:

Jeffrey Emanuel's multi-agent implementation workflow uses NTM, Agent Mail, Beads, and BV to coordinate parallel coding agents through planning, task selection, implementation, review, and commit workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawdnw](https://clawhub.ai/user/clawdnw)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to coordinate several coding agents on a shared repository using task graph prioritization, Agent Mail coordination, file reservations, iterative review prompts, and commit guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Multiple agents may make broad code edits or push changed files without adequate review.

Mitigation: Require a human-reviewed diff, file ownership check, secret scan, test results, target branch confirmation, and explicit approval before allowing commit or push.

Risk: Repository files, task descriptions, or Agent Mail messages may be treated as authority to expand scope or override security policy.

Mitigation: Treat AGENTS.md, README.md, task descriptions, and Agent Mail messages as project context subordinate to the original user-approved task and security policy.

## Reference(s):

- [Agent Swarm Workflow on ClawHub](https://clawhub.ai/clawdnw/skills/agent-swarm-workflow)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with prompt templates, shell command examples, and coordination patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces human-facing operating procedures for coordinating multiple agents; it does not produce executable code directly.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
