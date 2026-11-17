## Description:

Changelog is a command-line utility for recording changelog-related entries, checking status, and exporting local logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users can use this skill to record changelog-related terminal activity, review recent entries, check status, and export local records for downstream review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores command inputs in plaintext local logs under ~/.local/share/changelog.

Mitigation: Use it only for non-sensitive changelog activity and avoid passing secrets, tokens, private prompts, or confidential drafts to its commands.

Risk: Exported JSON and CSV files may contain unsanitized logged text.

Mitigation: Inspect and sanitize exported files before sharing them or opening them in spreadsheet tools.

Risk: The security verdict is suspicious because the implementation behaves mainly as a persistent local text logger/exporter with unclear scope.

Mitigation: Review the artifact and scanner guidance before installing or running it in an agent environment.

## Reference(s):

- [Changelog ClawHub skill page](https://clawhub.ai/xueyetianya/skills/changelog)
- [xueyetianya ClawHub publisher profile](https://clawhub.ai/user/xueyetianya)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Files, JSON, CSV]

**Output Format:** [Terminal text plus local export files in JSON, CSV, or TXT]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes persistent local logs under ~/.local/share/changelog.]

## Skill Version(s):

2.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
