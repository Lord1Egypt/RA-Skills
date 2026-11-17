## Description:

Rank upcoming trade shows by how many competitors in a provided company list match Lensmor exhibitor records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weilun88313](https://clawhub.ai/user/weilun88313)

### License/Terms of Use:

MIT-0

## Use Case:

External users and go-to-market teams use this skill to compare competitor show circuits, prioritize trade show budgets, and identify events where multiple named competitors appear in Lensmor exhibitor records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags an unverified personal namespace and mutable source checkout in the install path.

Mitigation: Verify that the @weilun88313 package is officially controlled by LensmorOfficial, and prefer a pinned reviewed version or commit with a checksum before installation.

Risk: Running the skill sends competitor names to Lensmor and may consume credits for non-empty successful searches.

Mitigation: Confirm the maximum first-page credit cost and obtain explicit user approval before the first live lookup.

Risk: Successful searches record API activity and asynchronously update the API-key owner's HubSpot last_search_date.

Mitigation: Disclose the HubSpot activity side effect before execution and proceed only after the user approves it.

Risk: Lensmor matches are database records and are not independently verified attendance confirmations.

Mitigation: Present results as matches in Lensmor exhibitor records and advise users to verify current event editions, dates, and exhibitor listings before budget decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/weilun88313/skills/competitor-show-tracker)
- [Lensmor API Documentation](https://api.lensmor.com/?utm_source=github&utm_medium=skill&utm_campaign=competitor-show-tracker)
- [Fictional Industrial Automation Example](examples/industrial-automation-show-circuit.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Guidance]

**Output Format:** [Markdown summary with ranked tables, event detail sections, insights, and follow-up suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LENSMOR_API_KEY; successful non-empty lookups can consume credits and update HubSpot last_search_date.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
