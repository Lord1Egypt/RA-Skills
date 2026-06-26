## Description: <br>
Accessibility Check helps agents review and improve frontend accessibility across semantic structure, keyboard support, focus management, ARIA, screen reader behavior, WCAG 2.2, touch accessibility, and assistive-technology regressions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bovinphang](https://clawhub.ai/user/bovinphang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Frontend developers and reviewers use this skill to audit UI code and interaction flows for WCAG 2.2 AA accessibility issues, then produce a prioritized Markdown report with concrete remediation suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Accessibility guidance or proposed code changes may be incomplete or incorrect for a specific product flow. <br>
Mitigation: Review findings and any proposed changes before applying them, then verify key flows with keyboard and assistive-technology checks. <br>
Risk: The skill may inspect UI or source files and write a local report in the workspace. <br>
Mitigation: Run it only in the intended workspace and review the generated report before sharing or acting on it. <br>


## Reference(s): <br>
- [Report Template](references/report-template.md) <br>
- [Screen Reader Testing](references/screen-reader-testing.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/bovinphang/fec-accessibility-check) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown accessibility review report with prioritized findings and remediation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Expected report path: reports/accessibility-review-YYYY-MM-DD-HHmmss.md] <br>

## Skill Version(s): <br>
2.5.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
