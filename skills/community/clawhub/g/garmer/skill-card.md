## Description:

Extract health and fitness data from Garmin Connect including activities, sleep, heart rate, stress, steps, and body composition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[garrza](https://clawhub.ai/user/garrza)

### License/Terms of Use:

MIT

## Use Case:

Developers, health insight builders, and AI agents use Garmer to retrieve Garmin Connect activity, sleep, heart rate, stress, steps, body composition, hydration, and respiration data for analysis or user-facing health summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Garmer stores reusable Garmin account tokens on disk for future sessions.

Mitigation: Use interactive login, protect or relocate the token directory such as ~/.garmer/garmin_tokens or GARMER_TOKEN_DIR, and remove tokens when access is no longer needed.

Risk: Garmer exports sensitive health and fitness data as JSON that may be copied, committed, or shared with other systems.

Mitigation: Store exports in protected locations, avoid committing or sharing exported JSON files, and review outputs before sending them to AI or chat systems.

Risk: The garmer update command can pull new code from a git remote and change installed behavior.

Mitigation: Run updates only after verifying the git remote and reviewing the incoming code source.

## Reference(s):

- [Garmer Skill Page](https://clawhub.ai/garrza/skills/garmer)
- [README](README.md)
- [Garmer API Reference](references/REFERENCE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON, files]

**Output Format:** [Markdown guidance with shell and Python examples; CLI commands may return human-readable text, JSON, or exported JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.10+, a Garmin Connect account, and garmer CLI installation via pip or uv.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata; artifact package metadata is 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
