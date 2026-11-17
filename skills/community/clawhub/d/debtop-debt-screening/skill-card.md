## Description:

Screens public debt transfer and disposal notices by industry, region, and amount within a scanned window, then groups matches by seller (creditor).

This skill is ready for commercial/non-commercial use.

## Publisher:

[ninjaliang](https://clawhub.ai/user/ninjaliang)

### License/Terms of Use:

MIT-0

## Use Case:

External debt-asset analysts and researchers use the skill to shortlist public debt notices and compare sellers, principal amounts, and debtors within the scanned results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Guest fallback creates and caches a short-lived service token and sends HTTPS requests to agent.debtop.com.

Mitigation: Prefer an existing MCP/OAuth connection; protect the cached token and do not run helper scripts against an untrusted endpoint.

Risk: Partial scans or outdated notices can make debt holdings appear more complete or current than the evidence supports.

Mitigation: Disclose scan coverage and date range, distinguish the named seller from the current holder, and avoid credit or investment conclusions.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/ninjaliang/skills/debtop-debt-screening)
- [Tool parameters and screening limits](artifact/references/tools-and-fields.md)
- [Guest access and authentication](artifact/references/guest-access.md)
- [Screening report template](artifact/templates/debt-screening-report.md)

## Skill Output:

**Output Type(s):** [Markdown, Text, Guidance]

**Output Format:** [Markdown report with seller summaries, notice tables, and source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports scanned count, coverage, and date window; amount and region filters apply only to scanned notices.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
