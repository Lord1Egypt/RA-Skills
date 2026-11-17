## Description:

Free developer guide for building paid skills on ClawHub, covering the standard three-phase payment flow, SkillSpector compliance requirements, and common pitfalls; it does not handle payments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinyu12166](https://clawhub.ai/user/jinyu12166)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building paid ClawHub skills use this reference to understand the expected payment-flow architecture, SkillSpector compliance constraints, sandbox testing, and common implementation pitfalls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The referenced npx sandbox command would execute third-party package code if followed.

Mitigation: Verify the @clawtip/clawtip-sandbox-cli package and run it only in a least-privileged test environment without production secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jinyu12166/skills/clawtip-skill)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reference-only; no bundled executable code.]

## Skill Version(s):

1.0.11 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
