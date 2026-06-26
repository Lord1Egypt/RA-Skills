## Description: <br>
AI-powered accessibility checker that helps detect WCAG issues, suggest ARIA labels, test keyboard navigation, and report accessibility findings for web UI files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[supermario11](https://clawhub.ai/user/supermario11) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and accessibility reviewers use this skill to scan React, TypeScript, and HTML UI files for common accessibility issues and receive human-reviewable repair guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Auto-fix examples and repair suggestions may introduce incorrect or incomplete accessibility changes if applied without review. <br>
Mitigation: Review proposed diffs, confirm behavior with accessibility checks, and run the project test suite before committing changes. <br>
Risk: The included checker reads local project files during scans. <br>
Mitigation: Point scans at specific source folders and avoid unnecessary sensitive or generated directories. <br>


## Reference(s): <br>
- [WCAG 2.1 Quick Reference](https://www.w3.org/WAI/WCAG21/quickref/) <br>
- [ClawHub Skill Page](https://clawhub.ai/supermario11/cuihua-a11y-checker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown accessibility reports with issue summaries, fix suggestions, code snippets, shell commands, and JSON configuration examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js for the included local checker script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
