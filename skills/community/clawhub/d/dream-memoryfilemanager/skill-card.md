## Description:

Dream actively maintains OpenClaw's MEMORY.md by distilling daily memory files, compressing stale context into a permanent ledger, and indexing selected content for Obsidian.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teman2050](https://clawhub.ai/user/teman2050)

### License/Terms of Use:

MIT

## Use Case:

External OpenClaw users and developers use Dream to keep active memory concise while preserving older or completed memories in a searchable archive. It supports scheduled or manual memory distillation, memory status checks, archive search, and Obsidian content indexing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill preserves personal memory in a permanent ledger, including entries that dream forget does not erase.

Mitigation: Use it only when permanent local retention is acceptable; avoid storing sensitive data and review or remove ledger files manually when retention is not desired.

Risk: Scheduled distillation can silently update memory and archive files.

Mitigation: Enable scheduled SOUL.md behavior only after review; use manual triggers until the memory update behavior is trusted.

Risk: Installation guidance relies on cloning mutable remote code and running a local shell script.

Mitigation: Pin the repository to a reviewed commit, inspect dream-tools.sh before execution, and make it executable only after review.

Risk: Security evidence identifies unsafe local file-write and Python-state handling issues before sensitive use.

Mitigation: Fix or review those issues before trusting the skill with sensitive memory data.

## Reference(s):

- [Dream README](artifact/readme.md)
- [Dream metadata homepage](https://github.com/teman2050/dream-skill)
- [ClawHub skill page](https://clawhub.ai/teman2050/skills/dream-memoryfilemanager)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance, shell commands, and local file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update MEMORY.md, Dream vault metadata, ledger files, and Obsidian index files when invoked.]

## Skill Version(s):

0.2.1 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
