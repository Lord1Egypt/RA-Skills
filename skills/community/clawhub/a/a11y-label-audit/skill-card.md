## Description: <br>
扫描 React、TSX 和 HTML 项目中的无障碍标签问题，生成审查报告，并可自动修复缺失或错误的 aria-label、role、alt、label、dialog 和 live-region 标注。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ityhg](https://clawhub.ai/user/ityhg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and accessibility reviewers use this skill to audit React, Next.js, TSX, HTML, Tauri, browser extension, and WebView-based front-end projects for WCAG-oriented labeling issues and cross-platform assistive-technology compatibility gaps. It can produce a file-by-file report and apply code edits for common fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may automatically edit source files across a broad default scope. <br>
Mitigation: Use it on a branch, specify exact files or folders, request report-only mode first, and review diffs plus lint or test results before accepting fixes. <br>
Risk: Accessibility labels and compatibility fixes may be inferred from context and can be inaccurate for the product's actual user experience. <br>
Mitigation: Review generated labels with product context, validate important flows with assistive technologies, and check target WebView or browser environments before release. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ityhg/a11y-label-audit) <br>
- [Reference guide](artifact/reference.md) <br>
- [Fix examples](artifact/examples.md) <br>
- [Usage guide](artifact/USAGE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown audit report with file and line tables, suggested fixes, and optional source-code edits] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify project files when automatic fixes are applied; review diffs and run lint or tests before accepting changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, clawhub.json, CHANGELOG released 2026-04-10) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
