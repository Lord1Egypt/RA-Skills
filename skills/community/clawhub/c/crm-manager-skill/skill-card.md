## Description:

A conversational CRM skill for administrators to create, update, query, search, and analyze YAML-backed customer records from natural language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luis1232023](https://clawhub.ai/user/luis1232023)

### License/Terms of Use:

MIT-0

## Use Case:

Employees or operators managing customer relationships use this skill to record customers, update contact and service history, search records, and generate sales or service analytics from local CRM data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Customer-name inputs can cause scripts to read or overwrite YAML files outside the intended CRM customer directory.

Mitigation: Run the skill only against a dedicated CRM data directory and reject untrusted customer names until path validation is fixed.

Risk: Customer YAML files and console output may expose sensitive CRM contact, service, and sales data.

Mitigation: Restrict runtime access to authorized users, require confirmation before writes or auto-tag updates, and treat generated reports as sensitive customer data.

## Reference(s):

- [CRM Manager Design Reference](references/design_reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown or plain-text agent responses with shell command examples and YAML customer records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read, write, and summarize customer YAML files when the packaged scripts are executed.]

## Skill Version(s):

4.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
