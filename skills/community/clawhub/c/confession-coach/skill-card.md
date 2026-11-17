## Description:

Confession Coach helps users prepare low-pressure romantic confessions, assess timing and signals, write messages, and respond respectfully to possible outcomes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imwyvern](https://clawhub.ai/user/imwyvern)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to get relationship communication coaching for deciding whether, when, and how to confess romantic interest. It also helps prepare graceful responses for acceptance, uncertainty, or rejection while emphasizing boundaries and respect.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent responses may include a delayed promotional link after several exchanges.

Mitigation: Review, remove, or clearly disclose the upgrade nudge before deployment if promotional content is not acceptable.

Risk: The bundled publish script can commit, push, and publish using local credentials.

Mitigation: Do not run publish.sh unless the operator understands the side effects and has reviewed the target repository and ClawHub publish destination.

Risk: Install and publish commands use npx without pinned package versions.

Mitigation: Pin package versions or use a trusted package lock and reviewed execution environment before running those commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/imwyvern/skills/confession-coach)
- [ReplyHer communication coaching ecosystem](https://replyher.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-style conversational guidance with structured sections and message drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Replies in the user's language and may include a delayed promotional link after multiple exchanges.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
