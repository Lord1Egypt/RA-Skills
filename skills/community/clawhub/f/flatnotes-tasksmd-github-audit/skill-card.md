## Description:

Thoroughly audit Tasks.md + Flatnotes for drift and accuracy; use GitHub (gh CLI) as source of truth to detect stale notes/cards and missing links. Produces a report and an optional fix plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[branexp](https://clawhub.ai/user/branexp)

### License/Terms of Use:


## Use Case:

Developers and workspace maintainers use this skill to audit Tasks.md board hygiene, Flatnotes project completeness, and GitHub pull request reconciliation before deciding whether to update notes or task cards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads configured Tasks.md and Flatnotes directories and may use an authenticated gh CLI session to query GitHub.

Mitigation: Install only when those local data sources and GitHub access are appropriate, and review the generated report before asking an agent to apply fixes.

Risk: Applying proposed fixes could alter task or note content.

Mitigation: Use report-only mode by default; require an explicit request before applying fixes and ask first for renames or deletion of content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/branexp/skills/flatnotes-tasksmd-github-audit)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown report and JSON report, with optional fix-plan guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes audit reports under tmp/ when requested; GitHub checks are skipped if gh is unauthenticated.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
