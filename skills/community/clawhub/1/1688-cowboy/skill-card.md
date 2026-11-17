## Description:

1688 Cowboy helps 1688 merchants hire, configure, and monitor a preset reception assistant for customer reception, daily reports, transferred inquiries, and knowledge-base training.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

1688 merchants use this skill as a conversation entry point for recruiting a reception assistant, viewing reception performance, reviewing transferred inquiries, and training knowledge used by the assistant. The skill routes configuration changes to a management surface and uses CLI commands for data retrieval, simulation, and selected setup tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles AK credentials and local configuration that may expose secrets if passed or stored carelessly.

Mitigation: Review credential handling before installation, avoid passing AK values on the command line, and protect local configuration files.

Risk: The skill can trigger business-changing reception setup or knowledge changes.

Mitigation: Confirm that the release's business-change controls match the merchant's approval process before enabling write-capable workflows.

Risk: Gateway misconfiguration could redirect requests or send business data to an unintended service.

Mitigation: Verify the gateway URL and deployment routing before use.

Risk: Knowledge synchronization and answer persistence may process merchant or customer information.

Mitigation: Confirm that cloud knowledge sync and persisted answers align with the merchant's privacy and data-retention expectations.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/1688aiinfra/skills/1688-cowboy)
- [Publisher profile](https://clawhub.ai/user/1688aiinfra)
- [Interaction component specifications](artifact/references/interaction-specs.md)
- [Configuration capability reference](artifact/references/capabilities/configure.md)
- [Reception configuration service reference](artifact/references/capabilities/cowboy_config.md)
- [Daily report capability reference](artifact/references/capabilities/daily_report.md)
- [Knowledge management capability reference](artifact/references/capabilities/knowledge.md)
- [Transferred inquiries capability reference](artifact/references/capabilities/transfer_inquiries.md)
- [1688 work channel configuration](https://work.1688.com/connect/channel)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON command results containing markdown for agent-facing responses and structured data for routing or follow-up actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce interactive card data, configuration instructions, and command invocations for supported reception-assistant workflows.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
