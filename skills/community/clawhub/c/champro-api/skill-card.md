## Description:

CHAMPRO API helps agents use CHAMPRO REST and Custom Builder APIs for inventory, product information, order validation and placement, order tracking, warehouse routing, shipping references, and custom design workflows that CHAMPRO PromoStandards endpoints do not cover.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zmtucker](https://clawhub.ai/user/zmtucker)

### License/Terms of Use:

MIT-0

## Use Case:

External operators, purchasing teams, and developers use this skill to source CHAMPRO stock or custom apparel, check inventory, validate orders, place sandbox or production orders, track suborders, and work with Custom Builder design sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated API calls can be redirected if untrusted input controls api_base or cb_base.

Mitigation: Use trusted CHAMPRO credentials only and do not allow untrusted prompts or generated JSON to supply api_base or cb_base.

Risk: Custom Builder file downloads can overwrite local paths when untrusted input controls output_path.

Mitigation: Restrict output_path to an expected working directory and avoid exposing this CLI to untrusted users.

Risk: Order actions can submit external writes, including production orders or partially placed orders.

Mitigation: Keep confirm and production under human control, rehearse production orders in the sandbox first, and escalate rather than retry when partial order results occur.

Risk: Validation can be bypassed or weakened if untrusted input controls skip_validation.

Mitigation: Do not allow untrusted prompts or generated JSON to set skip_validation before any ordering action.

## Reference(s):

- [CHAMPRO Development Tools](https://devtools.champrosports.com/#devtools)
- [CHAMPRO Account & Contact Info](https://champrosports.com/AccountAndContactInfo)
- [ClawHub Skill Page](https://clawhub.ai/zmtucker/skills/champro-api)
- [PromoStandards Gaps](references/promostandards_gaps.md)
- [API Reference](references/api_reference.md)
- [Custom Builder Reference](references/custom_builder.md)
- [Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with JSON-in/JSON-out CLI examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill's CLI actions return one JSON object on stdout or an error object with a non-zero exit code.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
