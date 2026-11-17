## Description:

Autonomous mobile robot fleet manager for AMR task entries, CSV or JSON exports, and status checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators can use this skill to run an AMR-themed local notes and configuration utility that records entries, lists and searches them, exports JSON or CSV, and reports simple status or statistics. It should not be used for real robot or fleet operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is advertised as an autonomous mobile robot fleet manager, but security evidence says it behaves like a local notes and configuration shell utility.

Mitigation: Do not rely on it for real robot, facility, or fleet operations; treat outputs as local log entries only.

Risk: The script writes to ~/.amr by default and can create amr-export.json or amr-export.csv in the current directory.

Mitigation: Run it only in non-sensitive directories and set AMR_DIR to an isolated path when testing or using it.

Risk: Security guidance warns against passing untrusted text to add, search, or config.

Mitigation: Use trusted input only and review generated data or configuration files before sharing or reusing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bytesagain-lab/skills/amr)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands and command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local data under ~/.amr and export amr-export.json or amr-export.csv in the current directory.]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
