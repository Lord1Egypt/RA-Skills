## Description: <br>
Cognito Forms API integration with managed OAuth for accessing forms, entries, documents, and files through Maton. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent access Cognito Forms through Maton, including listing forms, managing entries, and retrieving documents and files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Maton API key and access to a connected Cognito Forms account. <br>
Mitigation: Keep MATON_API_KEY private and install the skill only when agent access to Cognito Forms through Maton is intended. <br>
Risk: Create, update, and delete requests can change or remove form entries. <br>
Mitigation: Approve write operations only after checking the form ID, entry ID, target connection, and expected effect. <br>
Risk: Multiple Cognito Forms connections can cause requests to target the wrong account. <br>
Mitigation: Verify the selected connection and use the Maton-Connection header when more than one active connection exists. <br>
Risk: Document and file retrieval can expose form submission data. <br>
Mitigation: Confirm the form ID, entry ID, document template number, or file ID before retrieving documents or files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/byungkyu/cognito-forms) <br>
- [Cognito Forms API Overview](https://www.cognitoforms.com/support/475/data-integration/cognito-forms-api) <br>
- [Cognito Forms REST API Reference](https://www.cognitoforms.com/support/476/data-integration/cognito-forms-api/rest-api-reference) <br>
- [Cognito Forms API Reference](https://www.cognitoforms.com/support/476/data-integration/cognito-forms-api/api-reference) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with inline Python, JavaScript, bash, HTTP, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and an authorized Cognito Forms OAuth connection.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
