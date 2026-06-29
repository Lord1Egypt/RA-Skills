## Description: <br>
drawiodo helps agents turn natural-language requests into draw.io diagrams such as architecture diagrams, flowcharts, UML diagrams, ER diagrams, sequence diagrams, mind maps, and network topology diagrams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ldxs001](https://clawhub.ai/user/ldxs001) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, designers, architects, and technical writers use this skill to create and iteratively update draw.io diagrams from natural-language requirements, structured diagram specs, or requested edits to existing diagrams. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and update .drawio files, maintain local version history, and automatically open the draw.io desktop app. <br>
Mitigation: Review output paths before use and disable auto-preview in shared, automated, or headless environments. <br>
Risk: The skill can prune older saved versions during version management. <br>
Mitigation: Keep separate backups or adjust the version-retention workflow when older diagram history must be preserved. <br>


## Reference(s): <br>
- [API Reference](references/api_reference.md) <br>
- [User Guide](references/guide.md) <br>
- [Hooks and Workflow Safeguards](references/hooks.md) <br>
- [Layout Rules](references/layout_rules.md) <br>
- [Known Issues](references/known_issues.md) <br>
- [Test Report](references/test-report.md) <br>
- [Changelog](references/changelog.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [draw.io .drawio files with concise Markdown status and confirmation text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates workspace-local .drawio files, maintains local version history, and may open the draw.io desktop app for preview.] <br>

## Skill Version(s): <br>
2.6.1 (source: SKILL.md frontmatter, _meta.json, changelog, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
