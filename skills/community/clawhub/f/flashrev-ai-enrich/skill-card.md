## Description:

Use this skill when an AI agent needs to enrich a CSV lead list through the flashrev-ai-enrich npm CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flashlabs-ai](https://clawhub.ai/user/flashlabs-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business operations teams use this skill to guide agents through schema-first FlashRev CSV enrichment for lead, company, person, contact, search, scrape, and row-level LLM workflows. It emphasizes live capability discovery, explicit mapping, dry-run validation, sample review, and token or credit spend reporting before full runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Contact enrichment can unlock paid lead data and consume tokens or credits.

Mitigation: Run token checks, dry-runs, and sample previews before live enrichment, and continue only after the user approves the spend and reviewed sample.

Risk: The FLASHREV_API_KEY could be exposed through files, logs, generated artifacts, or mapped request fields.

Mitigation: Keep FLASHREV_API_KEY in the environment, never print it, and never map API keys, OAuth tokens, passwords, cookies, or unrelated PII into customer_api headers or body.

Risk: The customer_api capability can send lead data to third-party URLs and can be used for internal-network requests.

Mitigation: Use customer_api only after confirming the destination domain and mapped fields; require separate explicit approval before --allow-internal-targets.

Risk: DNS rebinding or unrestricted outbound access may bypass documented host guardrails in sensitive corporate or cloud environments.

Mitigation: Restrict outbound network access with operating-system firewall rules or network ACLs when running this skill in sensitive environments.

## Reference(s):

- [FlashRev AI Enrich API Contract](references/api_contract.md)
- [FlashRev AI Enrich on ClawHub](https://clawhub.ai/flashlabs-ai/skills/flashrev-ai-enrich)
- [FlashRev Private App Key Settings](https://info.flashlabs.ai/settings/privateApps)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON report handling]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to produce enriched CSV outputs through the FlashRev CLI, with dry-run, sample preview, status counts, row errors, and token or credit spend reporting.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
