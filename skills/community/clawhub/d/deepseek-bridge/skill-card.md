## Description:

DeepSeek Bridge exposes the DeepSeek Chat API through a local HTTP /ask endpoint with SQLite-backed conversation state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawhub-master](https://clawhub.ai/user/clawhub-master)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and local agent operators use this skill to route prompts to DeepSeek through a local Flask bridge, receive answers, and persist request status in SQLite.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts are sent to DeepSeek and saved with answers in a local SQLite database.

Mitigation: Use only with prompts that are acceptable to send to DeepSeek and store locally; review retention and access controls for chat_shared.db.

Risk: The bridge imports executable code from a hardcoded external path.

Mitigation: Verify which db_shared.py is imported before installation and avoid writable shared import paths.

Risk: Broad auto-start or trigger behavior could invoke the bridge in sensitive environments.

Mitigation: Disable broad auto-start or trigger rules where prompts or local state require tighter review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clawhub-master/skills/deepseek-bridge)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON HTTP response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The local bridge returns DeepSeek answers as JSON and records prompt, answer, status, and timestamps in SQLite.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
