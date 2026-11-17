## Description:

Customer support via Crisp API for checking, reading, searching, and responding to Crisp inbox messages using environment-provided website and plugin credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paul-phan](https://clawhub.ai/user/paul-phan)

### License/Terms of Use:


## Use Case:

Support teams and operators use this skill to let an agent inspect Crisp inbox activity, read and search conversation history, send confirmed replies, mark conversations read, and resolve tickets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent read/write access to customer conversations and can perform customer-visible or ticket-closing actions.

Mitigation: Use a least-privilege Crisp plugin token and require explicit human approval before sending replies, marking conversations read, or resolving tickets.

Risk: Crisp credentials and customer conversation data may be exposed if credentials are stored in shared shell profiles or operational logs.

Mitigation: Keep CRISP_WEBSITE_ID, CRISP_TOKEN_ID, and CRISP_TOKEN_KEY out of shared profiles where possible, avoid logging tokens, and review access before production use.

Risk: Unpinned Python dependencies can change behavior across environments.

Mitigation: Install dependencies in a controlled virtual environment and pin them for production deployments.

## Reference(s):

- [Crisp API Reference](references/api.md)
- [Crisp Marketplace](https://marketplace.crisp.chat/)
- [Crisp Skill on ClawHub](https://clawhub.ai/paul-phan/skills/crisp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and optional JSON CLI output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke authenticated Crisp API calls through scripts/crisp.py when credentials are configured.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
