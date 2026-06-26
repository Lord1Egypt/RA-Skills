## Description: <br>
Bootstrap and manage an open, file-based CRM using the CRM-in-a-Box protocol for contacts, pipeline, and interactions as NDJSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[taylorhou](https://clawhub.ai/user/taylorhou) <br>

### License/Terms of Use: <br>
BSL 1.1 <br>


## Use Case: <br>
Employees, external operators, and developers use this skill to bootstrap and maintain a local file-based CRM, including contacts, deal stages, and interaction logs without a SaaS dependency. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CRM files may contain sensitive contact, pipeline, and interaction data. <br>
Mitigation: Install and run the skill only in CRM workspaces the agent is allowed to inspect and modify, and avoid storing secrets in CRM files. <br>
Risk: Agent actions can append or modify local CRM records. <br>
Mitigation: Use least-privilege repository access and review write or action steps before they run. <br>
Risk: Adapting shell search examples with untrusted input can create quoting issues. <br>
Mitigation: Quote search terms and other user-provided values safely when adapting shell commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/taylorhou/crm-in-a-box) <br>
- [biz-in-a-box protocol family](https://biz-in-a-box.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON, YAML, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance for local CRM files such as contacts.ndjson, pipeline.ndjson, interactions.ndjson, and config.yaml.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
