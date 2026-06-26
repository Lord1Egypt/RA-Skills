## Description: <br>
Analyze, organize, and clean browser bookmarks on macOS using on-disk bookmark and history files. Detects duplicates, stale bookmarks, tracking parameters, and folder issues. All writes are opt-in with backup and rollback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[makkoncept](https://clawhub.ai/user/makkoncept) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and end users use this skill to inspect local Chrome and Firefox bookmark data, identify cleanup candidates, preview a conservative cleanup plan, and apply approved changes with backup and rollback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local browser bookmarks and history, which can contain private URLs, account labels, and browsing patterns. <br>
Mitigation: Keep analysis output and plan files private, and install only when local bookmark and history inspection is acceptable. <br>
Risk: Approved cleanup plans can delete, move, rename, or update bookmarks. <br>
Mitigation: Run a dry-run first, review every planned operation, require explicit approval before writes, close the browser before using write mode, and retain the generated backup for rollback. <br>
Risk: Cleanup recommendations may misclassify bookmarks as duplicates, stale, weakly named, or safe to update. <br>
Mitigation: Treat findings as review prompts, not automatic decisions, and apply only operations the user has confirmed. <br>


## Reference(s): <br>
- [Cleanup Plan JSON Schema](references/plan-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON analysis or cleanup plan files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local analysis reports, plan previews, dry-run results, and opt-in bookmark file updates with backup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
