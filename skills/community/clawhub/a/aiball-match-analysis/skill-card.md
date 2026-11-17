## Description:

Reads AI Ball's public football match record to explain home, draw, and away probabilities, completed results, and historical model performance without recommending a side.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ava78158](https://clawhub.ai/user/ava78158)

### License/Terms of Use:

MIT-0

## Use Case:

Football fans and analysts use this skill to review AI Ball's recorded match probabilities, results, competition coverage, and performance against the pre-match favourite.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Match probabilities may be mistaken for betting advice.

Mitigation: Present all three outcomes and their uncertainty; do not recommend a side or a stake.

Risk: Readings appear shortly before kick-off, and a match without a recorded score may already have started or finished.

Mitigation: Check kick-off time against the user's time zone and describe missing results as not yet recorded.

## Reference(s):

- [AI Ball public record API reference](references/api.md)
- [AI Ball open record](https://aiball.samagent.ai/en/record?src=skill)
- [AI Ball match analysis on ClawHub](https://clawhub.ai/ava78158/skills/aiball-match-analysis)

## Skill Output:

**Output Type(s):** [Analysis, Guidance]

**Output Format:** [Markdown text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports all three outcomes with uncertainty and links to the open record when citing figures.]

## Skill Version(s):

1.0.5 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
