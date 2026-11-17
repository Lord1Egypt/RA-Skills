## Description:

Access bioRxiv preprint repository for biology preprints by category and date range, with paper metadata including titles, authors, DOIs, dates, and categories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aquaskyline](https://clawhub.ai/user/aquaskyline)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and research-support agents use this skill to retrieve public bioRxiv preprint metadata for selected biology collections and date ranges. It supports listing available subject collections, fetching recent or bounded-date papers, and returning results as text or JSON for downstream summarization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default or --days usage may fetch a broader date range than expected.

Mitigation: Use explicit --start and --end dates when precise recency or bounded retrieval is required.

## Reference(s):

- [bioRxiv API Documentation](references/api.md)
- [bioRxiv API](https://api.biorxiv.org)
- [ClawHub Skill Page](https://clawhub.ai/aquaskyline/skills/biorxiv-openclaw-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and optional JSON paper metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public bioRxiv API responses; no authentication or credential input is required.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
