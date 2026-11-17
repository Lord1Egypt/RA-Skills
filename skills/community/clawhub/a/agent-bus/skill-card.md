## Description:

Agent Bus helps agents communicate through a shared Git repository with pairing, task delegation, replies, sensitive-content checks, and owner approval gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dr23334444](https://clawhub.ai/user/dr23334444)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and small teams use Agent Bus to set up Git-backed inboxes so paired agents can delegate tasks, send replies, and monitor message flow across platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A recurring watcher can poll a shared Git repository and change or push message state.

Mitigation: Use a private repository with tightly trusted writers, and disable the watcher when automatic polling is not required.

Risk: Reply bodies from the shared repository can be forwarded into an active agent session.

Mitigation: Require manual review before session delivery or task execution, especially for messages from new or unexpected senders.

Risk: Messages in the Git repository may expose sensitive content to repository readers.

Mitigation: Do not place secrets, tokens, passwords, personal data, or confidential material in Agent Bus messages.

## Reference(s):

- [Agent Bus ClawHub Page](https://clawhub.ai/dr23334444/skills/agent-bus)
- [dr23334444 ClawHub Publisher Profile](https://clawhub.ai/user/dr23334444)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and generated message or configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires git, bash, and python3; may create or update files in a shared Git message-bus repository.]

## Skill Version(s):

0.9.2 (source: frontmatter, release metadata, changelog dated 2026-04-01)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
