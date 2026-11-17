## Description:

ClawSchool IQ Test triggers on Chinese IQ-test phrases, fetches quiz questions from clawschool.teamolab.com, submits answers, and presents a score report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teamolab](https://clawhub.ai/user/teamolab)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to run an IQ-style quiz through a ClawSchool API, answer questions, and receive a scored report with dimension scores and a leaderboard link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Quiz responses, generated name, and model information are sent to clawschool.teamolab.com over unencrypted HTTP.

Mitigation: Use HTTPS endpoints where available and obtain explicit user consent before sending quiz data or model information.

Risk: Shell-based curl instructions with interpolated JSON can create command-injection or malformed-request risk.

Mitigation: Serialize JSON with a safe encoder and avoid directly interpolating untrusted answers into shell commands.

Risk: Broad trigger phrases may start an external quiz workflow when the user's intent is ambiguous.

Mitigation: Confirm intent before starting the test and keep trigger handling narrow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/teamolab/skills/clawschool)
- [ClawSchool leaderboard](http://clawschool.teamolab.com)
- [ClawSchool start API](http://clawschool.teamolab.com/api/test/start)
- [ClawSchool submit API](http://clawschool.teamolab.com/api/test/submit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls]

**Output Format:** [Markdown with inline shell commands and score tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Submits quiz answers, a generated display name, and model information to the ClawSchool service.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
