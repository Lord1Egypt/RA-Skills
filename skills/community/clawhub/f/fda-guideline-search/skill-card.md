## Description:

Search FDA industry guidelines by therapeutic area or topic.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search FDA guidance-like records by therapeutic area, document type, year, and optional search terms. It should be treated as a demonstration until its guidance retrieval and verification behavior is replaced with authoritative FDA or ICH document handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search results may contain fabricated FDA-looking guidance records.

Mitigation: Do not use results for regulatory, clinical, legal, or submission decisions until the skill retrieves and verifies authoritative FDA or ICH documents and clearly labels any mock mode.

Risk: The output option can write files broadly.

Mitigation: Restrict output paths to a safe workspace directory before running the skill with file output enabled.

## Reference(s):

- [FDA Search Strategy](references/search-strategy.md)
- [Therapeutic Area Mappings](references/area-mappings.json)
- [FDA API Documentation Notes](references/fda-api-notes.md)
- [FDA Guidance Search](https://www.fda.gov/regulatory-information/search-fda-guidance-documents)
- [FDA Drug Guidance](https://www.fda.gov/drugs/guidance-compliance-regulatory-information/guidances-drugs)
- [FDA Biologics Guidance](https://www.fda.gov/vaccines-blood-biologics/guidance-compliance-regulatory-information-biologics/guidances-biologics)
- [openFDA APIs](https://open.fda.gov/apis/)
- [FDA Data Catalog](https://catalog.data.gov/organization/fda-gov)
- [ICH Guidelines Database](https://database.ich.org/home)
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/fda-guideline-search)

## Skill Output:

**Output Type(s):** [text, json, shell commands, files, guidance]

**Output Format:** [Structured JSON search results with optional local PDF file paths and command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports therapeutic area, document type, year, download, full-text search, result limit, list-areas, and output-file options.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
