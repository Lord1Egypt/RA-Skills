## Description:

Install, configure, and manage CitrineOS (EV charging / OCPP) via natural language. Supports Docker, cloud hosting, and API operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[enenkov](https://clawhub.ai/user/enenkov)

### License/Terms of Use:


## Use Case:

Developers, operators, and EV charging teams use this skill to install, configure, troubleshoot, and operate CitrineOS deployments for OCPP charging infrastructure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide privileged host changes and start or stop infrastructure services.

Mitigation: Use it only in a test or controlled deployment, require explicit confirmation for operational actions, and verify authentication and firewall settings.

Risk: The skill can guide use of unpinned upstream code and EV charging operations APIs.

Mitigation: Pin reviewed versions before deployment and keep backend ports private.

## Reference(s):

- [CitrineOS core repository](https://github.com/citrineos/citrineos-core)
- [Docker Desktop installation documentation](https://docs.docker.com/get-docker/)
- [Docker Engine installation documentation](https://docs.docker.com/engine/install/)
- [ClawHub skill page](https://clawhub.ai/enenkov/skills/citrineos-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown guidance with inline shell commands and HTTP operation examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include operational commands and API requests that require user confirmation and environment-specific values.]

## Skill Version(s):

1.0.1 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
