## Description:

Manage Acumatica ERP customization projects through the CustomizationApi web API for export, import, publish, validation, deletion, status checks, and maintenance-mode workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[allanwei](https://clawhub.ai/user/allanwei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ERP administrators use this skill to automate Acumatica customization project lifecycle tasks across development, promotion, backup, publication, and maintenance workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commands can make production-impacting Acumatica changes, including publish, unpublish, delete, import, and maintenance-mode actions.

Mitigation: Confirm the target instance and tenant before execution, use a least-privileged Customizer account, and review planned operations before applying them to production.

Risk: Credentials may be exposed if the Acumatica instance URL uses plaintext HTTP or if the local configuration file is not protected.

Mitigation: Use a trusted HTTPS Acumatica URL, store credentials only in a protected acumatica.conf file, and restrict local file permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/allanwei/skills/acumatica-customization)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide commands that call Acumatica REST endpoints and read local configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
