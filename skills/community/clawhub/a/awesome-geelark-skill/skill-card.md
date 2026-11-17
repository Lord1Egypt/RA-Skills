## Description:

Interact with GeeLark Cloud Phone API for managing cloud phones, automation tasks, and social media operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geelarkbot](https://clawhub.ai/user/geelarkbot)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operators use this skill to manage GeeLark cloud phones, install apps, run diagnostics, and guide supervised social media RPA workflows through an AI agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles GeeLark API credentials and may touch third-party social media account sessions.

Mitigation: Review the credential flow before installation, keep credentials out of agent prompts, prefer environment variables or a secret store, restrict config permissions to 600, and rotate exposed tokens.

Risk: Automation can perform destructive, posting, credentialed RPA, or bulk operations.

Mitigation: Require explicit human confirmation before deletion, posting, credentialed RPA, or bulk actions, and use the provided delete helper instead of direct unattended deletion.

Risk: Cloud phone sessions can create cost or account exposure if left running.

Mitigation: Check account balance before operations, use auto-close session management, save logs, and review logs for sensitive data before sharing.

Risk: Local subprocess tools and device automation dependencies expand the execution surface.

Mitigation: Run diagnostics first, install adb and uiautomator2 from trusted sources, keep the API base URL fixed to the official GeeLark endpoint, and test in a sandbox before operational use.

## Reference(s):

- [GeeLark API Reference](references/api_reference.md)
- [GeeLark API Best Practices](references/best_practices.md)
- [ADB Operations Guide](references/cloudphone_operations.md)
- [RPA Tasks Guide](references/rpa_tasks.md)
- [Auto-Close Mechanism](references/auto_close.md)
- [GeeLark Official API Docs](https://github.com/GeeLark/geelark-openapi)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose API calls and local automation steps that require user credentials, installed dependencies, and human confirmation for sensitive actions.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
