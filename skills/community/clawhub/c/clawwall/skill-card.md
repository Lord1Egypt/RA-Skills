## Description:

Outbound DLP for OpenClaw — hard regex blocks secrets & PII from leaving the machine. Domain control, no LLM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stanxy](https://clawhub.ai/user/stanxy)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use ClawWall to scan outbound agent tool calls for secrets and PII before data leaves the local machine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local scan service may be exposed beyond loopback when configured with the documented default bind address.

Mitigation: Prefer binding the service to 127.0.0.1 before use.

Risk: The documented fail-open configuration can allow outbound tool calls if the scan service is unreachable.

Mitigation: Set blockOnError to true when relying on ClawWall for DLP enforcement.

Risk: Installation involves downloaded Python packages, source checkout, and npm build steps.

Mitigation: Install in an isolated environment and verify downloaded packages or source before running build steps.

## Reference(s):

- [ClawWall ClawHub skill page](https://clawhub.ai/stanxy/skills/clawwall)
- [ClawWall PyPI project](https://pypi.org/project/clawwall)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown with inline bash, JSON, and YAML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local service setup guidance, OpenClaw plugin configuration, policy examples, and operational safety notes.]

## Skill Version(s):

0.2.2 (source: server release metadata; artifact frontmatter reports 0.2.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
