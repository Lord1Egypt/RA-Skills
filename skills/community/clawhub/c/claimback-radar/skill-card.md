## Description:

Scans emails and bills to extract billing data, detect refund opportunities, subscription risks, and generate actionable savings recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[schchit](https://clawhub.ai/user/schchit)

### License/Terms of Use:

MIT-0

## Use Case:

People reviewing emails, bills, and subscription notices use this skill to identify refund windows, renewal risks, warranty deadlines, and possible savings actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided email or bill text is sent to OpenAI's API and may contain financial or identity data.

Mitigation: Use the skill only when the user accepts this external data flow, and avoid submitting sensitive data unless that exposure is intended.

Risk: Generated cancellation, refund, or action links may be inaccurate or unsafe to click.

Mitigation: Verify links and action steps independently before clicking or allowing downstream automation to act on them.

Risk: The CLI can load a local .env file, which may expose unrelated secrets if run from the wrong directory.

Mitigation: Prefer explicit OPENAI_API_KEY injection for production use and keep unrelated secrets out of the working directory's .env file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/schchit/skills/claimback-radar)
- [Input schema](schema/input.json)
- [Output schema](schema/output.json)
- [Netflix subscription example](examples/netflix_email.md)
- [Amazon Prime renewal example](examples/amazon_prime_email.md)

## Skill Output:

**Output Type(s):** [JSON, guidance]

**Output Format:** [JSON object matching schema/output.json]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a confirmation_card, action_receipts, risk_flags, and optional summary; generated links and recommended actions should be checked before use.]

## Skill Version(s):

1.0.5 (source: server release metadata and pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
