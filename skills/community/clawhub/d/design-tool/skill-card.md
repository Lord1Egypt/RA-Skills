## Description:

Design Tool is a local Bash command-line utility for recording, searching, summarizing, and exporting timestamped design-related log entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and workflow operators can use this skill to log design-related activities, search prior entries, view recent history, and produce simple local exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package is labeled as Penpot but the artifact behavior is a broad local logging CLI, which may confuse users about the capabilities they are installing.

Mitigation: Review the commands and expected behavior before installation, and do not assume Penpot integration unless separate trusted evidence confirms it.

Risk: User-provided text can be retained in local log files under ~/.local/share/design-tool and later displayed through history, recent, search, stats, or export commands.

Mitigation: Avoid entering secrets, tokens, sensitive project details, private client information, or other confidential material into logged commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckchzh/skills/design-tool)
- [Publisher profile](https://clawhub.ai/user/ckchzh)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell command examples and plain-text CLI output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill stores user-provided log entries locally under ~/.local/share/design-tool and can export collected logs as JSON, CSV, or TXT.]

## Skill Version(s):

2.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
