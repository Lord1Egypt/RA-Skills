## Description:

Dream actively maintains OpenClaw MEMORY.md by distilling daily memory files, compressing stale context, preserving archived memories in a ledger, detecting re-emergence, and indexing selected content for Obsidian.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teman2050](https://clawhub.ai/user/teman2050)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use Dream to keep long-term agent memory concise, searchable, and current while moving older or completed memories into a permanent local archive.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can permanently retain personal memory in ledger and re-emergence records.

Mitigation: Use it only with an approved local vault path, review what is archived, and add a full-erasure path for ledger and removed-entry records before handling sensitive data.

Risk: Automatic MEMORY.md rewrites and helper-script file operations can affect local agent context.

Mitigation: Restrict atomic writes to approved paths and review scheduled or automatic changes before enabling unattended use.

Risk: Forget/delete behavior clears active memory while leaving the permanent archive intact.

Mitigation: Require confirmation for forget/delete actions and clearly distinguish active-memory removal from archive erasure.

Risk: The security review reports unsafe file-write and code-injection behavior.

Mitigation: Address the reported helper-script issues, including Python timestamp handling, before deployment in a shared or production environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/teman2050/skills/dream-memory-manager)
- [Project homepage](https://github.com/teman2050/dream-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and local file updates performed by the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include memory summaries, status text, search results, ledger records, and Obsidian index entries.]

## Skill Version(s):

0.2.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
