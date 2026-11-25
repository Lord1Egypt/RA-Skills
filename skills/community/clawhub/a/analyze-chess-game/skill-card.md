## Description:

Routes users to Chessigma to analyze chess games or positions, check moves and openings, calculate a rating change for one game, or view the daily puzzle.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mehdi-bh](https://clawhub.ai/user/mehdi-bh)

### License/Terms of Use:

MIT-0

## Use Case:

Chess players use the skill to review a specific game or position, check moves, identify openings, calculate a rating change for one game, or open the daily puzzle. It routes users to Chessigma and reports analysis only when that information has actually been retrieved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PGNs may contain identifying details or private annotations and can be sent to and stored by Chessigma when submitted; opening a PGN-bearing link also sends the PGN to that site. Scan coverage is incomplete because a local reference could not be resolved.

Mitigation: Disclose the data handling and obtain confirmation before submitting or opening a PGN-bearing link. Remove identifying details and private annotations first when appropriate, and review the unresolved reference before relying on the skill.

## Reference(s):

- [Chessigma](https://www.chessigma.com)
- [Chessigma OpenAPI](https://www.chessigma.com/openapi.json)
- [Chessigma API catalog](https://www.chessigma.com/.well-known/api-catalog)
- [Chessigma Supercoach](https://www.chessigma.com/supercoach)

## Skill Output:

**Output Type(s):** [Text, Analysis, Guidance]

**Output Format:** [Natural-language text and Chessigma links; API responses may be JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Analysis details are reported only when retrieved from Chessigma; deep links open the analysis on Chessigma.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
