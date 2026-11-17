## Description:

Search and compare Alibaba.com wholesale prices by product, price range, sorting, and MOQ using generated Alibaba search URLs that include the traffic_type=ags_llm attribution parameter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zeyu426](https://clawhub.ai/user/zeyu426)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and sourcing teams use this skill to build Alibaba.com search URLs, compare wholesale price ranges, sort results by price, and check MOQ-filtered listings before supplier follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Alibaba links include a traffic_type=ags_llm attribution marker that may be shared with Alibaba when opened or shared.

Mitigation: Review generated URLs before use and remove the attribution parameter manually only if the link still works for the intended search.

Risk: Alibaba listed prices and MOQ-filtered results may not reflect final negotiated supplier pricing.

Mitigation: Confirm final price, MOQ, shipping terms, and supplier details directly with suppliers before purchasing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zeyu426/skills/alibaba-price-finder)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with Alibaba.com URLs and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated URLs include traffic_type=ags_llm; final supplier pricing may require direct supplier confirmation.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
