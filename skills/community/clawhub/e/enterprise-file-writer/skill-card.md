## Description:

Writes content to local text, code, configuration, Word, and Excel files in enterprise environments, with encoding handling for UTF-8 and GBK.

This skill is ready for commercial/non-commercial use.

## Publisher:

[endcy](https://clawhub.ai/user/endcy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create, overwrite, or append local files when a user has explicitly requested file-writing work. It is suited to authorized generation of text, code, configuration, log, DOCX, and XLSX outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can overwrite or append to local files, including important configuration, script, credential, or spreadsheet files.

Mitigation: Require explicit user approval for the target path and content, keep backups for important files, and avoid production configs, .env files, scripts, and existing spreadsheets unless the user has approved the write.

Risk: The server security guidance flags confirmed data-integrity flaws around non-UTF-8 encoding and XLSX append behavior.

Mitigation: Use UTF-8 when possible, verify non-UTF-8 output after writing, and avoid relying on XLSX append to preserve existing workbook data.

Risk: The artifact supports a force option that can bypass safety warnings.

Mitigation: Do not use force-style bypasses unless the user explicitly approves the specific risky write after reviewing the warning.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/endcy/skills/enterprise-file-writer)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [CHANGELOG.md](artifact/CHANGELOG.md)
- [VERIFICATION_REPORT.md](artifact/VERIFICATION_REPORT.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands and local file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful runs report the file path and bytes written; failures return error text.]

## Skill Version(s):

1.2.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
