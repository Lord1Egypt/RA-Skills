## Description:

Apple Mail search on macOS with fast metadata and full body lookup for finding messages by subject, sender, recipient, date, opening messages, and reading full body text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durtydhiana](https://clawhub.ai/user/durtydhiana)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and macOS users use this skill to search local Apple Mail messages, inspect message bodies, and open matching emails from an agent workflow. It is intended for local mailbox discovery and triage, not composing or sending email.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a third-party global npm CLI that can read private local Apple Mail metadata and message bodies.

Mitigation: Install only when that local email access is acceptable, review or pin the npm package version, and prefer the documented read-only or copy modes where available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/durtydhiana/skills/apple-mail-search-safe-5-0-4)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference JSON output from the fruitmail CLI when the user requests structured mail search results.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
