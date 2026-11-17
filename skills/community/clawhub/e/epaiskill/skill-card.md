## Description:

EPAI provides a CLI for managing EPAI knowledge bases, documents, and catalogs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iamlovingit](https://clawhub.ai/user/iamlovingit)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to list, create, delete, upload to, and manage EPAI knowledge bases, documents, and catalog entries through the bundled CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI can perform high-impact EPAI administration actions, including deleting knowledge bases, catalogs, and documents.

Mitigation: Verify target IDs and intended effects before running delete or administrative commands, and use narrowly scoped API credentials.

Risk: The CLI sends requests and credentials to the configured EPAI_API_BASE and can optionally disable TLS verification through EPAI_VERIFY_TLS.

Mitigation: Use a trusted HTTPS endpoint, keep TLS verification enabled, and install the skill only when the publisher and endpoint are trusted.

Risk: Document upload sends the full selected local files to the configured EPAI service.

Mitigation: Review selected files before upload and avoid uploading sensitive or unauthorized content.

## Reference(s):

- [EPAI skill page](https://clawhub.ai/iamlovingit/skills/epaiskill)
- [Publisher profile](https://clawhub.ai/user/iamlovingit)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EPAI_API_BASE, EPAI_API_KEY, EPAI_ACCOUNT, and EPAI_VERIFY_TLS environment variables.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
