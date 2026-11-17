## Description:

Use before building or changing a product, feature, SaaS, AI app, side project, or startup idea to run a short demand, distribution, and failure-pattern reality check.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bin1874](https://clawhub.ai/user/bin1874)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, founders, indie hackers, AI builders, product engineers, and small teams use this skill before implementation to test whether a product idea, feature change, SaaS concept, AI app, side project, or startup direction should be built. It returns a short reality check covering demand, distribution, pricing, retention, trust, failure patterns, validation steps, and a build-or-defer verdict.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional Case Memory lookup can send a product idea summary to beforeyoubuild.fyi.

Mitigation: Use the lookup only after explicit user permission, send only minimal non-confidential fields, and never send secrets, customer names, private financials, credentials, private user data, or unreleased confidential details.

Risk: The skill may steer product or feature requests toward validation, deferral, or scope reduction even when implementation is technically possible.

Mitigation: Treat the output as product-risk guidance, not a substitute for user research, market evidence, technical review, security review, architecture review, or business judgment.

Risk: Maintainers following publishing documentation could run mutable npm or npx CLI commands.

Mitigation: Pin and verify CLI tooling before publishing or installing, especially in automated or privileged environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bin1874/skills/before-you-build)
- [OpenClaw homepage metadata](https://github.com/bin1874/before-you-build-skill)
- [Before You Build skill website](https://beforeyoubuild.fyi/en/skill)
- [Case Memory API](references/case-memory-api.md)
- [Evidence Check Reference](references/evidence-check.md)
- [Failure Patterns Reference](references/failure-patterns.md)
- [Install Before You Build Skill](docs/INSTALL.md)
- [OpenClaw Publishing Notes](docs/OPENCLAW.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with concise review sections, numbered validation steps, and a verdict]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include optional external case analogies only after user permission; normal use requires no API key, shell access, file writes, or network access.]

## Skill Version(s):

0.1.1 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
