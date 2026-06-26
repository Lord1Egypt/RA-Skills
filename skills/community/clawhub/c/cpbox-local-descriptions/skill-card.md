## Description: <br>
Gets AI-generated markdown descriptions for local points of interest from POI IDs obtained through web search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sprintmint](https://clawhub.ai/user/sprintmint) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to request narrative markdown descriptions for local businesses or travel points of interest after obtaining POI IDs from a location-filtered web search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requests may trigger automatic x402 pay-per-use payment signing. <br>
Mitigation: Check pricing, wallet permissions, and spending limits before enabling automatic payment signing. <br>
Risk: POI IDs are sent to cpbox.io and payment flow may use an external facilitator. <br>
Mitigation: Review data-sharing expectations and external service trust before sending location-related identifiers. <br>
Risk: Descriptions are AI-generated from web search context and may be incomplete or inaccurate. <br>
Mitigation: Verify critical business or travel details against authoritative sources before publishing or acting on them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sprintmint/cpbox-local-descriptions) <br>
- [CPBox API Provider](https://www.cpbox.io) <br>
- [Local Descriptions Endpoint](https://www.cpbox.io/api/x402/local-descriptions) <br>
- [CPPAY Facilitator](https://www.cppay.finance) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown descriptions returned in JSON responses, with curl and x402-payment command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires 1-20 POI IDs from web-search; POI IDs are short-lived and requests may trigger x402 payment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
