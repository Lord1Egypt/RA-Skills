## Description:

Track Closing Line Value — the gold standard for measuring betting edge. Log placement odds, fetch closing lines, compute CLV, and generate performance reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rsquaredsolutions2026](https://clawhub.ai/user/rsquaredsolutions2026)

### License/Terms of Use:

MIT-0

## Use Case:

External bettors and betting analysts use this skill to log wagers, compare placement odds against closing lines, calculate closing line value, and summarize whether betting performance reflects edge or variance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented command pattern can turn supplied bet fields into executable Python or SQL.

Mitigation: Review before installing; use only trusted, simple numeric and text inputs, and prefer a revised version that validates odds and uses SQLite parameter binding.

Risk: Betting history is stored locally, and the artifact does not document how stored records can be deleted.

Mitigation: Document and review a deletion procedure for ~/.openclaw/data/clv.db before using the skill with sensitive betting history.

Risk: The security guidance flags unused credential or tool requirements until implemented.

Mitigation: Remove unused credential and tool requirements or document their implemented use before release.

## Reference(s):

- [CLV Tracker skill page](https://clawhub.ai/rsquaredsolutions2026/skills/clv-tracker)
- [The Odds API](https://the-odds-api.com/)
- [AgentBets CLV Tracker tutorial](https://agentbets.ai/guides/openclaw-clv-tracker-skill/)
- [OpenClaw Skills series](https://agentbets.ai/guides/#openclaw-skills)
- [Agent Betting Stack](https://agentbets.ai/guides/agent-betting-stack/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and SQLite command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference a local SQLite database at ~/.openclaw/data/clv.db and an ODDS_API_KEY credential.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
