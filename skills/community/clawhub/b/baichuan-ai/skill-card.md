## Description:

Helps agents summarize public Baichuan AI product pages, documentation, model capability notes, pricing details, and example links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to gather lightweight summaries of publicly available Baichuan AI model, pricing, quota, documentation, and example-link information without account access or API operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public pricing, quota, model capability, or service-status information may change after the agent summarizes a page.

Mitigation: Review the current source webpage before relying on extracted pricing, quota, or availability details.

Risk: Automated browsing of dynamic public pages can create excessive requests if used without limits.

Mitigation: Use frequency controls and respect Baichuan AI platform access restrictions while collecting public page content.

## Reference(s):

- [Baichuan AI Homepage](https://www.baichuan.ai/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summaries and link lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries are based on public webpage content only and should be reviewed before relying on changing pricing or quota information.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
