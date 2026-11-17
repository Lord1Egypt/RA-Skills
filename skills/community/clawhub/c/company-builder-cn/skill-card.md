## Description:

Helps Chinese-speaking OpenClaw users create and manage a multi-agent virtual company by collecting company, department, role, and staffing choices, then generating the corresponding workspace files and configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hkagi](https://clawhub.ai/user/hkagi)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and operators use this skill to design a virtual company, define departments and roles, recruit agents, and maintain the generated OpenClaw organization files and configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates and changes OpenClaw workspace files and configuration.

Mitigation: Review the planned company structure, generated files, and configuration changes before enabling the generated agents.

Risk: Generated employee instructions may allow broad personal-assistant monitoring and persistent actions beyond the company-builder purpose.

Mitigation: Remove or constrain generated AGENTS.md heartbeat, personal-service monitoring, bootstrap, memory, and git push instructions before granting access to private accounts or repositories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hkagi/skills/company-builder-cn)
- [Publisher profile](https://clawhub.ai/user/hkagi)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with generated workspace files, configuration updates, and command-oriented instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update OpenClaw workspace directories, agent markdown files, skill assignments, and openclaw.json configuration after user confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
