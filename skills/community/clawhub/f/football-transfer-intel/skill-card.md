## Description:

Football transfer intelligence: real-time rumour tracking, AI Truth Meter credibility scores, and multi-source verification across 137,000+ transfer events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leeleon](https://clawhub.ai/user/leeleon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and football analysts use this skill to check trending transfer stories, retrieve player-specific rumour details, and assess the credibility of proposed player-to-club moves.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Player and club search terms are sent to Rising Transfers for football transfer lookup and verification.

Mitigation: Use hot topics without an API key when possible and avoid including unrelated private information in transfer queries.

Risk: Authenticated detailed queries send RT_API_KEY to the Rising Transfers API service.

Mitigation: Store the key in the RT_API_KEY environment variable and use it only for the documented Rising Transfers endpoints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leeleon/skills/football-transfer-intel)
- [Rising Transfers API](https://api.risingtransfers.com)
- [Rising Transfers skill repository](https://github.com/LeoandLeon/rising-transfers-clawhub-skills)
- [Hot Topics endpoint](https://api.risingtransfers.com/api/v1/intelligence/hot-topics)
- [Transfer Detail endpoint](https://api.risingtransfers.com/api/v1/intelligence/transfer)
- [Truth Meter verification endpoint](https://api.risingtransfers.com/api/v1/intel/verify)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown summaries with transfer scores, source evidence, timestamps, and concise error guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require RT_API_KEY for detailed transfer lookups; hot topics can be used without an API key.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
