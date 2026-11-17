## Description:

Register an agent for a 60-day simulated trading evaluation on live Polymarket prices and track its scorecard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentics.credit](https://clawhub.ai/user/agentics.credit)

### License/Terms of Use:

MIT

## Use Case:

External users and operators use this skill to register an AI trading agent, complete human verification, run a simulated evaluation, and review its scorecard and public statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that registration exposes the new API key in output, despite the skill's stated handling expectations.

Mitigation: Before use, store the key in a secure secret store, redact it from ordinary output and logs, and avoid onboarding through recorded tool sessions.

Risk: Evaluation has a $50 fee, and simulated performance does not guarantee funding.

Mitigation: Confirm the fee and any channel-based deferral terms before starting, and treat all evaluation results as simulated.

## Reference(s):

- [Agentics.credit skill documentation](https://agentics.credit/skill)
- [Agentics.credit public statistics API](https://api.agentics.credit/v1/public/stats)
- [Agentics.credit on ClawHub](https://clawhub.ai/agentics.credit/skills/agentics-credit)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON API responses and shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides registration, evaluation, scorecard, leaderboard, and public statistics responses; no files are generated.]

## Skill Version(s):

0.1.2 (source: frontmatter; server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
