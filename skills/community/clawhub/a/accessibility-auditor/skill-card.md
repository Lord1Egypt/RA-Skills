## Description: <br>
Audits web accessibility against WCAG 2.1/2.2, assistive technology, keyboard navigation, color contrast, and inclusive design practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mtsatryan](https://clawhub.ai/user/mtsatryan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, designers, and accessibility reviewers use this skill to plan and perform web accessibility audits, generate WCAG checklists, write test automation, and document remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The color-contrast example uses a placeholder calculation and may miss real contrast failures if copied directly. <br>
Mitigation: Replace it with a vetted WCAG-compliant contrast library or algorithm before using it in audits or CI gates. <br>
Risk: CI workflow examples may publish reports or post pull request comments when adapted into a repository. <br>
Mitigation: Review any adopted workflow permissions, uploads, and comment-posting steps before enabling them in a real project. <br>


## Reference(s): <br>
- [Accessibility Auditor examples](references/examples.md) <br>
- [ClawHub skill page](https://clawhub.ai/mtsatryan/accessibility-auditor) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with checklists, remediation guidance, and code or configuration blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Examples include accessibility test scaffolds, CI workflow snippets, audit checklists, and reporting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
