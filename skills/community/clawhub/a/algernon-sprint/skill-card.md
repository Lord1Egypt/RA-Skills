## Description:

Timed interleaved study sprint for OpenAlgernon that shuffles cards from installed materials and ends with a post-sprint retrieval test to measure retention gain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antoniovfranco](https://clawhub.ai/user/antoniovfranco)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenAlgernon users use this skill to run timed, interleaved study review sessions across installed materials and compare sprint retention with a short post-sprint retrieval test.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a hardcoded local study database path that may not exist or may point at the wrong study data in another environment.

Mitigation: Review or adjust the configured database path before running the sprint workflow.

Risk: The workflow records sprint and retention metrics in a local conversation log.

Mitigation: Use only when local retention metric logging is acceptable, or adjust logging behavior before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/antoniovfranco/skills/algernon-sprint)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and study-session prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces timed review prompts, retention summaries, FSRS scheduling guidance, and a local session log entry.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
