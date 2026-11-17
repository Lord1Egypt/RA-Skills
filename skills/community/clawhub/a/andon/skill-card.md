## Description:

Andon alert and production status board for JSON and CSV Andon tasks and status checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams can use this skill to manage a local Andon-style production status log, including adding, listing, searching, removing, exporting, and summarizing entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and mutates local data under ~/.andon by default.

Mitigation: Review the configured ANDON_DIR before use and avoid running the skill in environments where local data mutation is not acceptable.

Risk: Security evidence reports unsafe shell and serialization handling.

Mitigation: Do not use untrusted arguments or allow another agent to supply arguments until the config, JSON, CSV, and deletion behavior is fixed and documented.

Risk: The remove and export commands can delete entries or write local export files.

Mitigation: Review command arguments before execution and keep backups of operational log data when retention matters.

## Reference(s):

- [Andon ClawHub skill page](https://clawhub.ai/xueyetianya/skills/andon)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and command output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe generated local JSONL, CSV, or JSON files created by the shell script.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
