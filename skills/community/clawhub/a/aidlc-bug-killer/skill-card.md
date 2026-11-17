## Description:

AIDLC Bug Killer is a Chinese-language multi-agent workflow for discovering, fixing, tracking, and confirming software bugs through file-based bug reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sydpz](https://clawhub.ai/user/sydpz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to coordinate bug discovery, implementation, review, and status tracking across SubAgent, main-agent, and ReviewAgent roles. It is suited to projects that want persistent Markdown bug reports and changelog updates as the coordination record.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can create or move bug-report Markdown files and update a project changelog, which can leave project state misleading if changes are not reviewed.

Mitigation: Review generated bug reports, directory status moves, and changelog updates before merge or release.

Risk: Bug-fix guidance or proposed code changes may be incomplete or incorrect for the target project.

Mitigation: Review code diffs as normal engineering changes and run the relevant test suite before accepting the fix.

## Reference(s):

- [Bug report template](artifact/references/bug-template.md)
- [AIDLC Bug Killer ClawHub release page](https://clawhub.ai/sydpz/skills/aidlc-bug-killer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown bug reports, changelog entries, implementation notes, and optional code or test command suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses file-based status movement across pending, waiting_confirm, and confirmed bug-report directories.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
