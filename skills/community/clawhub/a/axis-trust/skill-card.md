## Description:

Checks AI agent trust scores, credit-style reliability ratings, and trust tiers through the AXIS Agent Trust Infrastructure API, with guidance and examples for public lookups, agent registration, behavioral event submission, and identity verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leonidas-esquire](https://clawhub.ai/user/leonidas-esquire)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill to evaluate another agent's AXIS trust profile before delegation, data sharing, or transactions. Authenticated users can also register agents, submit behavioral events, and inspect trust or credit score details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Executable examples may expose live session cookies when copied into command lines or shared chats.

Mitigation: Avoid pasting live session cookies into commands or chats; prefer unauthenticated public lookups or a safer local secret-handling workflow for authenticated calls.

Risk: Registration, behavioral event submission, API key creation, and key revocation are account-sensitive actions.

Mitigation: Require explicit review before running authenticated examples, verify target agent IDs and event details, and test with non-production accounts where possible.

Risk: Shell examples accept user-provided values and session cookies.

Mitigation: Prefer the Python lookup example for public trust checks, and review shell inputs carefully before execution.

## Reference(s):

- [AXIS Homepage](https://axistrust.io)
- [AXIS API Explorer](https://axistrust.io/api-explorer)
- [AXIS Documentation](https://axistrust.io/docs)
- [AXIS Agent Directory](https://axistrust.io/directory)
- [AXIS Changelog](https://axistrust.io/changelog)
- [ClawHub Skill Page](https://clawhub.ai/leonidas-esquire/skills/axis-trust)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, API Calls]

**Output Format:** [Markdown guidance with inline shell and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe AXIS public and authenticated API requests; authenticated actions require an AXIS session cookie.]

## Skill Version(s):

1.1.0 (source: evidence release.version and CHANGELOG, released 2026-03-13)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
