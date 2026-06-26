## Description: <br>
AI辅助无障碍合规守护者，可自动化检测网页和移动端 H5 的无障碍问题，生成修复建议并出具合规报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA teams, accessibility reviewers, and compliance teams use this skill to scan web or H5 experiences against WCAG-oriented checks and produce issue lists, repair guidance, and shareable compliance report cards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may render pages, execute JavaScript, capture screenshots, and extract DOM content for analysis. <br>
Mitigation: Use it only on authorized public pages, test pages, or redacted HTML, and confirm authorization before scanning login-protected, internal, regulated, or customer-data pages. <br>
Risk: Accessibility findings are generated from screenshots, DOM structure, and AI analysis, so they may not fully replace manual assistive-technology testing. <br>
Mitigation: Review generated findings before treating them as compliance evidence, and validate important flows with human review and relevant screen-reader or keyboard testing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zlszhonglongshen/ai-a11y-guardian) <br>
- [Publisher Profile](https://clawhub.ai/user/zlszhonglongshen) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Files, Guidance] <br>
**Output Format:** [Markdown issue reports with structured findings, repair snippets, and generated report card files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include screenshots, DOM-derived findings, severity ratings, WCAG references, accessibility scores, and visual compliance cards.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
