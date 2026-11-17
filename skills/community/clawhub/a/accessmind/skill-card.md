## Description:

AccessMind helps agents perform WCAG 2.2, WCAG 2.1, and EN 301 549 accessibility audits with browser-based checks, keyboard navigation testing, ACT rules, and professional reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sarperarikan](https://clawhub.ai/user/sarperarikan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, accessibility specialists, and QA teams use this skill to audit web pages for accessibility barriers, map findings to WCAG and ACT checks, and generate remediation-oriented reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports broad browser permissions and audit tooling that may expose page content.

Mitigation: Install only in a disposable browser profile or isolated test environment, and audit only sites you are authorized to test.

Risk: Screenshots or page data may be sent to local services on fixed ports.

Mitigation: Avoid banking, admin, intranet, production, or sensitive authenticated pages unless the runtime environment and local services are reviewed and controlled.

Risk: Some tooling may weaken browser isolation or execute mutable third-party tooling.

Mitigation: Review permissions, dependency pinning, sandbox flags, and generated HTML rendering before use in sensitive environments.

## Reference(s):

- [AccessMind ClawHub skill page](https://clawhub.ai/sarperarikan/skills/accessmind)
- [WCAG-EM](https://www.w3.org/TR/WCAG-EM/)
- [ACT Rules](https://www.w3.org/WAI/standards-guidelines/act/)
- [WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/)
- [Axe-core Rules](https://dequeuniversity.com/rules/axe/4.10/)
- [ARIA Guide](references/aria-guide.md)
- [Browser Tool Workflow](references/browser-tool-workflow.md)
- [WCAG 2.2 Criteria](references/wcag-2.2-criteria.md)
- [Common Issues](references/common-issues.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples, JSON result structures, and HTML report templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include accessibility scores, WCAG and ACT mappings, issue lists, and remediation guidance.]

## Skill Version(s):

6.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
