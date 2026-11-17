## Description:

Competitive ad intelligence skill for fetching, analyzing, and reporting on competitor ads across Meta, Google Ads Transparency Center, and LinkedIn Ad Library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abhishekj9621](https://clawhub.ai/user/abhishekj9621)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, ecommerce operators, and developers use this skill to research competitor advertising across public Meta, Google, and LinkedIn ad libraries, then summarize campaign patterns and normalized ad records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses public ad-library scraping and third-party API providers, which may be subject to platform terms, provider policies, and service changes.

Mitigation: Confirm platform terms and organizational policy before use, prefer official APIs where available, and run scraping workflows only in approved contexts.

Risk: Competitor names, domains, page IDs, and API credentials may be sent to named external providers during deeper collection workflows.

Mitigation: Share only approved inputs with external providers, keep API credentials scoped to the task, and avoid running the workflow in environments that contain unrelated secrets.

Risk: Unpinned dependencies and browser-based scraping can introduce supply-chain or runtime exposure.

Mitigation: Pin dependencies before installation and run browser scraping in a restricted environment.

## Reference(s):

- [Meta (Facebook / Instagram) Ad Intelligence](artifact/references/meta.md)
- [Google Ads Transparency Center - Ad Intelligence](artifact/references/google.md)
- [LinkedIn Ad Library - Ad Intelligence](artifact/references/linkedin.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown summary report with normalized JSON ad records and optional code or shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include data limitations, phase recommendations, and next-step guidance for API keys or provider choices.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
