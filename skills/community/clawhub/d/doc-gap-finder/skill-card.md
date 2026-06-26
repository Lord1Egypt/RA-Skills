## Description: <br>
Scans documentation directories, heading structure, and file distribution to find missing sections, duplicate content, and outdated areas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Documentation maintainers, knowledge base owners, developers, and release reviewers use this skill to audit documentation folders for structure gaps, repeated sections, stale areas, and prioritized follow-up work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated report can include local file names, headings, and documentation structure from private folders. <br>
Mitigation: Use the skill only on documentation folders or directories the user is authorized to inspect, and review or redact the report before sharing. <br>
Risk: Scanning an entire private repository can expose more context than intended. <br>
Mitigation: Point the skill at the intended documentation directory or file list rather than a broader repository unless the wider audit is deliberate. <br>
Risk: Gap and duplicate findings are audit suggestions and may be incomplete or context-dependent. <br>
Mitigation: Treat results as a review draft and confirm priorities before adding, deleting, publishing, or reorganizing documentation. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/52YuanChangXing/doc-gap-finder) <br>
- [Publisher profile](https://clawhub.ai/user/52YuanChangXing) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report or JSON report with directory overview, suspected gaps, duplicates, suggested additions or removals, priorities, and confirmation items.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only local documentation audit; script output may be written to a user-selected report file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
