## Description:

Enriches leads by finding contact emails from websites, Instagram, Hunter.io, and email patterns, then formats deduplicated batches for Notion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[visualdeptcreative](https://clawhub.ai/user/visualdeptcreative)

### License/Terms of Use:


## Use Case:

Developers, operators, and sales workflow users can use this skill to enrich lead records with prioritized contact emails, confidence labels, and Notion-ready JSON batches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lead domains are sent to Hunter.io using the user's API key.

Mitigation: Confirm this third-party lookup is acceptable for the lead data before running enrichment, and protect the Hunter.io API key.

Risk: Enriched contact emails are stored in a local JSON batch file.

Mitigation: Keep the output file in a protected workspace and delete it when it is no longer needed.

Risk: A Notion sync could write enriched leads to the wrong database.

Mitigation: Verify the intended Notion lead database before syncing deduplicated output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/visualdeptcreative/skills/data-enricher)
- [Hunter.io domain search API](https://api.hunter.io/v2/domain-search)

## Skill Output:

**Output Type(s):** [guidance, JSON, files]

**Output Format:** [JSON lead records with concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Batches up to 10 leads and saves enriched output to a local leads-enriched-YYYY-MM-DD.json file.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
