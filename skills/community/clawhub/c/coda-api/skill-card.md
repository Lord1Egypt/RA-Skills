## Description: <br>
Coda API integration with managed OAuth for managing docs, pages, tables, rows, formulas, controls, permissions, and analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to access Coda through Maton-managed OAuth, including reading, creating, updating, and deleting Coda docs, pages, tables, rows, and related resources. It is intended for workflows where the user has a Maton API key and an authorized Coda connection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can edit or delete Coda content and change document sharing through the connected Coda account. <br>
Mitigation: Before approving write, delete, connection, or sharing changes, verify the exact account, document, table, page, row, principal, permission level, and intended effect. <br>
Risk: Using the wrong Maton connection can send requests to an unintended Coda account. <br>
Mitigation: When multiple Coda connections exist, specify the intended connection with the Maton-Connection header. <br>
Risk: The Maton API key is a sensitive credential for access through the gateway. <br>
Mitigation: Provide MATON_API_KEY only in trusted environments and install the skill only if Maton is trusted with access to the connected Coda account. <br>


## Reference(s): <br>
- [ClawHub Coda Skill](https://clawhub.ai/byungkyu/coda-api) <br>
- [Maton Homepage](https://maton.ai) <br>
- [Related API Gateway Skill](https://clawhub.ai/byungkyu/api-gateway) <br>
- [Coda API Reference](https://coda.io/apis/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with endpoint references and Python, JavaScript, JSON, and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MATON_API_KEY, network access, and an authorized Coda OAuth connection through Maton.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
