## Description: <br>
Queries enterprise address, phone, email, website, and related contact details by company name, unified social credit code, registration number, or organization code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to look up business contact details for a company when they have the company name or a registration identifier. Agents can call the Python CLI, inspect the returned contact records, and summarize relevant contact information for the user with appropriate privacy handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Company names or registration identifiers are sent to JisuAPI and may consume API quota or incur charges. <br>
Mitigation: Use the skill only with an approved JISU_API_KEY and confirm that sending the queried company data to JisuAPI is appropriate for the use case. <br>
Risk: Returned phone numbers, emails, names, and roles can be privacy-sensitive business contact data. <br>
Mitigation: Share only the contact details needed for the user's request and handle returned records according to applicable privacy and business-data policies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/enterprisecontact) <br>
- [JisuAPI Enterprise Contact API](https://www.jisuapi.com/api/enterprisecontact/) <br>
- [JisuAPI homepage](https://www.jisuapi.com/) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Shell commands, Guidance] <br>
**Output Format:** [JSON from a Python command-line query, with natural-language guidance for agent responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; sends company names or registration identifiers to JisuAPI and may return privacy-sensitive business contact data.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
