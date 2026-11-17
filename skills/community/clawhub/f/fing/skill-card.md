## Description:

Query and troubleshoot Fing Local API monitoring agents for local network device inventory, presence, online/offline state, people/presence where supported, and read-only homelab network checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[naamah75](https://clawhub.ai/user/naamah75)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, homelab operators, and support agents use this skill to inspect Fing Local API health, summarize device inventory, check online/offline state, and review people/presence information when Fing Desktop supports it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Device inventory and people/presence output can expose sensitive home-network and household presence information.

Mitigation: Prefer summary output, share detailed device lists only for direct troubleshooting, and treat presence data as sensitive.

Risk: The documented local API uses an API key in a query string and may use plaintext HTTP.

Mitigation: Prefer localhost or an encrypted tunnel, avoid placing the API key directly on command lines, and keep workspace .env files protected.

## Reference(s):

- [Fing Local API summary](references/api-summary.md)
- [Fing Local API documentation](https://www.fing.com/integrations/local-api/)
- [ClawHub skill page](https://clawhub.ai/naamah75/skills/fing)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize Fing device and people/presence data; detailed inventory output can include sensitive local network identifiers.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
