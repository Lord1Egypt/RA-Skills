## Description: <br>
Finds, shortlists, vets, and enriches US cybersecurity firms using the ServiceGraph pro_services catalog. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nostrband](https://clawhub.ai/user/nostrband) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Procurement teams, founders, and security leaders use this skill to find and compare US B2B cybersecurity firms for pen testing, vCISO, SOC 2 readiness, incident response, cloud security, IAM, and AppSec needs. It can also enrich selected firm domains after the user approves any paid unlocks. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a ServiceGraph API key, which is sensitive credential material. <br>
Mitigation: Keep the key in the environment or .env.local and do not paste it into chat. <br>
Risk: Detailed firm records require paid credit unlocks. <br>
Mitigation: Present brief results first and ask the user to approve specific unlocks before spending credits. <br>
Risk: Search results are scoped to US B2B cybersecurity firms and can be unsuitable for consumer, DIY, recruiting, or non-US requests. <br>
Mitigation: Decline or redirect out-of-scope requests and validate filters before using results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nostrband/find-cybersecurity-firm) <br>
- [ServiceGraph API](https://api.servicegraph.co) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline API request examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a ServiceGraph API key; paid detail unlocks cost credits and should be confirmed before use.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
