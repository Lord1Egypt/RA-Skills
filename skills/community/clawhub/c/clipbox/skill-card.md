## Description:

Save and organize reusable text snippets for quick retrieval. Use when storing code fragments, saving command templates, or building snippet libraries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other external users use Clipbox to save timestamped snippets, command templates, lint or check results, diffs, and reports locally for later search, review, or export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved snippets and command text are stored locally in plaintext.

Mitigation: Avoid storing secrets, credentials, proprietary code, or other sensitive content in Clipbox logs.

Risk: CSV, JSON, and text exports may include unsanitized saved content.

Mitigation: Review exported files before sharing or opening them in tools that may evaluate formulas or markup.

## Reference(s):

- [Clipbox ClawHub page](https://clawhub.ai/xueyetianya/skills/clipbox)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell command examples and local file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local plaintext log and export files under ~/.local/share/clipbox.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
