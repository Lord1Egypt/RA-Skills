## Description:

This skill guides agents in using a Playwright-based browser automation CLI for navigation, form filling, screenshots, and page information extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, automation builders, and personal users use this skill to drive browser workflows such as check-ins, form submission, visual inspection, and data capture through agent-browser commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent browser-control and command-execution ability.

Mitigation: Install and run it only in environments where that level of automation is acceptable, and review planned commands before execution.

Risk: Examples include password form submission and account actions.

Mitigation: Avoid inline passwords, use approved secret-handling practices, and require confirmation before submitting forms or changing account state.

Risk: Recurring unattended sign-ins may violate site rules or create unintended account activity.

Mitigation: Do not schedule unattended sign-ins unless the site's rules and the user's authorization are clear.

Risk: Screenshots and page snapshots may contain private information.

Mitigation: Store screenshots only when needed, restrict access, and delete sensitive captures after review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/browser-cli-tool-free)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Text, Files]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce browser screenshots and page snapshots through the referenced CLI.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
