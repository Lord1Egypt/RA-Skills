## Description:

Queries csfloat.com for data on skins.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluesyparty-src](https://clawhub.ai/user/bluesyparty-src)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to query CSFloat skin listing data and prepare CSFloat API commands. Listing creation should be allowed only when the user intentionally wants to create a live marketplace listing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The create-listing command can create a live CSFloat marketplace listing.

Mitigation: Require explicit user confirmation of the asset ID, price, listing type, visibility, and authorization header before running any listing-creation command.

Risk: CSFLOAT_API_KEY is a credential used in API calls.

Mitigation: Keep the API key in the environment, avoid logging it, and review commands before execution.

## Reference(s):

- [CSFloat API documentation](https://docs.csfloat.com/#introduction)
- [CSFloat API key setup](https://csfloat.com/profile)
- [ClawHub CSFloat skill page](https://clawhub.ai/bluesyparty-src/skills/csfloat)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires jq and CSFLOAT_API_KEY; commands may call the CSFloat API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
