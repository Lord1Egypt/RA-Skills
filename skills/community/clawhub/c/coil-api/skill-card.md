## Description:

Use Coil's CLI and API to install, authenticate, discover, and operate Coil workflows for outbound recipes, durable runs, lead management, automations, provider integrations, feedback, and runtime discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[doubledipcode](https://clawhub.ai/user/doubledipcode)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Developers and agent operators use this skill to configure Coil credentials, discover supported CLI/API capabilities, run outbound recipes, manage leads and automations, and relay required human review actions during Coil workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Coil CLI is installed from npm and can access organization credentials and outbound workflow data.

Mitigation: Install only after trusting the Coil npm publisher, prefer a sandboxed or project-local install, and grant the CLI only scoped, rotatable secrets.

Risk: Coil workflows may handle provider tokens, LinkedIn cookies, lead records, exports, and automation outputs.

Mitigation: Supply secrets through a runtime secret manager or stdin, avoid logging sensitive values, and review data exports before sharing them.

Risk: Server-returned human-action URLs may be required before publication, provider authorization, or reconciliation steps.

Mitigation: Relay only the server-provided URL and label, and require a human organization admin to review the destination before taking admin actions.

## Reference(s):

- [Coil homepage](https://www.usecoil.com)
- [Coil API Endpoints](references/api-endpoints.md)
- [Coil API Fields](references/api-fields.md)
- [Coil API ClawHub page](https://clawhub.ai/doubledipcode/skills/coil-api)
- [DoubleDipCode publisher profile](https://clawhub.ai/user/doubledipcode)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON-oriented operating guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance emphasizes JSON CLI output, server-provided human-action URLs, stdin-based secret handling, and authenticated Coil organization context.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
