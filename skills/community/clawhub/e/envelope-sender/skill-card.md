## Description:

Guides an agent to send a user-specified local PDF document for signature through eSignGlobal by calling the eSignGlobal CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weipengcopyright](https://clawhub.ai/user/weipengcopyright)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to collect an explicit absolute PDF path, signer names, signer emails, and an optional subject, then send one document for signature through eSignGlobal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles PDFs, signer names, signer emails, envelope metadata, and an eSignGlobal API key while invoking an unpinned external CLI.

Mitigation: Install only a vetted, pinned, preinstalled CLI version; run it with least-privilege access to the intended PDF; and keep ESIGNGLOBAL_APIKEY out of logs and local storage.

Risk: Unsafe command construction could expose file paths, signer JSON, or subjects to shell interpretation.

Mitigation: Pass file paths, signer JSON, and subjects as structured command arguments instead of shell-interpolated strings.

## Reference(s):

- [Envelope Sender on ClawHub](https://clawhub.ai/weipengcopyright/skills/envelope-sender)
- [Publisher profile](https://clawhub.ai/user/weipengcopyright)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns the external eSignGlobal CLI result and does not implement upload logic inside the skill.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
