## Description:

SN Data by Shikshan Nivesh: Form 13F fund holdings, with what each fund opened, added, trimmed and exited each quarter, plus 13D and 13G large holders. Use when a question asks what a fund owns or who owns a US company.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shikshannivesh](https://clawhub.ai/user/shikshannivesh)

### License/Terms of Use:

MIT-0

## Use Case:

Financial researchers and developers can use this skill to look up reported US fund holdings, quarterly position changes, and 13D/13G large holders. It helps answer who owns a company or what a fund reported, with filing-period context and source citations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The SN_KEY API credential could be exposed in shared output or files.

Mitigation: Keep the key in an environment variable, and never print it or put it in a file you share.

Risk: Reported holdings could be presented without filing context or as investment advice.

Mitigation: Include the fiscal period and source filing for figures, and present the data as information rather than a buy or sell call.

Risk: Using the data at work, in a product, or for bulk AI training may require a separate data license.

Mitigation: Check the data terms and obtain a license when required: https://shikshannivesh.com/data/licence

## Reference(s):

- [SN Data developer reference](https://shikshannivesh.com/data/developers)
- [AI client setup](https://shikshannivesh.com/data/ai)
- [REST API OpenAPI specification](https://shikshannivesh.com/api/v1/openapi.json)
- [13F fund-holder example](https://shikshannivesh.com/api/v1/companies/AAPL/fund-holders)
- [13F Fund Holdings on ClawHub](https://clawhub.ai/shikshannivesh/skills/13f-fund-holdings)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Text]

**Output Format:** [Text or Markdown summaries with fiscal periods and filing citations; includes inline bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Quote figures as returned, link the source filing, and credit the data to Shikshan Nivesh.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
