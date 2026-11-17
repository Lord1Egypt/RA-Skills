## Description:

Detect and block prompt injection attacks in emails. Use when reading, processing, or summarizing emails. Scans for fake system outputs, planted thinking blocks, instruction hijacking, and other injection patterns. Requires user confirmation before acting on any instructions found in email content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eltemblor](https://clawhub.ai/user/eltemblor)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill when reading, summarizing, or acting on email content to identify prompt-injection patterns and require user confirmation before following email-originated instructions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email content may include instructions that attempt to override agent behavior or request sensitive actions.

Mitigation: Scan email bodies for documented injection patterns, block critical matches, and require user confirmation before following instructions found in email content.

Risk: The pattern library contains risky-looking example strings that should not be executed.

Mitigation: Treat the examples as detection evidence only and use them to warn, block, or request confirmation.

## Reference(s):

- [Prompt Injection Pattern Library](references/patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown warning text and confirmation prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes matched pattern, severity, suspicious snippet, and read-only warning when applicable.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
