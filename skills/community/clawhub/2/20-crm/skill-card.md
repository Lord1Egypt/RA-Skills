## Description: <br>
Interact with Twenty CRM (self-hosted) via REST/GraphQL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[w7tf](https://clawhub.ai/user/w7tf) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to configure an agent for a self-hosted Twenty CRM instance and perform REST or GraphQL operations such as finding companies, creating companies, and updating CRM records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write, update, or delete business CRM data through Twenty REST and GraphQL calls. <br>
Mitigation: Use a narrowly scoped Twenty API key and require explicit user approval before PATCH or DELETE operations. <br>
Risk: The shell configuration loader can source a file selected through TWENTY_CONFIG_FILE. <br>
Mitigation: Set TWENTY_CONFIG_FILE only to a trusted local file, use restrictive file permissions, or export TWENTY_BASE_URL and TWENTY_API_KEY directly. <br>
Risk: The skill handles a bearer token for Twenty CRM. <br>
Mitigation: Keep TWENTY_API_KEY out of source control and shared files, and rotate the token if it is exposed. <br>


## Reference(s): <br>
- [Twenty CRM ClawHub listing](https://clawhub.ai/w7tf/20-crm) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration guidance, API calls, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, python3, TWENTY_BASE_URL, and TWENTY_API_KEY.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
