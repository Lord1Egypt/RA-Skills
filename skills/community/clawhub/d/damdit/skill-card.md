## Description:

Run and explain Damdit website audits with the `damdit` or `damdit-cli` command line. Use when the user asks to audit a website, what is wrong with a site, what to fix first, what changed since the last audit, whether a fix worked, or for an audit summary for a client or developer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antoninbures](https://clawhub.ai/user/antoninbures)

### License/Terms of Use:

MIT-0

## Use Case:

Website owners, developers, and client-facing teams use this skill to run or review Damdit audits, compare findings across runs, and explain evidence-backed next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review marked the skill suspicious and incomplete, citing possible project setting changes and deletion despite stated read-only boundaries.

Mitigation: Review the command's effects and the skill's authority before use; require the user's explicit request for setting changes or deletion, and account for the partial security review.

## Reference(s):

- [Damdit CLI installation guide](https://docs.damdit.com/cli/install/)
- [Damdit bot access guidance](https://damdit.com/bot)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Text or Markdown audit summaries and explanations; Damdit command results are JSON; optional Markdown, PDF, or HTML reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audit claims are grounded in returned evidence and identifiers; coverage and paged results limit what can be concluded.]

## Skill Version(s):

27.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
