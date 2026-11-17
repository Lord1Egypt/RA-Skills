## Description:

AI-powered accessibility checker that helps detect WCAG issues, generate ARIA label suggestions, test keyboard navigation, and review accessibility concerns in application code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[supermario11](https://clawhub.ai/user/supermario11)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to audit frontend components and pages for common accessibility issues, then receive reports and practical remediation suggestions for WCAG, ARIA, keyboard navigation, form labeling, headings, and related checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may overstate its WCAG coverage or miss accessibility issues.

Mitigation: Use its report as a preliminary review and pair findings with manual accessibility review, assistive technology testing, or established audit tooling.

Risk: Local scanning can inspect more files than intended when pointed at a broad directory.

Mitigation: Run it only against a tightly scoped project path and confirm the target directory before execution.

Risk: Suggested accessibility fixes can be incomplete or change application behavior.

Mitigation: Inspect diffs, run tests, and verify the user experience before accepting proposed changes.

## Reference(s):

- [WCAG 2.1 Quick Reference](https://www.w3.org/WAI/WCAG21/quickref/)
- [ClawHub skill page](https://clawhub.ai/supermario11/skills/cuihua-a11y-checker)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown accessibility reports with remediation guidance, code snippets, shell command examples, and configuration examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node for the bundled local checker.]

## Skill Version(s):

1.0.0 (source: skill metadata and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
