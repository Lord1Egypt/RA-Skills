## Description: <br>
Helps agents manage Bohrium datasets through the bohr CLI and Bohrium OpenAPI, including listing, creating, deleting, uploading, and managing dataset versions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sorrymaker0624](https://clawhub.ai/user/sorrymaker0624) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and engineers use this skill when they want an agent to prepare commands or API snippets for Bohrium dataset operations such as uploading datasets, listing dataset metadata, checking quota, creating versions, and deleting datasets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Bohrium access keys. <br>
Mitigation: Store ACCESS_KEY in a secure environment or secret manager and do not commit real keys into configuration files. <br>
Risk: The skill can change or delete remote Bohrium datasets and versions. <br>
Mitigation: Verify dataset IDs before mutations and require explicit confirmation before deletes or version changes. <br>
Risk: The skill may recommend remote bohr CLI installer scripts. <br>
Mitigation: Review the installer source before running curl-to-bash commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sorrymaker0624/bohrium-dataset) <br>
- [Bohrium Platform](https://open.bohrium.com) <br>
- [Bohrium Dataset OpenAPI Endpoint](https://open.bohrium.com/openapi/v1/ds) <br>
- [Bohrium Dataset API Endpoint](https://openapi.dp.tech/openapi/v1/ds) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands, JSON snippets, and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands or API requests that require an ACCESS_KEY and can mutate remote Bohrium datasets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
