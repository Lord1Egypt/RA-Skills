## Description:

Etalon Tech Scan helps agents use the ETALON CLI to detect website technologies from HTTP headers, cookies, scripts, meta tags, HTML patterns, and DNS records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rednix](https://clawhub.ai/user/rednix)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and analysts use this skill to confirm a website's technology stack, compare competitors or vendors, and summarize detected frameworks, hosting, analytics, payments, CMS, CDN, and security tools with confidence signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Website scans may be run against targets the user did not intend or in bulk.

Mitigation: Ask for explicit confirmation before each scan target and handle batch scans carefully.

Risk: Installing or running an unpinned local CLI can execute code outside the agent workspace.

Mitigation: Install only a trusted, preferably pinned ETALON CLI release and avoid elevated privileges.

Risk: Database credentials may be exposed if passed directly on the command line.

Mitigation: Use a protected environment variable or secret store for database connection strings when supported.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rednix/skills/etalon-techscan)
- [Publisher profile](https://clawhub.ai/user/rednix)
- [ETALON homepage](https://etalon.nma.vc)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summaries with inline shell commands and grouped scan results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports detected technologies with confidence scores and detection methods; requires a local etalon CLI installation.]

## Skill Version(s):

0.9.5 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
