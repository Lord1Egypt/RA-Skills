## Description: <br>
Frappecli helps an agent manage Frappe Framework and ERPNext instances, including doctypes, documents, files, reports, and RPC methods through the Frappe API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pasogott](https://clawhub.ai/user/pasogott) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to install and run frappecli for Frappe/ERPNext site administration, document CRUD, file transfers, report exports, and RPC calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through operations that affect Frappe/ERPNext business data, including document updates, deletes, uploads, exports, and RPC calls. <br>
Mitigation: Use least-privilege API keys, prefer staging first, and manually review production deletes, updates, uploads, exports, and RPC calls. <br>
Risk: Configuration examples require API keys and secrets in a local config file. <br>
Mitigation: Restrict the config file, avoid committing secrets, and rotate credentials if they are exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pasogott/frappecli) <br>
- [Publisher profile](https://clawhub.ai/user/pasogott) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and YAML code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that read or modify Frappe/ERPNext site data; review destructive operations before execution.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
