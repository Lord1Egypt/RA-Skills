## Description:

Provides guidance and command examples for using CloverCLI to manage Clover POS inventory, orders, payments, customers, employees, discounts, taxes, tenders, and reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[g9pedro](https://clawhub.ai/user/g9pedro)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to install, configure, and run CloverCLI commands for Clover POS administration and reporting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to install changing third-party CLI code.

Mitigation: Use a pinned and verified CloverCLI release where possible before using it with production Clover data.

Risk: The setup guidance shows Clover access tokens persisted in a shell profile.

Mitigation: Prefer a credential manager or per-command environment variable, and use least-privilege, revocable Clover tokens.

Risk: The artifact includes a real-looking client merchant identifier in shared documentation.

Mitigation: Remove real client identifiers from shared documentation and examples before redistribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/g9pedro/skills/clovercli)
- [npm package listed in artifact](https://www.npmjs.com/package/@versatly/clovercli)
- [GitHub repository listed in artifact](https://github.com/Versatly/clovercli)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include setup steps, CLI invocations, output-format guidance, and credential-handling cautions.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact describes CloverCLI v1.2.0 behavior)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
