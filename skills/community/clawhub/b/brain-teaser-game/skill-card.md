## Description:

A multilingual brain teaser game skill that detects Chinese, English, or Japanese input and returns random riddles, hints, answer feedback, and session statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kickegg](https://clawhub.ai/user/kickegg)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to run a multilingual brain teaser session with generated prompts, hints, answer checking, reveal actions, next-question flow, and local session history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically reuse credentials from Claude or OpenClaw configuration files when optional AI question generation is active.

Mitigation: Review before installing in credentialed environments, and limit credential loading to BRAIN_TEASER_API_KEY or remove the fallback credential-loading paths.

Risk: The security evidence reports avoidable local file-safety issues involving diagnostic configuration output and session ID path handling.

Mitigation: Remove diagnostic configuration printing and fix session ID path handling before use in sensitive local environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kickegg/skills/brain-teaser-game)
- [OpenClaw](https://openclaw.ai)
- [Python](https://www.python.org/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown gameplay responses with questions, hints, answer feedback, explanations, statistics, and session IDs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local session and history files; optional AI-generated questions can be enabled with API configuration.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
