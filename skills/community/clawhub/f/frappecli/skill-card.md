## Description:

CLI for Frappe Framework / ERPNext instances that helps agents manage documents, files, reports, and RPC calls on a Frappe site.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pasogott](https://clawhub.ai/user/pasogott)

### License/Terms of Use:


## Use Case:

Developers and ERP administrators use this skill to operate Frappe Framework or ERPNext instances from an agent workflow, including document CRUD, file management, report execution, and RPC calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can enable broad ERP administration actions, including data-changing operations and RPC calls on production systems.

Mitigation: Use least-privileged API credentials, test in staging first, and require explicit approval before updates, deletes, uploads, report exports, or RPC calls in production.

Risk: The configuration file contains API credentials for Frappe or ERPNext sites.

Mitigation: Protect the configuration file, avoid sharing credentials in prompts or logs, and rotate credentials if exposure is suspected.

Risk: Installing or updating the CLI from an unpinned source can change the behavior available to an agent.

Mitigation: Verify or pin the CLI source before installation and review updates before using the skill on sensitive systems.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that operate on configured Frappe or ERPNext sites and produce table, JSON, or CSV CLI output.]

## Skill Version(s):

0.1.1 (source: server release metadata; artifact frontmatter lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
