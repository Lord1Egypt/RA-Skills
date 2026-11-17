## Description:

This skill helps agents retrieve structured Amazon product details for a supplied ASIN using BrowserAct's Amazon ASIN Lookup API template.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phheng](https://clawhub.ai/user/phheng)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to look up Amazon product metadata, pricing, ratings, availability, descriptions, images, and specifications from a known ASIN. It is suitable for catalog enrichment, price comparison, review monitoring, availability checks, and market research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may expose a BrowserAct API key if the user provides it in chat.

Mitigation: Configure BROWSERACT_API_KEY outside chat using a protected local environment or secret manager, and rotate the key if it has already been shared.

Risk: ASIN lookup requests and task metadata are sent to BrowserAct's API.

Mitigation: Review whether the ASINs and related lookup activity are appropriate to send to BrowserAct before running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phheng/skills/amazon-asin-lookup-api-skill)
- [BrowserAct integrations console](https://www.browseract.com/reception/integrations)
- [BrowserAct workflow API endpoint](https://api.browseract.com/v2/workflow)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration]

**Output Format:** [Terminal logs followed by structured product data as text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and a BROWSERACT_API_KEY environment variable; the script polls BrowserAct until the lookup task finishes or fails.]

## Skill Version(s):

0.1.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
