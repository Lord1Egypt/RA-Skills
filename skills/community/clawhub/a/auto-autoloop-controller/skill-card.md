## Description:

When continuous automated improvement of a Skill is needed, this skill wraps improvement-orchestrator in a persistent loop with convergence detection, cost control, and cross-session state persistence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanyasheng](https://clawhub.ai/user/lanyasheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run repeated skill-improvement cycles with configurable iteration limits, estimated cost caps, convergence checks, and persistent state for resuming work across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can repeatedly run an automated skill-improvement subprocess and persist state across sessions.

Mitigation: Start with --dry-run, low --max-iterations, and supervised initial runs before allowing longer loops.

Risk: The cost cap is an estimate rather than a guaranteed spending limit.

Mitigation: Set a low --max-cost for early runs and monitor iteration logs and cumulative cost output during execution.

Risk: Scheduled background runs can continue after setup if cron is used.

Mitigation: Review run-eval.sh, choose safe target and state paths, set appropriate permissions, and know how to remove the crontab entry before scheduling.

## Reference(s):

- [Scheduling Guide](references/scheduling-guide.md)
- [State Format](references/state-format.md)
- [ClawHub Skill Page](https://clawhub.ai/lanyasheng/skills/auto-autoloop-controller)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with CLI examples, JSON state, JSONL logs, and per-iteration Markdown handoff files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces persistent state and run logs under the configured state root.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence; artifact frontmatter reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
