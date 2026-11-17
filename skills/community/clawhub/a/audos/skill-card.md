## Description:

Create AI-powered startup workspaces via the Audos API, including onboarding, build monitoring, workspace links, and follow-up guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[werdelin](https://clawhub.ai/user/werdelin)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this skill to help an agent collect a startup idea, complete Audos onboarding, monitor the workspace build, and return the generated landing page and workspace. It is suited for users who want to start a business, validate an idea, or create an MVP with Audos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow sends email addresses, business ideas, OTP codes, and workspace chat content to Audos.

Mitigation: Confirm the user understands what data will be sent before onboarding, and avoid entering sensitive personal or confidential business information unless Audos is approved for that use.

Risk: The skill describes non-expiring Audos auth tokens and recommends persistent storage.

Mitigation: Keep auth tokens out of ordinary agent memory, logs, and plaintext files; use approved secret storage or session-scoped handling and revoke or rotate tokens when exposure is suspected.

Risk: Helper scripts can send credentials to a custom endpoint through AUDOS_BASE_URL.

Mitigation: Use the default Audos API endpoint unless the alternate endpoint has been explicitly reviewed and trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/werdelin/skills/audos)
- [Audos](https://audos.com)
- [Audos API base](https://audos.com/api/agent/onboard)
- [Audos Publishing House](https://audos.com/publishing)
- [Live demo](https://audos.com/site/103877)
- [GitHub repository referenced by README](https://github.com/prehype/audos-agent-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Audos API request details, polling status updates, generated workspace URLs, and Otto chat guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
