## Description: <br>
Manages Didit identity-verification accounts, API keys, sessions, workflows, questionnaires, users, billing, blocklists, and webhooks across the platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rosasalberto](https://clawhub.ai/user/rosasalberto) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and verification administrators use this skill to manage Didit identity-verification operations, including account setup, workflow configuration, session creation and review, webhooks, billing, users, and blocklists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can administer Didit resources and perform sensitive changes such as user/session deletion, status overrides, billing actions, webhook updates, and blocklist changes. <br>
Mitigation: Use a least-privilege or test Didit key where possible and require explicit human approval before destructive, billing, webhook, status, or blocklist actions. <br>
Risk: Account setup and login flows can print API keys, access tokens, organization IDs, and application IDs to terminal output. <br>
Mitigation: Avoid running setup or login commands in logged or shared terminals; rotate exposed keys or tokens if credentials may have been captured. <br>


## Reference(s): <br>
- [Didit API Documentation](https://docs.didit.me) <br>
- [Didit Programmatic Registration Guide](https://docs.didit.me/integration/programmatic-registration) <br>
- [Didit Sessions API Overview](https://docs.didit.me/sessions-api/management-api) <br>
- [Didit Webhooks Guide](https://docs.didit.me/integration/webhooks) <br>
- [ClawHub Skill Page](https://clawhub.ai/rosasalberto/didit-verification-management) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code, shell commands, configuration examples, and JSON/API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Didit API requests and Python utility-script usage that require DIDIT_API_KEY or account credentials.] <br>

## Skill Version(s): <br>
4.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
