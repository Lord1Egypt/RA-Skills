## Description:

ACE Copilot helps agents support IBM App Connect Enterprise 12.0 work, including message flow development, ESQL scripting, BAR file deployment, integration node and server management, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shoaibkhan](https://clawhub.ai/user/shoaibkhan)

### License/Terms of Use:

MIT

## Use Case:

Developers and integration engineers use this skill for IBM ACE 12.0 development and operations tasks, including designing message flows, writing ESQL, building and deploying BAR files, diagnosing runtime issues, and preparing code changes for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated operational commands can target the wrong ACE node, server, queue, or environment if placeholders are copied without review.

Mitigation: Confirm target identifiers and environment before execution, test in dev or staging first, and require human review before production changes.

Risk: Credential-related examples include command flags and configuration fields where users might paste real passwords inline.

Mitigation: Use approved secret handling and ACE credential mechanisms, avoid inline real passwords in shell history or shared configuration, and rotate credentials if exposure is suspected.

Risk: Admin REST API and deployment examples can expose sensitive management surfaces if used outside trusted networks.

Mitigation: Keep ACE administration endpoints on trusted management networks and require TLS and authentication where applicable.

Risk: Trace output, logs, and support bundles can contain sensitive payloads, credentials, topology, or customer data.

Mitigation: Collect diagnostics only as needed, disable trace after troubleshooting, restrict access to bundles, and sanitize sensitive data before sharing.

## Reference(s):

- [ACE Copilot on ClawHub](https://clawhub.ai/shoaibkhan/skills/ace-copilot)
- [Publisher Profile](https://clawhub.ai/user/shoaibkhan)
- [Author GitHub Profile](https://github.com/ShoaibKhan)
- [Architecture](references/architecture.md)
- [Message Flows](references/message-flows.md)
- [ESQL](references/esql.md)
- [CLI Commands](references/cli-commands.md)
- [Deployment](references/deployment.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include IBM ACE ESQL snippets, BAR deployment commands, REST API examples, troubleshooting checklists, and configuration examples.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
