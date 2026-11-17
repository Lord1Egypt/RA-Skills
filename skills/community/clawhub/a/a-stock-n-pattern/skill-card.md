## Description:

Provides an A-share N-pattern stock-screening interface that returns structured stock candidates with pattern stage, volume, stop-loss, target, and rationale fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinboh68-prog](https://clawhub.ai/user/jinboh68-prog)

### License/Terms of Use:

MIT-0

## Use Case:

External users interested in A-share technical analysis use this skill to request N-pattern stock candidates as trading-reference data. Agents can summarize the returned candidates, stages, volume signals, targets, stop losses, and rationale for user review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Returned stocks, targets, stop losses, and volume data may be unverified static examples while appearing current.

Mitigation: Treat all signals as reference-only until the publisher supplies auditable live-data provenance and source timestamps.

Risk: The release describes x402 payment enforcement, but the provided API artifact does not show the documented enforcement behavior.

Mitigation: Verify real payment enforcement before installing, paying for, or depending on the skill.

Risk: Trading-reference output could be mistaken for personalized investment advice.

Mitigation: Review outputs independently, apply risk controls, and avoid relying on the skill as the sole basis for financial decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jinboh68-prog/skills/a-stock-n-pattern)
- [Publisher profile](https://clawhub.ai/user/jinboh68-prog)
- [Published API endpoint](https://a-stock-signals.vercel.app/n)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Structured JSON data that an agent may summarize as text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes stock code, name, N-pattern stage, strength indicator, volume ratio, stop-loss level, target level, and rationale when returned by the API.]

## Skill Version(s):

1.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
