## Description: <br>
Searches and retrieves US business entity data from the Filed.dev API for entity verification, registered agent lookup, officer searches, status checks, and business due diligence across supported US states. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mgrantley](https://clawhub.ai/user/mgrantley) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and business users use this skill to search Filed.dev business-entity data and retrieve company status, registered agent, officer, filing, and address details for KYB and due diligence workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted search terms can trigger local code execution in the shell helper. <br>
Mitigation: Review or patch the URL-encoding path before use, and only run searches with trusted lookup terms until fixed. <br>
Risk: Business lookup terms and returned entity details are sent to Filed.dev. <br>
Mitigation: Use a dedicated Filed.dev API key and avoid submitting sensitive company, officer, agent, filing, or entity lookup terms unless that disclosure is acceptable. <br>


## Reference(s): <br>
- [Filed API Reference](references/api-docs.md) <br>
- [Filed.dev](https://filed.dev) <br>
- [Filed.dev Pricing](https://filed.dev/pricing) <br>
- [RapidAPI Filed API](https://rapidapi.com/grantley-holdings-grantley-holdings-default/api/filed2) <br>
- [ClawHub Skill Page](https://clawhub.ai/mgrantley/filed) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, formatted text results, or raw JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FILED_API_KEY and curl; jq is optional for formatted output.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
