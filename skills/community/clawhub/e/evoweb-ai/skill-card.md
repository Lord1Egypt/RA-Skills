## Description:

Creates complete, responsive websites from brief natural language business descriptions using EvoWeb's hosted generation service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galizki](https://clawhub.ai/user/galizki)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to turn a concise business or project description into a generated live website and editor link through EvoWeb. It supports direct API use with an EvoWeb API key and a registration-link workflow when no API key is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Website descriptions, business details, and generated site content are sent to and hosted by EvoWeb.

Mitigation: Do not include secrets, credentials, private customer data, or confidential launch plans unless sharing them with EvoWeb is acceptable.

Risk: Direct API use requires an EvoWeb API key.

Mitigation: Keep EVOWEB_API_KEY in environment configuration and do not paste or expose the key in prompts, generated pages, or user-facing responses.

Risk: Website generation may consume EvoWeb account credits and generated sites remain hosted on EvoWeb infrastructure.

Mitigation: Confirm the account, billing, and hosting expectations before creating or remaking a site.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/galizki/skills/evoweb-ai)
- [EvoWeb homepage and API key registration](https://evoweb.ai/?utm_source=claw&utm_medium=skill&utm_campaign=website&utm_content=v1.0)
- [EvoWeb API base URL](https://api.evoweb.ai/openapi/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown text with JSON API payloads, polling status updates, and generated website URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EVOWEB_API_KEY for direct API use; without it, the skill produces a prefilled EvoWeb registration link.]

## Skill Version(s):

1.0.10 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
