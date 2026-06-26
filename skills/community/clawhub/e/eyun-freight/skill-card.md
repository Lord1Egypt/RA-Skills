## Description: <br>
Query ocean freight rates and search shipping prices via the Eyun freight assistant. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bobofrivia](https://clawhub.ai/user/bobofrivia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Freight operations users and agents use this skill to send ocean or air freight-rate questions to a configured Eyun service and return the service response to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user freight questions to a configured Eyun service, which may include customer, shipment, or commercial details. <br>
Mitigation: Use only a trusted EYUN_BASE_URL, configure the correct authorized EYUN_COMPANY_ID, and avoid sending secrets or unnecessary personal, customer, or shipment details. <br>
Risk: Enterprise account scoping depends on local configuration. <br>
Mitigation: Review the configured EYUN_COMPANY_ID before deployment and keep separate test and production configurations where possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bobofrivia/eyun-freight) <br>
- [Publisher profile](https://clawhub.ai/user/bobofrivia) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Configuration guidance] <br>
**Output Format:** [Markdown response text with optional structured data blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl plus EYUN_BASE_URL and EYUN_COMPANY_ID configuration.] <br>

## Skill Version(s): <br>
1.1.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
