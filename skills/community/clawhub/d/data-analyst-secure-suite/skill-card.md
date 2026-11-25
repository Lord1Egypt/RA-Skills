## Description:

A secure data analysis workflow suite based on MGC Blackbox 1.6.0+, providing credential protection, zero-exposure script & workflow application, workflow / skill-package sealed-authorization collaboration, and knowledge management. Supports 1.5.4 double-layer encryption with link authorization and free-mode sealing, plus 1.6.0 chain mode for multi-node sealed distribution (one seal → multiple independent sub-packages + distribution_index.json). Includes a Data Analyst Agent system prompt template.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zkeviny](https://clawhub.ai/user/zkeviny)

### License/Terms of Use:

MIT-0

## Use Case:

Data analysts and developers use this suite to follow workflows for managing credentials and knowledge, storing and running analysis scripts, and collaborating through sealed workflow packages with explicit user authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flagged potentially misleading assurances about credential rotation.

Mitigation: Confirm that replaced credentials are revoked with the service that issued them.

Risk: The security review flagged potentially misleading assurances about knowledge privacy.

Mitigation: Check whether knowledge sent to the AI can appear in its context before sharing sensitive content.

Risk: The local credential API's necessity and trustworthiness should be assessed.

Mitigation: Review the local API and its access requirements before relying on it for credential access.

Risk: Security review coverage was partial because some referenced paths could not be resolved.

Mitigation: Review unresolved references before installing or relying on the suite.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zkeviny/skills/data-analyst-secure-suite)
- [MGC Blackbox project](https://github.com/zkeviny/MGC-Blackbox)
- [MGC Blackbox issue tracker](https://github.com/zkeviny/MGC-Blackbox/issues)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown instructions with Python examples, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes user authorization templates and MGC credential, workflow, collaboration, and knowledge management procedures.]

## Skill Version(s):

1.5.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
