## Description:

Enhanced document summarizer with smart summaries, bullet extraction, executive summaries, chapter breakdowns, multi-document comparison, and translate-and-summarize support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users can use this skill to have an agent summarize local documents, extract keywords and outlines, compare files, export summaries, and inspect document statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configuration command can be abused to run arbitrary shell commands if untrusted text or an agent controls config keys or values.

Mitigation: Do not let untrusted text or autonomous agents choose config keys or values until key allowlisting and safe file rewriting are implemented.

Risk: Processed document paths are persistently logged under the user's home directory.

Mitigation: Use the skill only on non-sensitive documents unless local path history in $HOME/.doc-summarize-pro/history.log is acceptable.

Risk: The security evidence marks the release verdict as suspicious.

Mitigation: Review the scripts before installing and run the skill with least-privileged local access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xueyetianya/skills/doc-summarize-pro)
- [Publisher profile](https://clawhub.ai/user/xueyetianya)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration]

**Output Format:** [Plain text, Markdown, or JSON summaries and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes local files and directories; stores configuration and command history under $HOME/.doc-summarize-pro.]

## Skill Version(s):

3.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
