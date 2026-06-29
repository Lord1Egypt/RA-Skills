## Description: <br>
Generate polished changelogs and release notes from git history, PRs, and issues - auto-categorize features, fixes, and breaking changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release engineers use this skill to collect git history, classify changes, and generate reviewable changelogs, release notes, team announcements, or structured CI/CD output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated JSON or release text can include commit summaries, contributor names, references, and repository URL metadata from private repositories. <br>
Mitigation: Review generated JSON and release content before pasting it into chat, release tools, or public channels. <br>
Risk: GitHub or GitLab credentials may be exposed if embedded in remote URLs or supplied unintentionally during optional PR or issue enrichment. <br>
Mitigation: Avoid tokens in git remote URLs and provide platform credentials only when intentionally enabling enrichment. <br>
Risk: Automatically generated changelog entries can be misclassified, duplicated, or misleading. <br>
Mitigation: Run a human review pass for category accuracy, duplicate entries, breaking-change handling, links, dates, and release version before publication. <br>


## Reference(s): <br>
- [Changelog Weaver on ClawHub](https://clawhub.ai/harrylabsj/changelog-weaver) <br>
- [Conventional Commits](https://www.conventionalcommits.org/) <br>
- [Keep a Changelog](https://keepachangelog.com/) <br>
- [Conventional Commits Reference](references/conventional-commits.md) <br>
- [Output Format Specifications](references/output-formats.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown, plain text, and JSON files with optional shell commands and review guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated content should be reviewed before publishing, especially when based on private repository history or optional PR and issue enrichment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
