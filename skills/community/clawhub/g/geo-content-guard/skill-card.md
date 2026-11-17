## Description:

Detects GEO/SEO soft articles, synthetic promotion pages, abnormal brand mention density, and low-credibility sources in external web content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2404589803](https://clawhub.ai/user/2404589803)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to scan external web pages, local content, or raw text before summarizing or recommending from those sources. It helps flag promotional influence patterns, high brand density, recommendation steering, and low-credibility domains so downstream agents can cross-check or avoid suspect content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URL scans can fetch arbitrary URLs, including private or internal locations reachable from the runtime environment.

Mitigation: Run URL scans in an environment that cannot reach sensitive internal services, or add URL and endpoint allowlists before deployment.

Risk: Optional AI review can send scanned excerpts and metadata to ZenMux or another configured endpoint.

Mitigation: Avoid using --with-ai on confidential local files or private/internal URLs unless the endpoint is approved for that data.

## Reference(s):

- [GEO Content Guard ClawHub Skill Page](https://clawhub.ai/2404589803/skills/geo-content-guard)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain-text scan summaries and JSON scan reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces PASS, WARN, or BLOCK recommendations with a risk score, signal evidence, metrics, and optional AI-review summary.]

## Skill Version(s):

0.1.0 (source: server release metadata, SKILL.md frontmatter, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
