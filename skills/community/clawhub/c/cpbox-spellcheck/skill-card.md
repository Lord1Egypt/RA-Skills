## Description:

Corrects misspelled search queries for pre-search cleanup or "Did you mean?" interfaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sprintmint](https://clawhub.ai/user/sprintmint)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to check short user search queries before search execution or to present corrected suggestions in a user interface.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to run an unpinned payment package through npx in a wallet-backed flow.

Mitigation: Verify and pin the @springmint/x402-payment package version before use.

Risk: Payment is automatic after the x402 flow is configured, which can obscure destination and amount.

Mitigation: Use a wallet with strict spending limits and require clear confirmation of payment destination and amount for each request.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sprintmint/skills/cpbox-spellcheck)
- [x402 payment setup prerequisites](https://github.com/springmint/cpbox-skills#prerequisites)
- [CPBox spellcheck endpoint](https://www.cpbox.io/api/x402/spellcheck)
- [CPPay facilitator](https://www.cppay.finance)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with HTTP, bash, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns corrected query suggestions when available; payment may be required through an x402 flow.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
