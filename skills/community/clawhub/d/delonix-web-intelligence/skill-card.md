## Description:

A Chinese-language OpenClaw skill for hotel public-opinion monitoring that searches web results, summarizes competitive and complaint signals, drafts daily reports, and prepares Feishu card delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaoliuzhu](https://clawhub.ai/user/chaoliuzhu)

### License/Terms of Use:

MIT-0

## Use Case:

Hotel industry employees and analysts use this skill to monitor public opinion, competitor activity, complaints, industry trends, and crisis signals for brands such as Huazhu, Jinjiang, Atour, and Delonix.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install instructions include unpinned npx and GitHub build or download commands.

Mitigation: Pin package and release versions, verify integrity before execution, and avoid running the commands on sensitive machines until reviewed.

Risk: The skill supports broad web and platform data collection for public-opinion monitoring.

Mitigation: Limit collection scope to approved business topics, respect platform terms and rate limits, and review data handling before sharing reports.

Risk: Scheduled Feishu delivery can send recurring reports to a hardcoded chat destination.

Mitigation: Replace the chat ID with an approved destination, keep scheduled delivery disabled until explicitly needed, and narrow invocation triggers to Delonix-specific phrases.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chaoliuzhu/skills/delonix-web-intelligence)
- [AutoCLI repository referenced by artifact](https://github.com/nashsu/AutoCLI.git)
- [AutoCLI v0.3.7 release artifact referenced by artifact](https://github.com/nashsu/AutoCLI/releases/download/v0.3.7/autocli-x86_64-unknown-linux-musl.tar.gz)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, Feishu card markup, JSON search output, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can generate local daily report files under /tmp/delonix-intelligence when the bundled report script is run.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact text references v1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
