## Description:

Your personal Deadline assistant. Use when you need deadline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use Deadline as an offline command-line assistant for drafting, editing, optimizing, scheduling, and reviewing content-related entries. The tool records activity locally and supports status checks, search, recent history, statistics, and exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-entered text is retained on the local machine under ~/.local/share/deadline.

Mitigation: Avoid entering passwords, credentials, private business content, or sensitive personal data unless local file permissions and retention are acceptable.

Risk: Exported files may contain stored user content and should be treated as sensitive when shared or imported elsewhere.

Mitigation: Review JSON, CSV, or TXT exports before sharing them, and delete local logs or exports when they are no longer needed.

## Reference(s):

- [Deadline on ClawHub](https://clawhub.ai/xueyetianya/skills/deadline)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Guidance]

**Output Format:** [Plain text CLI output with optional JSON, CSV, or TXT export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores user-entered content and history locally under ~/.local/share/deadline.]

## Skill Version(s):

2.0.1 (source: ClawHub release metadata; artifact frontmatter and script report 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
