## Description:

Runs lightweight self-audits of OpenClaw behavior to find repeated failures, propose safe configuration or process improvements, and track changes after incidents, silent-bot periods, rate-limit spikes, or weekly maintenance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[utromaya-code](https://clawhub.ai/user/utromaya-code)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to audit OpenClaw reliability after incidents or during maintenance, identify repeated failures, propose minimal reversible fixes, and record changes and next actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic restarts or session cleanup can interrupt live OpenClaw activity or remove useful diagnostic context.

Mitigation: Require operator confirmation for production restarts or cleanup, capture relevant logs before action, and document the rollback path.

Risk: Context, token, or fallback-chain tuning can change response behavior, latency, or cost.

Mitigation: Apply one reversible change per cycle, keep the previous configuration, and compare failures and latency before and after the change.

Risk: Reliability reports may include sensitive data from service logs.

Mitigation: Redact secrets and sensitive user data before sharing reports, and avoid exposing credentials in summaries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/utromaya-code/skills/agent-self-improver)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown audit summaries with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proposed or applied low-risk operational changes with rollback notes.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
