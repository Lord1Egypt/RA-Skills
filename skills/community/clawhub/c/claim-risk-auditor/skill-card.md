## Description:

Checks copy, academic writing, promotional scripts, and product descriptions for high-risk claims, evidence gaps, and safer phrasing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, marketers, researchers, trainers, and agents use this skill to review copied content for risky assertions, missing support, and more cautious wording.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read the current macOS clipboard on broad prompts without an explicit confirmation step, and the clipboard may contain passwords, tokens, private notes, or unrelated confidential text.

Mitigation: Invoke it only after intentionally copying the text to review, and clear or replace sensitive clipboard contents before use.

Risk: Clipboard ingestion depends on local Node.js and macOS pbpaste availability.

Mitigation: Confirm those binaries are available before relying on clipboard-based review, or provide the text directly to the agent instead.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/claim-risk-auditor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text analysis, with shell output when clipboard access is requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and macOS pbpaste for clipboard ingestion.]

## Skill Version(s):

1.0.0 (source: server release evidence and CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
