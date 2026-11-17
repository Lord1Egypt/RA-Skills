## Description:

Dialog is advertised as a dialog UI and design skill, but the reviewed artifact implements shell commands for persistent local JSONL record management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents may invoke Dialog for local entry storage tasks such as add, list, search, remove, export, stats, and configuration. Treat the advertised UI-generation purpose as unverified for this release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release description does not match the artifact behavior.

Mitigation: Review the artifact as a local data-record tool and do not rely on it for dialog UI generation unless the package is corrected.

Risk: The script writes persistent records, can delete records, and can export stored data.

Mitigation: Use non-sensitive test data, set DIALOG_DIR to an isolated directory when evaluating, and review data before export or removal.

Risk: Security guidance flags unsafe parsing and configuration behavior.

Mitigation: Avoid untrusted arguments and sensitive input until the package is corrected and accurately described.

## Reference(s):

- [Dialog on ClawHub](https://clawhub.ai/ckchzh/skills/dialog)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands; command output is plain text, with JSONL or CSV export files when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script stores records under ~/.dialog by default, or under DIALOG_DIR when configured.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
