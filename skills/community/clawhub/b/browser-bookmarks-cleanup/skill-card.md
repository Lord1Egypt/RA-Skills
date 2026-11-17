## Description:

Analyze, organize, and clean browser bookmarks on macOS using on-disk bookmark and history files. Detects duplicates, stale bookmarks, tracking parameters, and folder issues. All writes are opt-in with backup and rollback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[makkoncept](https://clawhub.ai/user/makkoncept)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to inspect local Chrome and Firefox bookmarks, identify duplicate, stale, weak, or poorly organized entries, and prepare conservative cleanup plans before making any changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive browser data, including local bookmark paths, URLs, history-derived visit signals, and possible account names or emails in discovery output.

Mitigation: Review outputs locally, avoid including discovery results in shared logs or transcripts, and redact profile or account details before sharing reports.

Risk: Cleanup plans can delete, move, rename, or update bookmarks if committed.

Mitigation: Review generated plans carefully, run dry-runs first, separately export or back up bookmarks, close the browser before writing, and use the generated backup file for rollback.

Risk: Duplicate, stale, or weak-name findings may be incomplete or misleading because they are based on local files and history availability.

Mitigation: Treat findings as review candidates, verify important bookmarks manually, and prefer conservative operations when approving a plan.

## Reference(s):

- [Cleanup Plan JSON Schema](references/plan-schema.md)
- [ClawHub skill page](https://clawhub.ai/makkoncept/skills/browser-bookmarks-cleanup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON analysis, plan, and result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only analysis by default; write operations require an explicit --write flag and produce a backup path when committed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
