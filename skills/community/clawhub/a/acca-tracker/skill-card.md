## Description:

Track football accumulator betting slips from photos or text, check live scores on a recurring schedule, and report per-leg status with overall accumulator health and cash-out context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[svenmedina07-ship-it](https://clawhub.ai/user/svenmedina07-ship-it)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to parse football accumulator or parlay betting slips, monitor live match results, and receive concise updates on whether each leg is winning, lost, or pending. It is intended for bet tracking and status reporting, not betting advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes betting-slip contents and may expose stake, odds, teams, and payout information to the agent.

Mitigation: Install only if sharing betting-slip contents is acceptable, and confirm the parsed slip before tracking starts.

Risk: Recurring background score checks can continue after the user no longer needs updates.

Mitigation: Use the documented stop-tracking flow when updates are no longer wanted; the skill also uses bounded scheduled checks.

Risk: Live score sources may lag, be unavailable, or provide incomplete coverage for some matches.

Mitigation: Require reports to state when data is unavailable and avoid guessing scores or outcomes.

## Reference(s):

- [Acca Tracker on ClawHub](https://clawhub.ai/svenmedina07-ship-it/skills/acca-tracker)
- [Bet Type Reference](references/bet-types.md)
- [Data Source Strategy](references/data-sources.md)
- [TheSportsDB Events API](https://www.thesportsdb.com/api/v1/json/3/eventsday.php?d={today}&s=Soccer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown status reports with tables, parsed slip summaries, scheduled-check prompts, and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include recurring background score checks, estimated cash-out context, and explicit no-data status when scores cannot be verified.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
