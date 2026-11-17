## Description:

Bracket Oracle helps agents generate NCAA March Madness brackets by combining team ratings, Monte Carlo tournament simulation, public-pick analysis, and pool-aware optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lastandy](https://clawhub.ai/user/lastandy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and bracket pool participants use this skill to fetch college basketball ratings, simulate NCAA tournament outcomes, and generate pool-aware bracket picks with strategy explanations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Premium KenPom credentials could be exposed if placed in source files or shared transcripts.

Mitigation: Keep credentials in local environment variables or a secrets manager, and avoid committing or pasting them into prompts.

Risk: Optional dependencies and live sports-data sources may change or become unavailable.

Mitigation: Install dependencies from trusted package indexes, prefer pinned versions, and review generated picks when data fetches fail or fall back.

Risk: Bracket recommendations are probabilistic and may be stale, incomplete, or wrong when public-pick data is unavailable.

Mitigation: Treat outputs as decision support, refresh source data near submission deadlines, and manually review high-impact picks.

## Reference(s):

- [Bracket Oracle on ClawHub](https://clawhub.ai/lastandy/skills/bracket-oracle)
- [Bart Torvik T-Rank](https://barttorvik.com/)
- [Agent Bracket League 2026](https://github.com/lastandy/bracket-league-2026)
- [ESPN Tournament Challenge Group](https://fantasy.espn.com/games/tournament-challenge-bracket-2026/group?id=83062dd9-bc6e-4867-896e-d57926480488)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; generated bracket outputs are dictionary or JSON-like data structures.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use live third-party sports data and locally cached JSON; optional KenPom credentials are read from environment variables.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
