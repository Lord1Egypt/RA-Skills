## Description:

Checks domain availability, safety status, invalidity reasons, and sensitive-risk flags so agents can help clean and validate company domain lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

Sales, marketing, research, recruiting, procurement, and CRM operations teams use this skill to validate company domains before outreach, enrichment, supplier review, or list cleaning. Agents can call the vendor API and return per-domain status, invalidity reasons, sensitive-risk indicators, fee information, and a request ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed or persisted locally.

Mitigation: Use the skill only with a trusted vendor account, keep the local key file private to the user account, and do not allow agents to print `~/.upkuajing/.env`.

Risk: Domain checks can incur paid API requests and the skill includes account and recharge helper commands.

Mitigation: Require explicit user confirmation before chargeable calls, and use the documented price or account checks when cost or balance is unclear.

Risk: The skill performs optional error reporting and daily update checks in addition to the main domain validation call.

Mitigation: Report errors only after user approval and review this extra network activity before installation.

## Reference(s):

- [Domain validity API reference](artifact/references/domain-api.md)
- [Skill error report API reference](artifact/references/skill-error-report-api.md)
- [ClawHub skill listing](https://clawhub.ai/upkuajing/skills/domain-validity-check-zh)
- [Upkuajing homepage](https://www.upkuajing.com)
- [Upkuajing OpenAPI pricing](https://www.upkuajing.com/web/openapi/price.html)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON results with concise agent guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes total count, per-domain validation results, fee information, and request ID when the API call succeeds.]

## Skill Version(s):

1.0.2 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
