## Description:

Looks up a bank card number's issuing bank, province or city of origin, card type, and validation status using JisuAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to answer bank-card origin and validity questions by passing a card number to a Python CLI backed by JisuAPI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full bank card numbers and the JISU_API_KEY are sent to a third-party service in URL query parameters.

Mitigation: Use a dedicated low-privilege JisuAPI key, avoid submitting real card numbers unless the user explicitly agrees, and account for possible provider or network query logging.

Risk: Security evidence marks the release suspicious because the artifact lacks a clear privacy warning for card-number handling.

Mitigation: Review the skill before installation and add user-facing consent and privacy guidance before using it with real card numbers.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jisuapi/skills/bankcard)
- [JisuAPI](https://www.jisuapi.com/)
- [JisuAPI Bank Card API Documentation](https://www.jisuapi.com/api/bankcard)
- [JisuAPI Bank Card Query Endpoint](https://api.jisuapi.com/bankcard/query)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON from a Python CLI, with agent-facing text summaries when appropriate]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; sends the requested bank card number to JisuAPI.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
