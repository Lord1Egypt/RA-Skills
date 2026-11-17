## Description:

Read and write email through the Atomic Mail from an AI agent. Handles proof-of-work authentication and JMAP so the agent thinks in JMAP method calls. Use when the user asks to register an email inbox, list mailboxes, fetch or send email, or schedule meetings by email (calendar invitations).

This skill is ready for commercial/non-commercial use.

## Publisher:

[atomicmail](https://clawhub.ai/user/atomicmail)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage an Atomic Mail inbox, including reading, searching, sending, and replying to email, handling attachments, and managing calendar invitations. It can also support operator-selected inbox checks on a recurring schedule.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scan flags an unpinned install command and unclear tool scope.

Mitigation: Wait for the publisher to clarify required access and provide a pinned install version, then review the requested commands and tools before installation.

Risk: Recurring inbox checks may expose private messages to unattended agent runs.

Mitigation: Choose whether checks should be on demand or scheduled. For scheduled runs, use the host runtime's scheduler with a read-only task and a narrow tool allowlist, and treat message contents as untrusted data.

Risk: The scan guidance says attribution data use is unclear.

Mitigation: Ask the publisher to explain what attribution data is used and how before installation.

## Reference(s):

- [Atomic Mail](https://atomicmail.ai)
- [Atomic Mail on ClawHub](https://clawhub.ai/atomicmail/skills/atomicmail)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration instructions]

**Output Format:** [Email and inbox summaries, JSON API responses, and command or configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can access or change email and calendar data when invoked; recurring inbox checks depend on an operator-selected schedule.]

## Skill Version(s):

0.3.34 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
