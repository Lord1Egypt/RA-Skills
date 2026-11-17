## Description:

Automates visual, interaction, performance, and WCAG AA checks for web interfaces in a browser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djc00p](https://clawhub.ai/user/djc00p)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA teams use this skill to check web pages and user journeys for browser errors, visual regressions, and accessibility issues. Test only sites they own or are authorized to assess, using staging environments and dedicated test data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser interactions can submit forms, create accounts, log in, or complete checkout, changing data on the target site.

Mitigation: Test only on owned or authorized staging or sandbox sites with dedicated test accounts and sandbox payment data; get explicit approval for each state-changing flow.

Risk: Screenshots or QA reports may expose sensitive information.

Mitigation: Review screenshots and reports and remove sensitive information before sharing them.

## Reference(s):

- [Browser automation tools](references/tools.md)
- [WCAG AA accessibility checklist](references/wcag.md)
- [Browser QA on ClawHub](https://clawhub.ai/djc00p/skills/browser-qa)

## Skill Output:

**Output Type(s):** [Markdown, Screenshots, Accessibility findings]

**Output Format:** [Markdown QA report with browser screenshots and categorized findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include console and network checks, Core Web Vitals, interaction results, visual comparisons, and WCAG AA findings.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
