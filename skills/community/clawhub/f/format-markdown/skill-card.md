## Description: <br>
Summarize and format Markdown files, then apply MkDocs/Material-compatible structural spacing fixes for math, list, and table blocks; outputs to {filename}_formatted.md by default. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smilingwayne](https://clawhub.ai/user/smilingwayne) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and documentation maintainers use this skill to format Markdown documents, generate title and summary/frontmatter suggestions, and apply MkDocs Material spacing fixes while preserving source meaning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and rewrites Markdown files selected by the user. <br>
Mitigation: Use the default formatted-copy workflow for important documents and review outputs before replacing originals. <br>
Risk: Structural-fixes-only mode and backup-disabling options can modify files directly. <br>
Mitigation: Use in-place modes only when direct edits are intended, and keep backups enabled unless another recovery path exists. <br>
Risk: Generated analysis files and backups may contain sensitive source-document content. <br>
Mitigation: Review generated analysis and backup files before sharing, committing, or retaining them. <br>
Risk: The structural formatting script requires local npm dependencies. <br>
Mitigation: Install dependencies from the provided lockfile with npm ci before running the script. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/smilingwayne/format-markdown) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files, analysis reports, and terminal command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a formatted copy by default; structural-fixes-only mode can edit in place and may create timestamped backups unless backup creation is disabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
