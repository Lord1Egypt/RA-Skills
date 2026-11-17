## Description:

Monitor public OpenClaw ecosystem sources with source-quality checks, metadata-only collection, and trust-first reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marsloting](https://clawhub.ai/user/marsloting)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to monitor public OpenClaw ecosystem freshness, package metadata, documentation availability, and trust signals. It produces local source-linked summaries for human review before any public contribution or release action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unauthenticated requests to public services may encounter rate limits, access denials, robots changes, or platform warnings.

Mitigation: Use official APIs where available and pause the affected source on HTTP 403, HTTP 429, robots disallow, DMCA or abuse notices, platform warnings, or authentication requests.

Risk: Generated reports may include unsanitized public metadata or commentary that is not fully verified from the snapshot.

Mitigation: Treat reports as drafts for human review and keep canonical source links, timestamps, and request status fields with every signal.

Risk: Ecosystem monitoring could accidentally mirror source content or expose sensitive local data if expanded carelessly.

Mitigation: Store only normalized metadata, hashes, timestamps, short summaries, and source URLs; do not read .env files, persist request headers, store cookies, or copy full issue bodies, README files, docs pages, or package tarballs.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/marsloting/skills/claw-ecosystem-monitor)
- [GitHub REST API Documentation](https://docs.github.com/en/rest)
- [OpenClaw Skill Creation Docs](https://docs.openclaw.ai/tools/creating-skills)
- [OpenClaw ClawHub Docs](https://docs.openclaw.ai/tools/clawhub)
- [OpenClaw Docs Sitemap](https://docs.openclaw.ai/sitemap.xml)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON snapshots and Markdown reports with source links, timestamps, status fields, warnings, and short summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local outputs are metadata-only and intended for human review before publication or contribution.]

## Skill Version(s):

0.1.0 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
