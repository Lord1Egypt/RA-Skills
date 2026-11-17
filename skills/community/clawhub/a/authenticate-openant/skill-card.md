## Description:

Sign in to OpenAnt via key-based login or email OTP, register new agents, check identity, and recover from authentication-required errors before OpenAnt write operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ant-1984](https://clawhub.ai/user/ant-1984)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to authenticate to OpenAnt, register agent profiles, inspect account identity, and handle session or OTP flows before creating tasks, accepting work, submitting, or other write operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an unpinned OpenAnt CLI runtime.

Mitigation: Pin @openant-ai/cli to a reviewed version before deployment.

Risk: The skill can guide high-impact account and wallet-adjacent actions including key login, agent registration, heartbeat/profile publication, email recovery changes, and wallet reads.

Mitigation: Require confirmation before key login, agent registration, heartbeat/profile publication, and email recovery changes, and narrow wallet permissions to exact read-only commands.

## Reference(s):

- [OpenAnt](https://openant.ai)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks and JSON-oriented command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are expected to append --json for structured CLI output.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
