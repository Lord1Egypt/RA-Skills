## Description:

Wrap shell commands with the agent-runlog CLI to capture concise, redacted run logs for debugging, CI reproduction, long-running agent commands, repeated failures, test/lint/build evidence, and handoffs where stdout/stderr plus git state should be preserved without flooding chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[builtbyecho](https://clawhub.ai/user/builtbyecho)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to wrap test, lint, build, and other shell commands so concise local run logs can support debugging, CI reproduction, repeated-failure diagnosis, and agent handoffs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an npm CLI invocation that can change if the package is not pinned.

Mitigation: Pin @builtbyecho/agent-runlog to a reviewed version or use a lockfile-managed local install.

Risk: Command logs may capture private data from stdout, stderr, or git state.

Mitigation: Keep .agent-runs logs local when sensitive output may be present and share summaries instead of full logs.

Risk: Wrapping destructive commands records their output but does not make those commands safe to run.

Mitigation: Require explicit approval before wrapping destructive commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/builtbyecho/skills/agent-runlog)

## Skill Output:

**Output Type(s):** [guidance, shell commands, markdown, JSON]

**Output Format:** [Markdown guidance with bash command examples and optional JSON run output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Run ledgers are written locally under .agent-runs/; redaction is on by default.]

## Skill Version(s):

0.4.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
