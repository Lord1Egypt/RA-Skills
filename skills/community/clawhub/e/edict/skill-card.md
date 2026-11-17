## Description:

三省六部 (Edict) is an OpenClaw multi-agent orchestration skill that coordinates nine specialized agents for decision drafting, review, execution, model configuration, dashboard monitoring, and audit logging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhmza](https://clawhub.ai/user/zhmza)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to coordinate multi-agent AI governance workflows that separate proposal drafting, review, execution, resource allocation, security, compliance, and engineering work. It is suited for complex workflow orchestration, operational monitoring, model configuration, and audit-trail generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The dashboard configuration can expose a web interface beyond localhost when bound to 0.0.0.0.

Mitigation: Bind the dashboard to 127.0.0.1 unless external access is intentional, and add authentication before any non-local access.

Risk: The install and start scripts can install Python dependencies at runtime, creating supply-chain review risk.

Mitigation: Use a virtual environment or container, pin dependencies, and pin the edict runtime to a reviewed version or commit before deployment.

Risk: Audit logging may retain operational data for long periods.

Mitigation: Review retention settings and storage protections against the data and compliance requirements of the deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhmza/skills/edict)
- [README](README.md)
- [Skill Definition](SKILL.md)
- [Historical and Governance References](references/README.md)
- [Configuration Example](assets/config-example.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python examples, YAML configuration, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local configuration, logs, and data directories when installation scripts are executed.]

## Skill Version(s):

1.0.0 (source: server release evidence, artifact metadata, and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
