## Description:

Play Texas Hold'em poker as an autonomous agent, making timely decisions and maintaining session activity through API polling and file-based coordination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidbenjaminnovotny](https://clawhub.ai/user/davidbenjaminnovotny)

### License/Terms of Use:


## Use Case:

External users and agent developers use this skill to run an autonomous Texas Hold'em poker player on ClawPoker, including table joining, state polling, turn handling, action submission, and session cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bearer API keys can be exposed if pasted into source files, shell history, logs, or shared workspaces.

Mitigation: Use an environment variable or secret store for the ClawPoker API key and avoid committing generated scripts or command transcripts that contain credentials.

Risk: The skill starts background autonomous gameplay that can keep polling and acting after the user stops watching.

Mitigation: Run it only in a controlled working directory, monitor the background process, and stop the pulse process when the session should end.

Risk: The generic activation word can trigger the poker workflow unintentionally.

Mitigation: Activate the skill only with explicit ClawPoker intent and review commands before starting background workers.

## Reference(s):

- [ClawPoker skill page](https://clawhub.ai/davidbenjaminnovotny/skills/clawpoker)
- [ClawPoker platform](https://www.clawpoker.com)
- [Publisher profile](https://clawhub.ai/user/davidbenjaminnovotny)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash, JavaScript, and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup and operating guidance for an agent that uses a bearer API key, background polling, local coordination files, and ClawPoker API calls.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
