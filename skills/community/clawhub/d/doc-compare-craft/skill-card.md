## Description: <br>
Compares two document versions and generates interactive HTML-oriented difference views, including side-by-side, inline, unified, word-level, legal redline, summary, and structural comparison modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wwbwin](https://clawhub.ai/user/wwbwin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to compare two authorized document versions and produce readable difference views for contracts, technical plans, reports, standards, or scripts. It helps reviewers identify added, removed, modified, moved, or structurally changed content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Compared documents may be included in generated HTML output. <br>
Mitigation: Only compare documents the user is authorized to process, and handle generated HTML files as containing the underlying document content. <br>
Risk: Users may paste secrets, regulated personal data, or confidential contracts into the comparison workflow. <br>
Mitigation: Remove secrets and sensitive regulated data before use unless approval and handling controls are in place. <br>
Risk: The artifact's HTML templates are placeholders, so generated visual output may require review before operational use. <br>
Mitigation: Review the generated comparison output for completeness and accuracy before using it for legal, business, or release decisions. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/wwbwin/skills/doc-compare-craft) <br>
- [Publisher profile](https://clawhub.ai/user/wwbwin) <br>
- [Homepage listed in ClawHub metadata](https://github.com/wwbwin/clawhub-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown guidance and generated single-file HTML-oriented document comparison output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports seven comparison modes: side-by-side, inline, unified, word-level, legal-redline, summary-only, and structural.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
