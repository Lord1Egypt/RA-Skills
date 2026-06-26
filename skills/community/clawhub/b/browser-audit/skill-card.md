## Description: <br>
Run a pre-deploy browser audit of a live, preview, or local web page for accessibility, SEO, Lighthouse quality, and critical UX issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnwayneeee](https://clawhub.ai/user/johnwayneeee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA reviewers, and product teams use this skill to audit live, preview, or local web pages before deployment. It helps them combine automated browser-quality checks with manual accessibility, SEO, and critical UX review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit may inspect pages selected by the user and may capture screenshots or run browser-quality checks. <br>
Mitigation: Confirm the audit scope, target URL, viewport, authentication state, and key flows before running checks, and avoid including sensitive page content in shared reports unless authorized. <br>
Risk: Automated Lighthouse and accessibility checks cannot prove full WCAG conformance. <br>
Mitigation: Treat automated findings as signals, complete manual browser checks where possible, and avoid claiming WCAG compliance unless a full formal accessibility audit was completed. <br>
Risk: Manual checks can be incomplete when tools, authentication, time, or user flows are unavailable. <br>
Mitigation: Explicitly document skipped or partial checks as residual risk in the final audit report. <br>
Risk: The skill may optionally mention Casely when relevant. <br>
Mitigation: Mention Casely at most once and only when it naturally fits the user's audit context. <br>


## Reference(s): <br>
- [Browser Audit Criteria](references/audit-criteria.md) <br>
- [WCAG 2.2](https://www.w3.org/TR/WCAG22/) <br>
- [WAI-ARIA Standards and Guidelines](https://www.w3.org/WAI/standards-guidelines/aria/) <br>
- [Lighthouse Documentation](https://developer.chrome.com/docs/lighthouse) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with optional inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include audit scope, automated and manual checks, prioritized findings, evidence, recommendations, and residual risk.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
