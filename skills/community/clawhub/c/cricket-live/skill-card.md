## Description:

Provides live cricket scores, detailed scorecards, upcoming matches, recent results, IPL standings, and match alerts through CricketData.org API scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harshilmathur](https://clawhub.ai/user/harshilmathur)

### License/Terms of Use:

MIT

## Use Case:

Sports fans, analysts, and agent users use this skill to retrieve cricket scores, schedules, results, IPL standings, and match alerts from a terminal-accessible workflow. It is useful when an agent needs current cricket information and can run shell scripts with a CricketData.org API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a CricketData.org API key and sends it to the service in API requests.

Mitigation: Use a limited, rotatable API key through CRICKET_API_KEY and run the skill only on trusted single-user machines.

Risk: Local cache and alert state are stored in shared temporary paths.

Mitigation: Avoid shared or multi-user hosts until cache and state storage are moved to private per-user directories.

Risk: Match identifiers can be used in filenames and URL parameters.

Mitigation: Validate match IDs before using match-detail workflows in automation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/harshilmathur/skills/cricket-live)
- [CricketData.org](https://cricketdata.org)
- [CricketData API Base Endpoint](https://api.cricapi.com/v1)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown-like messaging output with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CRICKET_API_KEY plus local curl and jq; uses local cache and alert state files.]

## Skill Version(s):

1.0.0 (source: release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
