## Description: <br>
Build and maintain a local favorites catalog from installed repositories, apps, skills, extensions, and hooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luw2007](https://clawhub.ai/user/luw2007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and power users use this skill to scan local repositories, installed apps, skills, extensions, and hooks into a file-backed favorites catalog, then generate Markdown digests and notification copy for notable changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner builds a persistent local inventory of repositories, applications, skills, extensions, and hooks. <br>
Mitigation: Review the generated favorites/ entries, snapshots, and reports before sharing or committing them. <br>
Risk: Running the scanner may contact GitHub or vendor/source URLs discovered from local metadata. <br>
Mitigation: Run only in an environment where outbound enrichment is acceptable, or review and modify the enrichment behavior before execution. <br>
Risk: Generated entries that are no longer observed may be pruned during refresh. <br>
Mitigation: Keep backups or version control for favorites/ when preserving historical catalog entries matters. <br>


## Reference(s): <br>
- [Naming And Data Model](references/naming-and-model.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/luw2007/favorites-curator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands] <br>
**Output Format:** [Markdown reports, JSON snapshots, Markdown entry files, and short text notification lines] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates a persistent local favorites catalog under favorites/.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
