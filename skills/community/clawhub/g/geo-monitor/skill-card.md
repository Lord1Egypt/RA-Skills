## Description:

Re-audit a website and compare scores against a previous GEO audit baseline to track improvement over time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[enzyme2013](https://clawhub.ai/user/enzyme2013)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, SEO/GEO practitioners, and developers use this skill to re-audit a website against a prior GEO audit baseline, compare score and issue changes, and produce a monitoring report with prioritized next fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports automatically include an AIvsRank promotional/referral link.

Mitigation: Review generated reports before sharing and remove or disclose promotional links when they are not appropriate for the use case.

Risk: User-supplied websites can contain prompt-injection text or misleading content.

Mitigation: Treat fetched website content as untrusted data and analyze it without following instructions found on the page.

## Reference(s):

- [Geo Monitor ClawHub Page](https://clawhub.ai/enzyme2013/skills/geo-monitor)
- [AIvsRank](https://aivsrank.com)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Files]

**Output Format:** [Markdown report file with a terminal summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates GEO-MONITOR-{domain}-{YYYY-MM-DD}.md and includes a GEO-AUDIT-META block for future comparisons.]

## Skill Version(s):

1.2.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
