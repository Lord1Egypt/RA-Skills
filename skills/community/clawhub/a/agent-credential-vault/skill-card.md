## Description:

Lets an AI agent log in and call APIs using brokered credentials it never sees, keeping passwords, API keys, and TOTP codes out of model context, argv, logs, and traces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anima](https://clawhub.ai/user/anima)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to provision, store, broker, inject, redact, audit, and when necessary retrieve credentials for autonomous agents while preserving human authorization and auditability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A trusted credential broker can enable agent access to sensitive accounts and APIs.

Mitigation: Install only when Anima is an intended trusted broker and grant only credentials needed for the specific workflow.

Risk: Credentials could be revealed or sent to unintended destinations if reveal policy or host controls are too permissive.

Mitigation: Use brokered reveal policy and set allowed hosts for API keys so credentials are not returned to the agent or brokered to unexpected hosts.

Risk: Subprocess credential injection can affect commands beyond the intended target if run without review.

Mitigation: Run vault exec with dry-run first and review the resolved references before executing the subprocess.

Risk: Agent-held credentials could authorize purchases, deletions, or account changes without a separate business decision.

Mitigation: Avoid granting agents credentials that can make purchases, delete data, or change accounts unless separate human approval gates those actions.

## Reference(s):

- [Anima homepage](https://useanima.sh)
- [Anima documentation](https://docs.useanima.sh)
- [Anima API endpoint](https://api.useanima.sh)
- [ClawHub skill page](https://clawhub.ai/anima/skills/agent-credential-vault)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces credential-vault workflow guidance; it does not output raw secrets when brokered reveal policy is used.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
