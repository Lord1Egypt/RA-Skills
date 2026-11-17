## Description:

Multi-channel ABM automation that turns LinkedIn URLs into coordinated outbound campaigns. Scrapes profiles, enriches with Apollo (email + phone), gets mailing addresses via Skip Trace, then orchestrates email sequences, LinkedIn touches, and handwritten letters via Scribeless. The secret weapon for standing out in crowded inboxes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dru-ca](https://clawhub.ai/user/dru-ca)

### License/Terms of Use:


## Use Case:

Sales, growth, and revenue teams use this skill to turn LinkedIn prospect lists into coordinated outbound campaigns across email, LinkedIn, and handwritten letters. The workflow helps agents draft and run API-based enrichment, address lookup, campaign upload, and CSV handoff steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can collect and use sensitive personal contact data and home-address data for outbound campaigns.

Mitigation: Use it only for lawful, authorized business outreach and avoid personal emails, phone numbers, and home addresses unless there is a documented basis to process them.

Risk: Campaign execution can create privacy, consent, suppression-list, unsubscribe, and retention obligations.

Mitigation: Verify vendor terms, suppression lists, unsubscribe handling, data retention, and privacy obligations before running any campaign.

Risk: Skip Trace address matches may be inaccurate or stale.

Mitigation: Verify that Skip Trace state matches the LinkedIn location and skip or review records where the state does not match.

## Reference(s):

- [Enrichment Reference](artifact/references/enrichment.md)
- [Scribeless API Reference](artifact/references/scribeless-api.md)
- [ClawHub skill page](https://clawhub.ai/dru-ca/skills/abm-outbound)
- [Apify](https://apify.com)
- [Apollo](https://apollo.io)
- [Scribeless platform](https://platform.scribeless.co)
- [Scribeless documentation](https://docs.scribeless.co)
- [Instantly](https://instantly.ai)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with bash, Python, JSON, and CSV examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include API request examples, campaign timing guidance, and CSV fields for enriched prospect data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
