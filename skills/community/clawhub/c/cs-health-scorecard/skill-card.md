## Description:

Build a structured customer health scorecard for a specific account, including RAG status, weighted dimension scores, renewal risk, key risks, and recommended actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

Customer success teams, account managers, and revenue leaders use this skill to assess account health, renewal risk, expansion potential, and next actions from recent account evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scorecards may contain sensitive customer, commercial, renewal, and support data.

Mitigation: Use only data appropriate for the target environment, limit unnecessary customer details, and follow the user's data handling policy.

Risk: The artifact references scripts/health_score.py, but that file was not included in the package evidence.

Mitigation: Do not run or rely on the helper unless the script is present and reviewed; calculate scores transparently from the documented weights when needed.

Risk: Health scores and renewal forecasts can mislead decisions if based on stale, vague, or unsupported account information.

Mitigation: Anchor every dimension score to named, recent evidence and use the documented rubric before presenting recommended actions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mohitagw15856/skills/cs-health-scorecard)
- [Skill Homepage](https://mohitagw15856.github.io/pm-claude-skills/skill/cs-health-scorecard.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown scorecard with tables, dimension detail, risks, recommended actions, and renewal forecast.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a fixed weighted scoring framework and RAG status bands; any referenced helper script should be verified before use.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
