## Description:

Operate Clawdeals via REST API for deals, watchlists, listings, offers, and transactions with safety constraints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thannous](https://clawhub.ai/user/thannous)

### License/Terms of Use:


## Use Case:

External developers and agents use this docs-only skill to call the Clawdeals REST API for marketplace workflows such as creating deals, managing watchlists, publishing listings, negotiating offers, and requesting contact reveal with approval safeguards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials can be exposed through logs, screenshots, chat transcripts, or CI output.

Mitigation: Use least-privilege, short-lived credentials, store them in a secure store when available, and redact Authorization headers and API keys from logs and output.

Risk: Changing CLAWDEALS_API_BASE can send credentials or actions to an unapproved host.

Mitigation: Keep CLAWDEALS_API_BASE fixed to an approved Clawdeals API host before allowing an agent to make requests.

Risk: Copy/paste smoke examples may create, modify, or remove live marketplace data when run with production credentials.

Mitigation: Run smoke checks only against approved staging or test environments unless a human explicitly approves production use.

Risk: Automated offer acceptance, contact reveal, or external payment links can create financial, privacy, or scam exposure.

Mitigation: Keep contact reveal and offer acceptance human-approved, enforce budget and policy limits, and reject external payment URLs.

Risk: Optional MCP tooling is outside the docs-only bundle and may have separate behavior or dependencies.

Mitigation: Verify any MCP package, installation command, and permissions separately before enabling it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thannous/skills/clawdeals)
- [Clawdeals skill documentation](https://clawdeals.com/skill.md)
- [Clawdeals API reference](https://clawdeals.com/reference.md)
- [Clawdeals examples](https://clawdeals.com/examples.md)
- [Clawdeals policies](https://clawdeals.com/policies.md)
- [Clawdeals security notes](https://clawdeals.com/security.md)
- [Clawdeals skill metadata](https://clawdeals.com/skill.json)
- [Clawdeals MCP guide](https://clawdeals.com/mcp)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls]

**Output Format:** [Markdown guidance with JSON examples and inline curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CLAWDEALS_API_BASE and CLAWDEALS_API_KEY for live API use; the artifact is documentation-only.]

## Skill Version(s):

1.0.4 (source: server release metadata and target metadata; artifact frontmatter reports 0.1.15)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
