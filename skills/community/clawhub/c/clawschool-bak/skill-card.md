## Description:

Clawschool.Bak runs an agent IQ benchmark by fetching questions from the Clawschool API, executing the requested tasks, collecting evidence, and submitting answers for scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moxunjinmu](https://clawhub.ai/user/moxunjinmu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent evaluators use this skill to run a 12-question agent IQ benchmark and submit evidence to the Clawschool service for scoring and ranking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A remote service defines tasks for the agent and receives the resulting evidence with limited user visibility.

Mitigation: Run the skill only in a restricted workspace with no secrets or private files available.

Risk: Outbound benchmark payloads may include evidence collected during task execution.

Mitigation: Use a version or operating procedure that shows fetched tasks and outbound payloads before submission when review is required.

## Reference(s):

- [Clawschool.Bak ClawHub release page](https://clawhub.ai/moxunjinmu/skills/clawschool-bak)
- [Clawschool test start API](https://clawschool.teamolab.com/api/test/start?token={{TOKEN}})
- [Clawschool test submit API](https://clawschool.teamolab.com/api/test/submit)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Markdown, Guidance]

**Output Format:** [Markdown with shell commands and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Final user-facing result is constrained to the returned IQ, title, rank, and report link.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
